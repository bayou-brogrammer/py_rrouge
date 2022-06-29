from __future__ import annotations

from typing import Optional

import g
import game.action
import game.color
import game.combat
import game.components
import game.engine
import game.entity
import game.exceptions
import game.input_handlers
from game.node import Node
from game.typing import ActionOrHandler


class Consumable(Node):
    @property
    def item(self) -> game.entity.Item:
        assert isinstance(self.parent, game.entity.Item)
        return self.parent

    def get_action(self, consumer: game.entity.Actor) -> Optional[ActionOrHandler]:
        """Try to return the action for this item."""
        return game.action.ItemAction(consumer, self.item)

    def activate(self, action: game.action.ItemAction) -> None:
        """Invoke this items ability.

        `action` is the context for this activation.
        """
        raise NotImplementedError()

    def consume(self) -> None:
        """Remove the consumed item from its containing inventory."""
        item = self.item
        inventory = item.parent
        assert isinstance(inventory, game.components.Inventory)
        inventory.items.remove(item)
        item.parent = None


class HealingConsumable(Consumable):
    def __init__(self, amount: int):
        super().__init__()
        self.amount = amount

    def activate(self, action: game.action.ItemAction) -> None:
        consumer = action.entity
        amount_recovered = game.combat.heal(consumer.fighter, self.amount)

        if amount_recovered > 0:
            g.engine.message_log.add_message(
                f"You consume the {self.item.name}, and recover {amount_recovered} HP!",
                game.color.health_recovered,
            )
            self.consume()
        else:
            raise game.exceptions.Impossible("Your health is already full.")
