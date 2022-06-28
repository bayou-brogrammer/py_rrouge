from __future__ import annotations

from typing import Optional

import tcod

import game.action
from game.typing import ActionOrHandler


class BaseEventHandler(tcod.event.EventDispatch[ActionOrHandler]):
    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        """Handle an event and return the next active event handler."""
        state = self.dispatch(event)

        if isinstance(state, BaseEventHandler):
            return state

        assert not isinstance(state, game.action.Action), f"{self!r} can not handle actions."
        return self

    def on_render(self, console: tcod.Console) -> None:
        raise NotImplementedError()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[ActionOrHandler]:
        raise SystemExit()
