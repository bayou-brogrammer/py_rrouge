from typing import Tuple

from game.components.position import Position
from game.entity import Actor


class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity  # The object performing the action.

    # @property
    # def engine(self) -> game.engine.Engine:
    #     return self.entity.get_parent(game.engine.Engine)

    def perform(self) -> None:
        """Perform this action now.
        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        pos = self.entity.get_component(Position)
        return pos.x + self.dx, pos.y + self.dy

    # @property
    # def blocking_entity(self) -> Optional[game.entity.Entity]:
    #     """Return the blocking entity at this actions destination.."""
    #     return g.engine.gamemap.get_blocking_entity_at(*self.dest_xy)

    # @property
    # def target_actor(self) -> Optional[game.entity.Actor]:
    #     """Return the actor at this actions destination."""
    #     return g.engine.gamemap.get_actor_at_location(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()


class Wait(Action):
    def perform(self) -> None:
        pass
