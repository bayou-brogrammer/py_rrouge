#!/usr/bin/env python3

import logging
import sys
import warnings

import tcod

import constants
import g
import game.engine
import game.exceptions
import game.handlers


def main() -> None:
    tileset = tcod.tileset.load_tilesheet(
        constants.tileset, constants.tileset_columns, constants.tileset_rows, constants.charmap
    )

    with tcod.context.new(
        vsync=True,
        tileset=tileset,
        title=constants.title,
        rows=constants.screen_height,
        columns=constants.screen_width,
        renderer=tcod.RENDERER_OPENGL2,  # OpenGL Bonks out and fallsback to tcod.RENDERER_SDL2
    ) as g.context:

        g.engine = game.engine.Engine()
        g.engine.run_game()


if __name__ == "__main__":
    if __debug__:
        if not sys.warnoptions:
            warnings.simplefilter("default")
        logging.basicConfig(level=logging.DEBUG)
    main()
