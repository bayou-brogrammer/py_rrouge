from typing import Tuple, Type

import tcod

import g
from game.components.fov import FieldOfView
from game.components.position import Position
from game.ecs import System

FovCTypes = Tuple[Type[Position], Type[FieldOfView]]
FovCs = Tuple[Position, FieldOfView]


class FovSystem(System[FovCTypes, FovCs]):
    def process(self) -> None:
        for id, (pos, fov) in self.query():
            if fov.dirty:
                fov.dirty = False
                fov.visible[:] = tcod.map.compute_fov(
                    g.engine.gamemap.tiles,
                    (pos.x, pos.y),
                    radius=fov.radius,
                    algorithm=tcod.FOV_SYMMETRIC_SHADOWCAST,
                )

                if id == g.engine.player.id:
                    g.engine.gamemap.visible[:] = fov.visible
                    g.engine.gamemap.explored[:] |= fov.visible
