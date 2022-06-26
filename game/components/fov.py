import numpy as np
from numpy.typing import NDArray
from snecs import RegisteredComponent

from game.gamemap import GameMap


class FieldOfView(RegisteredComponent):
    radius: int
    visible: NDArray[np.bool_]
    dirty: bool

    def __init__(self, gamemap: GameMap, radius: int):
        self.dirty = True
        self.radius = radius
        self.visible = self.visible = np.full((gamemap.width, gamemap.height), fill_value=False, order="F")
