from __future__ import annotations

from typing import Optional

import tcod

import g
import game.action
import game.actions
import game.color
import game.constants
import game.entity
import game.exceptions
from game.rendering import InventoryRenderer
from game.typing import ActionOrHandler

from .game_handler import AskUserEventHandler


class InventoryEventHandler(AskUserEventHandler, InventoryRenderer):
    """This handler lets the user select an item.
    What happens then depends on the subclass.
    """

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
