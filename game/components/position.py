from typing import Iterator

from snecs import RegisteredComponent


class Position(RegisteredComponent):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __iter__(self) -> Iterator[int]:
        return iter([self.x, self.y])

    # def move(self, x: int, y: int) -> None:
    # self.x = x
    # self.y = y
