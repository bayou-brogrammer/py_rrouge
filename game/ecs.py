from typing import Tuple, Type, TypeVar, overload

import snecs
from snecs.component import Component
from snecs.typedefs import EntityID

T1 = TypeVar("T1", bound="Component")
T2 = TypeVar("T2", bound="Component")
T3 = TypeVar("T3", bound="Component")

""" Entity Component"""


def entity_component(entity_id: EntityID, component_type: Type[T1]) -> T1:
    return snecs.entity_component(entity_id, component_type)


def try_entity_component(entity_id: EntityID, component_type: Type[T1]) -> T1 | None:
    try:
        return snecs.entity_component(entity_id, component_type)
    except KeyError:
        return None


""" Entity Components Overrides"""


@overload
def entity_components(
    entity_id: EntityID,
    component_types: Tuple[Type[T1]],
) -> Tuple[T1]:
    ...


@overload
def entity_components(
    entity_id: EntityID,
    component_types: Tuple[Type[T1], Type[T2]],
) -> Tuple[T1, T2]:
    ...


@overload
def entity_components(
    entity_id: EntityID,
    component_types: Tuple[Type[T1], Type[T2], Type[T3]],
) -> Tuple[T1, T2, T3]:
    ...


def entity_components(entity_id, component_types):  # type: ignore
    return snecs.entity_components(entity_id, component_types).values()
