from __future__ import annotations

import logging
import random

import tcod

import game.entity
import game.exceptions
import game.game_map
from game.components.ai import BaseAI
from game.node import Node

logger = logging.getLogger(__name__)


class Engine(Node):
    gamemap: game.game_map.GameMap
    game_world: game.game_map.GameWorld
    player: game.entity.Actor
    rng: random.Random
    mouse_location = (0, 0)

    def __init__(self) -> None:
        super().__init__()
        self.rng = random.Random()

    def handle_enemy_turns(self) -> None:
        logger.info("Enemy turn.")
        for entity in set(self.gamemap.actors) - {self.player}:
            ai = entity.try_get(BaseAI)
            if ai:
                try:
                    ai.perform()
                except game.exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.gamemap.visible[:] = tcod.map.compute_fov(
            self.gamemap.tiles,
            (self.player.x, self.player.y),
            radius=8,
            algorithm=tcod.FOV_SYMMETRIC_SHADOWCAST,
        )

        # If a tile is currently "visible" it will also be marked as "explored".
        self.gamemap.explored |= self.gamemap.visible
