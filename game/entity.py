from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Iterable, Type, TypeVar

import snecs
from snecs.typedefs import EntityID

from game.components.fov import FieldOfView
from game.components.position import Position
from game.node import Node

if TYPE_CHECKING:
    from snecs import Component

    C = TypeVar("C", bound=Component)


class Entity(Node):
    """A generic object to represent players, enemies, items, etc."""

    id: EntityID

    def __init__(self, id: EntityID) -> None:
        super().__init__()
        self.id = id

    def remove_component(self, component_type: Type[C]) -> None:
        """Return the component associated with this entity."""
        return snecs.remove_component(self.id, component_type)

    def get_component(self, component_type: Type[C]) -> C:
        """Return the component associated with this entity."""
        return snecs.entity_component(self.id, component_type)

    def get_components(self, components: Iterable[Type[C]]) -> Dict[Type[Component], Component]:
        """Return the component associated with this entity."""
        return snecs.entity_components(self.id, components)


class Actor(Entity):
    def __init__(self, id: EntityID) -> None:
        super().__init__(id)

    @property
    def position(self) -> Position:
        return self.get_component(Position)

    @property
    def fov(self) -> FieldOfView:
        return self.get_component(FieldOfView)
