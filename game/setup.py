"""Handle the loading and initialization of game sessions."""
from __future__ import annotations

import constants
import g
import game
import game.engine
import game.gamemap

from .spawner import spawn_monster, spawn_player


def new_game() -> None:
    """Return a brand new game session as an Engine instance."""
    gamemap = game.gamemap.GameMap(g.engine, constants.map_width, constants.map_height)
    player = spawn_player(gamemap, *gamemap.rooms[0].center)

    for room in gamemap.rooms[1:]:
        spawn_monster(gamemap, *room.center)

    g.engine.gamemap = gamemap
    g.engine.player = player
    g.engine.run_systems()
