from __future__ import annotations

from typing import Optional

import tcod

import g
from game import rendering
from game.actions import Action
from game.typing import ActionOrHandler

from .base_handler import BaseEventHandler


class EventHandler(BaseEventHandler):
    def __init__(self) -> None:
        super().__init__()

    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        """Handle an event, perform any actions, then return the next active event handler."""
        # from .game_handler import MainGameEventHandler

        action_or_state = self.dispatch(event)
        if isinstance(action_or_state, EventHandler):
            return action_or_state

        if isinstance(action_or_state, Action) and self.handle_action(action_or_state):
            # A valid action was performed.
            return self  # Return to the main handler.
            # return MainGameEventHandler()  # Return to the main handler.

        return self

    def handle_action(self, action: Action) -> BaseEventHandler:
        return self

    def ev_quit(self, event: tcod.event.Quit) -> Optional[ActionOrHandler]:
        raise SystemExit()

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        if g.engine.gamemap.in_bounds(event.tile.x, event.tile.y):
            g.engine.mouse_location = event.tile.x, event.tile.y
            g.mouse_pos = event.tile.x, event.tile.y
        else:
            g.mouse_pos = None

    def on_render(self, console: tcod.Console) -> None:
        rendering.render_map(console)
        # game.rendering.render_ui(console, self.engine)
