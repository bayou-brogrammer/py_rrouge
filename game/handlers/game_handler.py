from __future__ import annotations

import logging
from typing import Optional

import tcod

import g
from game import actions, exceptions, systems
from game.typing import ActionOrHandler

from .event_handler import EventHandler

MOVE_KEYS = {
    # Arrow keys.
    tcod.event.K_UP: (0, -1),
    tcod.event.K_DOWN: (0, 1),
    tcod.event.K_LEFT: (-1, 0),
    tcod.event.K_RIGHT: (1, 0),
    tcod.event.K_HOME: (-1, -1),
    tcod.event.K_END: (-1, 1),
    tcod.event.K_PAGEUP: (1, -1),
    tcod.event.K_PAGEDOWN: (1, 1),
    # Numpad keys.
    tcod.event.K_KP_1: (-1, 1),
    tcod.event.K_KP_2: (0, 1),
    tcod.event.K_KP_3: (1, 1),
    tcod.event.K_KP_4: (-1, 0),
    tcod.event.K_KP_6: (1, 0),
    tcod.event.K_KP_7: (-1, -1),
    tcod.event.K_KP_8: (0, -1),
    tcod.event.K_KP_9: (1, -1),
    # Vi keys.
    tcod.event.K_h: (-1, 0),
    tcod.event.K_j: (0, 1),
    tcod.event.K_k: (0, -1),
    tcod.event.K_l: (1, 0),
    tcod.event.K_y: (-1, -1),
    tcod.event.K_u: (1, -1),
    tcod.event.K_b: (-1, 1),
    tcod.event.K_n: (1, 1),
}


WAIT_KEYS = {
    tcod.event.K_PERIOD,
    tcod.event.K_KP_5,
    tcod.event.K_CLEAR,
}


CURSOR_Y_KEYS = {
    tcod.event.K_UP: -1,
    tcod.event.K_DOWN: 1,
    tcod.event.K_PAGEUP: -10,
    tcod.event.K_PAGEDOWN: 10,
}

logger = logging.getLogger(__name__)


class MainGameEventHandler(EventHandler):

    systems = [systems.FovSystem()]

    def handle_action(self, action: actions.Action) -> EventHandler:
        """Handle actions returned from event methods."""

        try:
            action.perform()
            g.engine.run_systems()
        except exceptions.Impossible as exc:
            logger.fatal(exc.args[0])
            return self

        # monster turn
        # g.engine.run_systems()

        return self

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        # from game.engine import TurnState

        key = event.sym

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            return actions.Bump(g.engine.player, dx=dx, dy=dy)
        elif __debug__ and key == tcod.event.KeySym.F8:
            g.fullbright = not g.fullbright

        return None
