from __future__ import annotations

from typing import Optional

import tcod

import g
import game.action
import game.rendering
from game.typing import ActionOrHandler

from .base_event import BaseEventHandler


class EventHandler(BaseEventHandler, game.rendering.GameRenderer):
    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        """Handle an event, perform any actions, then return the next active event handler."""
        from .game_handler import GameOverEventHandler

        action_or_state = self.dispatch(event)

        if isinstance(action_or_state, EventHandler):
            return action_or_state

        if isinstance(action_or_state, game.action.Action) and self.handle_action(action_or_state):
            if not g.engine.player.is_alive:
                # The player was killed sometime during or after the action.
                return GameOverEventHandler()
            return self
            # return MainGameEventHandler()  # Return to the main handler.

        return self

    def handle_action(self, action: game.action.Action) -> BaseEventHandler:
        return self

    def ev_quit(self, event: tcod.event.Quit) -> Optional[ActionOrHandler]:
        raise SystemExit()

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        if g.engine.gamemap.in_bounds(event.tile.x, event.tile.y):
            g.engine.mouse_location = event.tile.x, event.tile.y
