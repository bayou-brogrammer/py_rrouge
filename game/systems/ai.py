import math
from typing import List, Tuple, Type

import numpy as np
import snecs
import tcod
from numpy.typing import NDArray

import g
from game.components import AI, FieldOfView, Position
from game.components.intent import WantsToMelee
from game.ecs import System

AICTypes = Tuple[Type[Position], Type[FieldOfView], Type[AI]]
AICs = Tuple[Position, FieldOfView, AI]


class AISystem(System[AICTypes, AICs]):
    def get_path_to(self, from_pos: Position, dest_pos: Position) -> List[Tuple[int, int]]:
        """Compute and return a path to the target position.

        If there is no valid path then returns an empty list.
        """
        # Copy the walkable array.
        cost: NDArray[np.int8] = np.array(g.engine.gamemap.tiles, dtype=np.int8)

        for idx, blocked in np.ndenumerate(g.engine.gamemap.blocked):
            x, y = idx[0], idx[1]
            if blocked and cost[x, y]:
                cost[x, y] += 10

        # Create a graph from the cost array and pass that graph to a new pathfinder.
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((from_pos.x, from_pos.y))  # Start position.

        # Compute the path to the destination and remove the starting point.
        path: List[List[int]] = pathfinder.path_to((dest_pos.x, dest_pos.y))[1:].tolist()

        # Convert from List[List[int]] to List[Tuple[int, int]].
        return [(index[0], index[1]) for index in path]

    def distance_to(self, from_pt: Position, to_pt: Position) -> float:
        """
        Return the distance between the current entity and the given (x, y) coordinate.
        """
        return math.sqrt((to_pt.x - from_pt.x) ** 2 + (to_pt.y - from_pt.y) ** 2)

    def process(self) -> None:
        from game.engine import TurnState

        if g.engine.turn_state != TurnState.MonsterTurn:
            return

        player_pos = g.engine.player.position
        for id, (current_pos, fov, _) in self.query():
            dx = player_pos.x - current_pos.x
            dy = player_pos.y - current_pos.y
            distance = max(abs(dx), abs(dy))
            if distance < 1.5:
                # Attack
                snecs.add_component(id, WantsToMelee(target=g.engine.player.id))
            elif fov.visible[player_pos.x, player_pos.y]:
                path = self.get_path_to(current_pos, player_pos)

                if path:
                    dest_x, dest_y = path.pop(0)

                    g.engine.gamemap.blocked[current_pos.x, current_pos.y] = False
                    current_pos.x = dest_x
                    current_pos.y = dest_y
                    g.engine.gamemap.blocked[dest_x, dest_y] = False
                    fov.dirty = True
