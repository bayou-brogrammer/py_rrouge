from typing import Callable, Iterator, Tuple, Type, TypeVar, overload

from snecs.component import Component
from snecs.query import Query
from snecs.typedefs import EntityID
from snecs.world import World, default_world

T1 = TypeVar("T1", bound="Component")
T2 = TypeVar("T2", bound="Component")
T3 = TypeVar("T3", bound="Component")
T4 = TypeVar("T4", bound="Component")


@overload
def typed_query(
    component_types: Tuple[Type[T1]],
    world: "World" = default_world,
) -> Iterator[Tuple[EntityID, T1]]:
    ...


@overload
def typed_query(
    component_types: Tuple[Type[T1], Type[T2]],
    world: "World" = ...,
) -> Iterator[Tuple[EntityID, Tuple[T1, T2]]]:
    ...


@overload
def typed_query(
    component_types: Tuple[Type[T1], Type[T2], Type[T3]],
    world: "World" = ...,
) -> Iterator[Tuple[EntityID, Tuple[T1, T2, T3]]]:
    ...


@overload
def typed_query(
    component_types: Tuple[Type[T1], Type[T2], Type[T3], Type[T4]],
    world: "World" = ...,
) -> Iterator[Tuple[EntityID, Tuple[T1, T2, T3, T4]]]:
    ...


def typed_query(  # type: ignore
    component_types, world=default_world
) -> Iterator[Tuple[EntityID, Tuple[Component, ...]]]:
    for entity_id, components in Query(component_types, world):
        yield entity_id, tuple(components)


@overload
def typed_compiled_query(
    component_types: Tuple[Type[T1]],
    world: "World" = ...,
) -> Callable[[], Iterator[Tuple[EntityID, Tuple[T1]]]]:
    ...


@overload
def typed_compiled_query(
    component_types: Tuple[Type[T1], Type[T2]],
    world: "World" = ...,
) -> Callable[[], Iterator[Tuple[EntityID, Tuple[T1, T2]]]]:
    ...


def typed_compiled_query(component_types, world=default_world):  # type: ignore
    query = Query(component_types, world).compile()

    def inner() -> Iterator[Tuple[EntityID, Tuple[Component, ...]]]:
        for entity_id, components in query:
            yield entity_id, tuple(components)

    return inner
