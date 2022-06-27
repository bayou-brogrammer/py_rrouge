from typing import Tuple, Type

import g
from game.components import CombatStats, Player
from game.ecs import System

EndTurnCTypes = Tuple[Type[CombatStats], Type[Player]]
EndTurnCs = Tuple[CombatStats, Player]


class EndTurnSystem(System[None, None]):
    def process(self) -> None:
        from game.engine import TurnState

        next_state = g.engine.turn_state
        match g.engine.turn_state:
            case TurnState.PreRun:
                next_state = TurnState.AwaitingInput
            case TurnState.PlayerTurn:
                next_state = TurnState.MonsterTurn
            case TurnState.MonsterTurn:
                next_state = TurnState.AwaitingInput

        if g.engine.player.get_component(CombatStats).hp <= 0:
            next_state = TurnState.GameOver

        g.engine.turn_state = next_state
