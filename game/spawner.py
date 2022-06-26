"""Handle spawning of entities"""
from __future__ import annotations

import snecs

from game import color
from game.components.fov import FieldOfView
from game.components.player import Player
from game.components.position import Position
from game.components.renderable import Renderable
from game.entity import Actor
from game.gamemap import GameMap


def spawn_player(gamemap: GameMap, x: int, y: int) -> Actor:
    """Spawn the player at the given coordinates."""
    return Actor(snecs.new_entity([Player(), Position(x, y), Renderable("@", color.yellow), FieldOfView(gamemap, 8)]))
