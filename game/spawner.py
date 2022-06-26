"""Handle spawning of entities"""
from __future__ import annotations

from game import color
from game.components import FieldOfView, Monster, Player, Position, Renderable
from game.entity import Actor
from game.gamemap import GameMap


def spawn_player(gamemap: GameMap, x: int, y: int) -> Actor:
    """Spawn the player at the given coordinates."""
    return Actor(
        [
            Player(),
            Position(x, y),
            Renderable("@", color.yellow),
            FieldOfView(gamemap, 8),
        ]
    )


def spawn_monster(gamemap: GameMap, x: int, y: int) -> Actor:
    """Spawn a monster at the given coordinates."""
    return Actor(
        [
            Monster(),
            Position(x, y),
            Renderable("g", color.red),
            FieldOfView(gamemap, 6),
        ]
    )
