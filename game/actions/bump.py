from __future__ import annotations

import snecs

import g
import game.exceptions
from game import ecs
from game.components.fov import FieldOfView
from game.components.intent import WantsToMelee
from game.components.position import Position

from .action import ActionWithDirection


class Move(ActionWithDirection):
    def perform(self) -> None:
        """Move the entity in the given direction."""

        pos = self.entity.get_component(Position)
        dest_x, dest_y = pos.x + self.dx, pos.y + self.dy

        if not g.engine.gamemap.in_bounds(dest_x, dest_y):
            raise game.exceptions.Impossible("That way is blocked.")  # Destination is out of bounds.
        if not g.engine.gamemap.tiles[dest_x, dest_y]:
            raise game.exceptions.Impossible("That way is blocked.")  # Destination is blocked by a tile.
        if self.blocking_entity:
            raise game.exceptions.Impossible("That way is blocked.")  # Destination is blocked by an entity.

        pos.x, pos.y = dest_x, dest_y
        if (fov := ecs.try_entity_component(self.entity.id, FieldOfView)) is not None:
            fov.dirty = True


class Melee(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise game.exceptions.Impossible("Nothing to attack.")

        print("Melee action")

        snecs.add_component(self.entity.id, WantsToMelee(target=target))


class Bump(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return Melee(self.entity, self.dx, self.dy).perform()
        else:
            return Move(self.entity, self.dx, self.dy).perform()
