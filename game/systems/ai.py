from typing import Tuple, Type

from game.components import AI, Position
from game.ecs import System

AICTypes = Tuple[Type[Position], Type[AI]]
AICs = Tuple[Position, AI]


class AISystem(System[AICTypes, AICs]):
    def process(self) -> None:
        for id, (pos, ai) in self.query():
            pass
