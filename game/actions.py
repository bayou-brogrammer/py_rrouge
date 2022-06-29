from __future__ import annotations

from typing import TYPE_CHECKING

import g
import game.color
import game.combat
import game.exceptions
from game.action import Action, ActionWithDirection, ItemAction

if TYPE_CHECKING:
    import game.entity


class Wait(Action):
    def perform(self) -> None:
        pass


class Move(ActionWithDirection):
    def perform(self) -> None:
        dest_x = self.entity.x + self.dx
        dest_y = self.entity.y + self.dy

        if not g.engine.gamemap.in_bounds(dest_x, dest_y):
            raise game.exceptions.Impossible("That way is blocked.")  # Destination is out of bounds.
        if not g.engine.gamemap.tiles[dest_x, dest_y]:
            raise game.exceptions.Impossible("That way is blocked.")  # Destination is blocked by a tile.
        if g.engine.gamemap.get_blocking_entity_at(dest_x, dest_y):
            raise game.exceptions.Impossible("That way is blocked.")  # Destination is blocked by an entity.

        self.entity.x, self.entity.y = dest_x, dest_y


class Melee(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise game.exceptions.Impossible("Nothing to attack.")

        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        if self.entity is g.engine.player:
            attack_color = game.color.player_atk
        else:
            attack_color = game.color.enemy_atk

        if damage > 0:
            g.engine.message_log.add_message(f"{attack_desc} for {damage} hit points.", attack_color)
            game.combat.apply_damage(target.fighter, damage)
        else:
            g.engine.message_log.add_message(f"{attack_desc} but does no damage.", attack_color)


class Bump(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return Melee(self.entity, self.dx, self.dy).perform()
        else:
            return Move(self.entity, self.dx, self.dy).perform()


class Pickup(Action):
    """Pickup an item and add it to the inventory, if there is room for it."""

    def __init__(self, entity: game.entity.Actor):
        super().__init__(entity)

    def perform(self) -> None:
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory

        for item in g.engine.gamemap.items_at_location(actor_location_x, actor_location_y):
            if len(inventory.items) >= inventory.capacity:
                raise game.exceptions.Impossible("Your inventory is full.")

            assert item.parent is g.engine.gamemap
            item.parent = self.entity.inventory
            inventory.items.append(item)

            g.engine.message_log.add_message(f"You picked up the {item.name}!")
            return

        raise game.exceptions.Impossible("There is nothing here to pick up.")


class DropItem(ItemAction):
    def perform(self) -> None:
        self.entity.inventory.drop(self.item)
