#!/usr/bin/env python3
import logging
import sys
import traceback
import warnings
from pathlib import Path

import tcod

import g
import game.exceptions
import game.input_handlers
import game_io
from game import constants
from game.typing import EventHandlerLike


def main() -> None:
    screen_width = 80
    screen_height = 50

    tileset = tcod.tileset.load_tilesheet(
        Path(constants.tileset),
        *constants.tileset_bounds,
        charmap=constants.charmap,
    )
    event_handler: EventHandlerLike = game.input_handlers.MainMenuHandler()

    with tcod.context.new(
        columns=screen_width,
        rows=screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as g.context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        try:
            while True:
                root_console.clear()
                event_handler.on_render(console=root_console)
                g.context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        g.context.convert_event(event)
                        event_handler = event_handler.handle_events(event)
                except Exception:  # Handle exceptions in game.
                    traceback.print_exc()  # Print error to stderr.
                    # Then print the error to the message log.
                    if isinstance(event_handler, game.input_handlers.EventHandler):
                        g.engine.message_log.add_message(traceback.format_exc(), game.color.error)
        except game.exceptions.QuitWithoutSaving:
            raise SystemExit()
        except SystemExit:  # Save and quit.
            game_io.save_game(Path("savegame.sav"))
            raise
        except BaseException:  # Save on any other error.
            game_io.save_game(Path("savegame.sav"))
            raise


if __name__ == "__main__":
    if __debug__:
        if not sys.warnoptions:
            warnings.simplefilter("default")
        logging.basicConfig(level=logging.DEBUG)
    main()
