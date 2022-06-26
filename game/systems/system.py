from __future__ import annotations

from typing import Callable, Generic, Iterator, Tuple, TypeVar, get_args, get_origin

from snecs.typedefs import EntityID

from game.query import typed_compiled_query

T = TypeVar("T")
C = TypeVar("C")


class System(Generic[T, C]):
    components: T
    return_type: C
    compiled_query: Callable[[], Iterator[C]]

    def __init_subclass__(cls) -> None:
        for base in cls.__orig_bases__:  # type: ignore
            if get_origin(base) == System:
                _, component_types_tuple_type = get_args(base)
                component_types = get_args(component_types_tuple_type)
                cls.components = component_types
                cls.compiled_query = typed_compiled_query(component_types)  # type: ignore
                return

    def query(self) -> Iterator[Tuple[EntityID, C]]:
        return self.__class__.compiled_query()

    def process(self) -> None:
        raise NotImplementedError()
