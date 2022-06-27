from typing import Tuple, Type

import numpy as np

import g
from game.components import Position
from game.ecs import System

IndexCTypes = Tuple[Type[Position]]
IndexCs = Tuple[Position]


class IndexingSystem(System[IndexCTypes, IndexCs]):
    def process(self) -> None:
        g.engine.gamemap.clear()

        for id, (pos,) in self.query():
            g.engine.gamemap.test = np.append(g.engine.gamemap.test, id)

        print(g.engine.gamemap.test)
