from typing import Tuple, Type

import g
from game import ecs
from game.components import Position
from game.components.entity import BlocksTile
from game.ecs import System

IndexCTypes = Tuple[Type[Position]]
IndexCs = Tuple[Position]


class IndexingSystem(System[IndexCTypes, IndexCs]):
    def process(self) -> None:
        g.engine.gamemap.clear_content_index()
        g.engine.gamemap.populate_blocked()

        for id, (pos,) in self.query():
            idx = g.engine.gamemap.idx(pos.x, pos.y)

            if ecs.try_entity_component(id, BlocksTile):
                g.engine.gamemap.blocked[pos.x, pos.y] = True

            g.engine.gamemap.tile_content[idx].append(id)
