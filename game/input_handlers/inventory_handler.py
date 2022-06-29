from __future__ import annotations

from typing import Optional

import tcod

import g
import game.action
import game.actions
import game.constants
import game.entity
import game.exceptions
import game.render_functions
from game.typing import ActionOrHandler

from .game_handler import AskUserEventHandler


class InventoryEventHandler(AskUserEventHandler):
    """This handler lets the user select an item.
    What happens then depends on the subclass.
    """

    TITLE = "<missing title>"

    def on_render(self, console: tcod.Console) -> None:
        """Render an inventory menu, which displays the items in the inventory, and the letter to select them.
        Will move to a different position based on where the player is located, so the player can always see where
        they are.
        """
        super().on_render(console)

        number_of_items_in_inventory = len(g.engine.player.inventory.items)
        height = number_of_items_in_inventory + 2

        if height <= 3:
            height = 3

        width = len(self.TITLE) + 4
        x = game.constants.inventory_panel_x - width // 2
        y = game.constants.inventory_panel_y

        game.render_functions.render_panel(
            console,
            x,
            y,
            width,
            height,
            f" {self.TITLE} ",
            title_fg=(0, 0, 0),
            title_bg=(255, 255, 255),
        )

        if number_of_items_in_inventory > 0:
            for i, item in enumerate(g.engine.player.inventory.items):
                item_key = chr(ord("a") + i)

                # is_equipped = g.engine.player.equipment.item_is_equipped(item)

                item_string = f"({item_key}) {item.name}"

                # if is_equipped:
                #     item_string = f"{item_string} (E)"

                console.print(x + 1, y + i + 1, item_string)
        else:
            console.print(x + width // 2 - 2, y + 1, "[Empty]")

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        player = g.engine.player
        key = event.sym
        index = key - tcod.event.K_a

        if 0 <= index <= 26:
            try:
                selected_item = player.inventory.items[index]
            except IndexError:
                g.engine.message_log.add_message("Invalid entry.", game.color.invalid)
                return None
            return self.on_item_selected(selected_item)
        return super().ev_keydown(event)

    def on_item_selected(self, item: game.entity.Item) -> Optional[ActionOrHandler]:
        """Called when the user selects a valid item."""
        raise NotImplementedError()


class InventoryActivateHandler(InventoryEventHandler):
    """Handle using an inventory item."""

    TITLE = "Select an item to use"

    def on_item_selected(self, item: game.entity.Item) -> Optional[ActionOrHandler]:
        if item.consumable:
            # Return the action for the selected item.
            return item.consumable.get_action(g.engine.player)
        # elif item.equippable:
        #     return game.actions.Equip(g.engine.player, item)
        else:
            return None


class InventoryDropHandler(InventoryEventHandler):
    """Handle dropping an inventory item."""

    TITLE = "Select an item to drop"

    def on_item_selected(self, item: game.entity.Item) -> Optional[ActionOrHandler]:
        """Drop this item."""
        return game.actions.DropItem(g.engine.player, item)
