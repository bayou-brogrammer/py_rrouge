from __future__ import annotations

import random
from typing import TYPE_CHECKING, Any, Iterator, Optional, Tuple, Type, TypeVar

import numpy as np
from numpy.typing import NDArray

import game.constants
import game.entity
from game.constants import SHROUD
from game.node import Node

if TYPE_CHECKING:
    import game.engine

E = TypeVar("E", bound="game.entity.Entity")


class GameMap(Node):
    rng: random.Random
    player_start: Tuple[int, int]
    downstairs_location: Tuple[int, int]

    def __init__(self, engine: game.engine.Engine, width: int, height: int):
        super().__init__()

        self.width, self.height = width, height
        self.engine = engine
        self.rng = engine.rng

        self.tiles: NDArray[np.uint8] = np.zeros((width, height), dtype=np.uint8, order="F")

        self.memory: NDArray[Any] = np.full((width, height), fill_value=SHROUD, order="F")
        self.visible = np.full((width, height), fill_value=False, order="F")  # Tiles the player can currently see
        self.explored = np.full((width, height), fill_value=False, order="F")  # Tiles the player has seen before

    @property
    def entities(self) -> Iterator[game.entity.Entity]:
        yield from self.get_children(game.entity.Entity)

    @property
    def actors(self) -> Iterator[game.entity.Actor]:
        yield from self.get_children(game.entity.Actor)

    @property
    def items(self) -> Iterator[game.entity.Item]:
        yield from self.get_children(game.entity.Item)

    @property
    def gamemap(self) -> GameMap:
        return self

    def entities_at_location(self, x: int, y: int, t: Type[E]) -> Iterator[E]:
        for entity in self.entities:
            if isinstance(entity, t) and entity.x == x and entity.y == y:
                yield entity

    def actors_at_location(self, x: int, y: int) -> Iterator[game.entity.Actor]:
        for e in self.entities_at_location(x, y, game.entity.Actor):
            yield e

    def items_at_location(self, x: int, y: int) -> Iterator[game.entity.Item]:
        for e in self.entities_at_location(x, y, game.entity.Item):
            yield e

    def get_blocking_entity_at(self, x: int, y: int) -> Optional[game.entity.Entity]:
        """Returns an entity that blocks the position at x,y if one exists, otherwise returns None."""
        for entity in self.entities_at_location(x, y, game.entity.Entity):
            if entity.blocks_movement:
                return entity

        return None

    def get_actor_at_location(self, x: int, y: int) -> Optional[game.entity.Actor]:
        for actor in self.actors_at_location(x, y):
            if actor.blocks_movement:
                return actor

        return None

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height
