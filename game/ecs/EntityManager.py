from __future__ import annotations

from typing import TYPE_CHECKING, Collection, Optional, Tuple, Type, TypeVar, overload

import snecs
from snecs.typedefs import EntityID

from .component import entity_component, entity_components

if TYPE_CHECKING:
    from snecs import Component

    T1 = TypeVar("T1", bound="Component")
    T2 = TypeVar("T2", bound="Component")
    T3 = TypeVar("T3", bound="Component")


class EntityManager:
    """Class to handle snecs ecs entities"""

    id: EntityID

    def __init__(self, *, components: Collection[Component] = ()) -> None:
        super().__init__()
        self.id = snecs.new_entity(components)

    def remove_component(self, component_type: Type[T1]) -> None:
        """Return the component associated with this entity."""
        return snecs.remove_component(self.id, component_type)

    def get_component(self, component_type: Type[T1]) -> T1:
        """Return the component associated with this entity."""
        return entity_component(self.id, component_type)

    ### Get Component Optional ###
    def try_get_component(self, component_type: Type[T1]) -> Optional[T1]:
        try:
            return snecs.entity_component(self.id, component_type)
        except KeyError:
            return None

    ### Get Components ###
    @overload
    def get_components(
        self,
        component_types: Tuple[Type[T1]],
    ) -> Tuple[T1]:
        ...

    @overload
    def get_components(
        self,
        component_types: Tuple[Type[T1], Type[T2]],
    ) -> Tuple[T1, T2]:
        ...

    @overload
    def get_components(
        self,
        component_types: Tuple[Type[T1], Type[T2], Type[T3]],
    ) -> Tuple[T1, T2, T3]:
        ...

    def get_components(self, component_types):  # type: ignore
        """Return the component associated with this entity."""
        return entity_components(self.id, component_types)

    ### Get Components Optional ###
    @overload
    def try_get_components(
        self,
        component_types: Tuple[Type[T1]],
    ) -> Optional[Tuple[T1]]:
        ...

    @overload
    def try_get_components(
        self,
        component_types: Tuple[Type[T1], Type[T2]],
    ) -> Optional[Tuple[T1, T2]]:
        ...

    @overload
    def try_get_components(
        self,
        component_types: Tuple[Type[T1], Type[T2], Type[T3]],
    ) -> Optional[Tuple[T1, T2, T3]]:
        ...

    def try_get_components(self, component_types):  # type: ignore
        try:
            return snecs.entity_components(self.id, component_types).values()
        except KeyError:
            return None


if __name__ == "__main__":
    n = EntityManager()
