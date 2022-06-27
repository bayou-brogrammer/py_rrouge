from __future__ import annotations

import os
from typing import Optional

import tcod

import g
from game import actions, color, exceptions
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
QUIT_KEYS = {
    tcod.event.K_q,
    tcod.event.K_ESCAPE,
}


class MainGameEventHandler(EventHandler):
    def handle_action(self, action: actions.Action) -> EventHandler:
        """Handle actions returned from event methods."""
        from game.engine import TurnState

        try:
            action.perform()
        except exceptions.Impossible as exc:
            g.engine.message_log.add_message(exc.args[0], color.impossible)
            return self  # TODO: Should we allow for impossible actions to waste a turn?

        g.engine.turn_state = TurnState.PlayerTurn
        return self

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        from game.engine import TurnState

        if g.engine.turn_state != TurnState.AwaitingInput:
            return None

        key = event.sym

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            return actions.Bump(g.engine.player, dx=dx, dy=dy)
        elif key in WAIT_KEYS:
            return actions.Wait(g.engine.player)

        match key:
            case tcod.event.K_ESCAPE:
                raise SystemExit()

            # Debug Case
            case tcod.event.KeySym.F8:
                if __debug__:
                    g.fullbright = not g.fullbright

        return None


class GameOverEventHandler(EventHandler):
    def on_quit(self) -> None:
        """Handle exiting out of a finished game."""
        if os.path.exists("savegame.sav"):
            os.remove("savegame.sav")  # Deletes the active save file.
        raise exceptions.QuitWithoutSaving()  # Avoid saving a finished game.

    def ev_quit(self, event: tcod.event.Quit) -> None:
        self.on_quit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        if event.sym in QUIT_KEYS:
            self.on_quit()

    def on_render(self, console: tcod.Console) -> None:
        console.print(1, 1, "Game Over", fg=color.red)
