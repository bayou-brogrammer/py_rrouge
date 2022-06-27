"""Handle spawning of entities"""
from __future__ import annotations

from game import color
from game.components import AI, FieldOfView, Player, Position, Renderable
from game.components.entity import BlocksTile
from game.components.stats import CombatStats
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
            CombatStats(hp=30, max_hp=30, defense=2, power=5),
        ]
    )


def spawn_monster(gamemap: GameMap, x: int, y: int) -> Actor:
    """Spawn a monster at the given coordinates."""
    return Actor(
        [
            AI(),
            Position(x, y),
            Renderable("g", color.red),
            FieldOfView(gamemap, 6),
            BlocksTile(),
            CombatStats(hp=16, max_hp=16, defense=1, power=4),
        ]
    )
