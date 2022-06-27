from typing import Tuple, Type

import tcod

import g
from game.components import Player, Position
from game.ecs import System

InputCTypes = Tuple[Type[Position], Type[Player]]
InputCs = Tuple[Position, Player]


class PlayerInputSystem(System[InputCTypes, InputCs]):
    def process(self) -> None:
        from game.engine import TurnState

        if g.engine.turn_state != TurnState.PlayerTurn:
            return

        for id, (pos, _) in self.query():
            for event in tcod.event.wait():
                g.context.convert_event(event)
                print(event)
                g.engine.turn_state = TurnState.PlayerTurn
