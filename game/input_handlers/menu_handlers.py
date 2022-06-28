from __future__ import annotations

from pathlib import Path
from typing import Optional

import tcod
from PIL import Image  # type: ignore

import game.action
import game.actions
import game.color
import game.constants
import game.exceptions
import game.setup

from .base_event import BaseEventHandler

# Load the background image.  Pillow returns an object convertable into a NumPy array.
background_image = Image.open(Path(game.constants.bg_img))


class MainMenuHandler(BaseEventHandler):
    """Handle the main menu rendering and input."""

    def __init__(self) -> None:
        super().__init__()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[BaseEventHandler]:
        from .game_handler import MainGameEventHandler

        key = event.sym

        match key:
            case tcod.event.K_q | tcod.event.K_ESCAPE:
                raise SystemExit()
            case tcod.event.K_n:
                game.setup.new_game()
                return MainGameEventHandler()

        return None

    def on_render(self, console: tcod.Console) -> None:
        console.draw_semigraphics(background_image, 0, 0)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            game.constants.title_extended,
            fg=game.color.menu_title,
            alignment=tcod.CENTER,
        )
        console.print(
            console.width // 2,
            console.height - 2,
            f"By {game.constants.author}",
            fg=game.color.menu_title,
            alignment=tcod.CENTER,
        )

        for i, text in enumerate(["[N] Play a new game", "[C] Continue last game", "[Q] Quit"]):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(game.constants.menu_width),
                fg=game.color.menu_text,
                bg=game.color.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )
