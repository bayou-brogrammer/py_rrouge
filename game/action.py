from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple

import g

if TYPE_CHECKING:
    import game.entity


class Action:
    def __init__(self, entity: game.entity.Actor) -> None:
        super().__init__()
        self.entity = entity  # The object performing the action.

    def perform(self) -> None:
        """Perform this action now.
        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class ActionWithDirection(Action):
    def __init__(self, entity: game.entity.Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[game.entity.Entity]:
        """Return the blocking entity at this actions destination.."""
        return g.engine.gamemap.get_blocking_entity_at(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[game.entity.Actor]:
        """Return the actor at this actions destination."""
        return g.engine.gamemap.get_actor_at_location(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()
