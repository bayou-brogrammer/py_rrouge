from __future__ import annotations

from enum import Enum
from typing import Any

import numpy as np
import tcod
from numpy.typing import NDArray


class TileType(Enum):
    WALL = 0
    FLOOR = 1
    DOWN_STAIRS = 2


tile_graphics: NDArray[Any] = np.array(
    [
        (ord("#"), (0x80, 0x80, 0x80), (0x40, 0x40, 0x40)),  # wall
        (ord("."), (0x40, 0x40, 0x40), (0x18, 0x18, 0x18)),  # floor
        (ord(">"), (0xFF, 0xFF, 0xFF), (0x18, 0x18, 0x18)),  # down stairs
    ],
    dtype=tcod.console.rgb_graphic,
)
