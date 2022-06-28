"""Handle the loading and initialization of game sessions."""
from __future__ import annotations

import g
import game.constants
import game.engine
import game.entity_factories
import game.game_map


def new_game() -> game.engine.Engine:
    """Return a brand new game session as an Engine instance."""
    engine = game.engine.Engine()
    engine.game_world = game.game_map.GameWorld(
        engine=engine,
        max_rooms=game.constants.max_rooms,
        room_min_size=game.constants.room_min_size,
        room_max_size=game.constants.room_max_size,
        map_width=game.constants.map_width,
        map_height=game.constants.map_height,
    )
    engine.game_world.generate_floor()

    engine.player = game.entity_factories.player.spawn(engine.gamemap, *engine.gamemap.player_start)
    engine.update_fov()

    # engine.message_log.add_message("Hello and welcome, adventurer, to yet another dungeon!", game.color.welcome_text)

    g.engine = engine
    return engine
