from __future__ import annotations

import random
from typing import TYPE_CHECKING, Dict, Iterator, List, Tuple

import tcod

import game.constants
import game.entity
import game.entity_factories
from game.tiles import TileType

from .game_map import GameMap
from .rect import Rect

if TYPE_CHECKING:
    import game.engine


MAX_ROOMS = game.constants.max_rooms
MIN_SIZE = game.constants.room_min_size
MAX_SIZE = game.constants.room_max_size


max_monsters_by_floor = [
    (1, 2),
    (4, 3),
    (6, 5),
]

max_items_by_floor = [
    (1, 1),
    (4, 2),
]

enemy_chances: Dict[int, List[Tuple[game.entity.Entity, int]]] = {
    0: [(game.entity_factories.orc, 80)],
    3: [(game.entity_factories.troll, 15)],
    5: [(game.entity_factories.troll, 30)],
    7: [(game.entity_factories.troll, 60)],
}

item_chances: Dict[int, List[Tuple[game.entity.Entity, int]]] = {
    0: [(game.entity_factories.health_potion, 35)],
    # 2: [(game.entity_factories.confusion_scroll, 10)],
    # 4: [(game.entity_factories.lightning_scroll, 25), (game.entity_factories.sword, 5)],
    # 6: [(game.entity_factories.fireball_scroll, 25), (game.entity_factories.chain_mail, 15)],
}


class GameWorld:
    """
    Holds the settings for the GameMap, and generates new maps when moving down the stairs.
    """

    def __init__(
        self,
        *,
        engine: game.engine.Engine,
        map_width: int,
        map_height: int,
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        current_floor: int = 0,
    ):
        self.engine = engine

        self.map_width = map_width
        self.map_height = map_height

        self.max_rooms = max_rooms

        self.room_min_size = room_min_size
        self.room_max_size = room_max_size

        self.current_floor = current_floor

    def __tunnel_between__(self, start: Tuple[int, int], end: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
        """Return an L-shaped tunnel between these two points."""
        x1, y1 = start
        x2, y2 = end
        if self.engine.rng.random() < 0.5:  # 50% chance.
            corner_x, corner_y = x2, y1  # Move horizontally, then vertically.
        else:
            corner_x, corner_y = x1, y2  # Move vertically, then horizontally.

        # Ge`       `   nerate the coordinates for this tunnel.
        for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
            yield x, y
        for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
            yield x, y

    def __get_max_value_for_floor__(self, max_value_by_floor: List[Tuple[int, int]], floor: int) -> int:
        current_value = 0

        for floor_minimum, value in max_value_by_floor:
            if floor_minimum > floor:
                break
            else:
                current_value = value

        return current_value

    def __get_entities_at_random__(
        self,
        weighted_chances_by_floor: Dict[int, List[Tuple[game.entity.Entity, int]]],
        number_of_entities: int,
        floor: int,
    ) -> List[game.entity.Entity]:
        entity_weighted_chances = {}

        for key, values in weighted_chances_by_floor.items():
            if key > floor:
                break
            else:
                for value in values:
                    entity = value[0]
                    weighted_chance = value[1]

                    entity_weighted_chances[entity] = weighted_chance

        entities = list(entity_weighted_chances.keys())
        entity_weighted_chance_values = list(entity_weighted_chances.values())

        chosen_entities = random.choices(entities, weights=entity_weighted_chance_values, k=number_of_entities)

        return chosen_entities

    def __place_entities__(self, room: Rect, dungeon: GameMap, floor_number: int) -> None:
        number_of_monsters = random.randint(0, self.__get_max_value_for_floor__(max_monsters_by_floor, floor_number))
        number_of_items = random.randint(0, self.__get_max_value_for_floor__(max_items_by_floor, floor_number))

        monsters: List[game.entity.Entity] = self.__get_entities_at_random__(
            enemy_chances,
            number_of_monsters,
            floor_number,
        )
        items: List[game.entity.Entity] = self.__get_entities_at_random__(
            item_chances,
            number_of_items,
            floor_number,
        )

        for entity in monsters + items:
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            if dungeon.get_blocking_entity_at(x, y):
                continue
            if (x, y) == dungeon.player_start:
                continue

            entity.spawn(dungeon, x, y)

    def __generate_dungeon__(self) -> GameMap:
        dungeon = GameMap(self.engine, self.map_width, self.map_height)
        dungeon.parent = self.engine

        rooms: List[Rect] = []
        center_of_last_room = (0, 0)

        for _ in range(MAX_ROOMS):
            room_width = self.engine.rng.randint(MIN_SIZE, MAX_SIZE)
            room_height = self.engine.rng.randint(MIN_SIZE, MAX_SIZE)

            x = self.engine.rng.randint(0, dungeon.width - room_width - 1)
            y = self.engine.rng.randint(0, dungeon.height - room_height - 1)

            # "RectangularRoom" class makes rectangles easier to work with.
            new_room = Rect(x, y, room_width, room_height)

            # Run through the other rooms and see if they intersect with this one.
            if any(new_room.intersects(other_room) for other_room in rooms):
                continue  # This room intersects, so go to the next attempt.
            # If there are no intersections then the room is valid.

            # Dig out this rooms inner area.
            dungeon.tiles[new_room.inner] = TileType.FLOOR.value

            if len(rooms) == 0:
                # The first room, where the player starts.
                dungeon.player_start = new_room.center
            else:  # All rooms after the first.
                # Dig out a tunnel between this room and the previous one.
                for x, y in self.__tunnel_between__(rooms[-1].center, new_room.center):
                    dungeon.tiles[x, y] = TileType.FLOOR.value

                center_of_last_room = new_room.center

            self.__place_entities__(new_room, dungeon, self.engine.game_world.current_floor)

            dungeon.tiles[center_of_last_room] = TileType.DOWN_STAIRS.value
            dungeon.downstairs_location = center_of_last_room

            # Finally, append the new room to the list.
            rooms.append(new_room)

        return dungeon

    def generate_floor(self) -> None:
        self.current_floor += 1
        self.engine.gamemap = self.__generate_dungeon__()
