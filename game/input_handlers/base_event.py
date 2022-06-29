from __future__ import annotations

from typing import Optional

import tcod

import game.action
import game.rendering
from game.typing import ActionOrHandler


class BaseEventHandler(tcod.event.EventDispatch[ActionOrHandler], game.rendering.Renderer):
    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        """Handle an event and return the next active event handler."""
        state = self.dispatch(event)

        if isinstance(state, BaseEventHandler):
            return state

        assert not isinstance(state, game.action.Action), f"{self!r} can not handle actions."
        return self

    def on_render(self, root_console: tcod.Console) -> None:
        self.render(root_console)

    def ev_quit(self, event: tcod.event.Quit) -> Optional[ActionOrHandler]:
        raise SystemExit()
