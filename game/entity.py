from __future__ import annotations

from typing import TYPE_CHECKING, Collection, Optional, TypeVar

from game.components.fov import FieldOfView
from game.components.position import Position
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
    def position(self) -> Optional[Position]:
        return self.try_get_component(Position)

    @property
    def fov(self) -> Optional[FieldOfView]:
        return self.try_get_component(FieldOfView)
