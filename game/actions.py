from __future__ import annotations

from typing import TYPE_CHECKING

import game.color
import game.exceptions
from game.action import Action, ActionWithDirection

if TYPE_CHECKING:
    import game.entity


class Wait(Action):
    def perform(self) -> None:
        pass


class Move(ActionWithDirection):
    def perform(self) -> None:
        dest_x = self.entity.x + self.dx
        dest_y = self.entity.y + self.dy

        if not self.engine.gamemap.in_bounds(dest_x, dest_y):
            raise game.exceptions.Impossible("That way is blocked.")  # Destination is out of bounds.
        if not self.engine.gamemap.tiles[dest_x, dest_y]:
            raise game.exceptions.Impossible("That way is blocked.")  # Destination is blocked by a tile.
        if self.engine.gamemap.get_blocking_entity_at(dest_x, dest_y):
            raise game.exceptions.Impossible("That way is blocked.")  # Destination is blocked by an entity.

        self.entity.x, self.entity.y = dest_x, dest_y


class Melee(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise game.exceptions.Impossible("Nothing to attack.")

        # damage = self.entity.fighter.power - target.fighter.defense

        # attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        # if self.entity is self.engine.player:
        #     attack_color = game.color.player_atk
        # else:
        #     attack_color = game.color.enemy_atk

        # if damage > 0:
        #     self.engine.message_log.add_message(f"{attack_desc} for {damage} hit points.", attack_color)
        #     game.combat.apply_damage(target.fighter, damage)
        # else:
        #     self.engine.message_log.add_message(f"{attack_desc} but does no damage.", attack_color)


class Bump(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return Melee(self.entity, self.dx, self.dy).perform()
        else:
            return Move(self.entity, self.dx, self.dy).perform()
