from typing import Tuple

from snecs import RegisteredComponent

from game.render_order import RenderOrder


class Renderable(RegisteredComponent):
    def __init__(self, char: str, color: Tuple[int, int, int], render_order: RenderOrder = RenderOrder.ACTOR) -> None:
        self.char = char
        self.color = color
        self.render_order = render_order
