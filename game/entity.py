from __future__ import annotations

from typing import TYPE_CHECKING, Collection, Optional, TypeVar

from game.components import CombatStats, FieldOfView, Position
from game.ecs import EntityManager
from game.node import Node

if TYPE_CHECKING:
    from snecs import Component

    T1 = TypeVar("T1", bound="Component")
    T2 = TypeVar("T2", bound="Component")
    T3 = TypeVar("T3", bound="Component")


class Entity(EntityManager, Node):
    """A generic object to represent players, enemies, items, etc."""

    def __init__(self, components: Collection[Component] = ()) -> None:
        super().__init__(components=components)


class Actor(Entity):
    def __init__(self, components: Collection[Component] = ()) -> None:
        super().__init__(components)

    @property
    def position(self) -> Position:
        return self.get_component(Position)

    @property
    def fov(self) -> Optional[FieldOfView]:
        return self.try_get_component(FieldOfView)

    @property
    def stats(self) -> Optional[CombatStats]:
        return self.try_get_component(CombatStats)

    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return self.stats is not None and self.stats.hp > 0
