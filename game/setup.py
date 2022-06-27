"""Handle the loading and initialization of game sessions."""
from __future__ import annotations

import constants
import g
from game import entity_factories, gamemap


def new_game() -> None:
    """Return a brand new game session as an Engine instance."""
    g.engine.gamemap = gamemap.GameMap(g.engine, constants.map_width, constants.map_height)

    player_start = g.engine.gamemap.rooms[0].center
    g.engine.player = entity_factories.player.spawn(g.engine.gamemap, *player_start)
    g.engine.update_fov()
