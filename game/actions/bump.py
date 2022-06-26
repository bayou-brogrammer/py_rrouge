from __future__ import annotations

import g
import game.exceptions
from game import ecs
from game.components.fov import FieldOfView
from game.components.position import Position

from .action import ActionWithDirection


class Move(ActionWithDirection):
    def perform(self) -> None:
        """Move the entity in the given direction."""

        pos = ecs.entity_component(self.entity.id, (Position))
        dest_x, dest_y = pos.x + self.dx, pos.y + self.dy

        if not g.engine.gamemap.in_bounds(dest_x, dest_y):
            raise game.exceptions.Impossible("That way is blocked.")  # Destination is out of bounds.
        if not g.engine.gamemap.tiles[dest_x, dest_y]:
            raise game.exceptions.Impossible("That way is blocked.")  # Destination is blocked by a tile.
        # if g.engine.gamemap.get_blocking_entity_at(dest_x, dest_y):
        #     raise game.exceptions.Impossible("That way is blocked.")  # Destination is blocked by an entity.

        pos.x, pos.y = dest_x, dest_y

        if (fov := ecs.try_entity_component(self.entity.id, FieldOfView)) is not None:
            fov.dirty = True


class Melee(ActionWithDirection):
    def perform(self) -> None:
        pass


class Bump(ActionWithDirection):
    def perform(self) -> None:
        return Move(self.entity, self.dx, self.dy).perform()
