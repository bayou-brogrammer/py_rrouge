from __future__ import annotations

import numpy as np
import tcod

import g
from game import gamemap
from game.tiles import tile_graphics


def render_map(console: tcod.Console, gamemap: gamemap.GameMap) -> None:
    """Draw Map"""
    gamemap = g.engine.gamemap

    # The default graphics are of tiles that are visible.
    light = tile_graphics[gamemap.tiles]

    # Apply effects to create a darkened map of tile graphics.
    dark = gamemap.memory.copy()
    # dark = light.copy()
    dark["fg"] //= 2
    dark["bg"] //= 8

    visible = gamemap.visible
    if g.fullbright:
        visible = np.ones_like(visible)

    for entity in sorted(gamemap.entities, key=lambda x: x.render_order.value):
        if not visible[entity.x, entity.y]:
            continue  # Skip entities that are not in the FOV.
        light[entity.x, entity.y]["ch"] = ord(entity.char)
        light[entity.x, entity.y]["fg"] = entity.color

    # If a tile is in the "visible" array, then draw it with the "light" colors.
    # If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
    # Otherwise, the default graphic is "dark".
    console.rgb[0 : gamemap.width, 0 : gamemap.height] = np.select(
        condlist=[visible, gamemap.explored],
        choicelist=[light, dark],
        default=dark,
    )

    for entity in sorted(gamemap.entities, key=lambda x: x.render_order.value):
        if not visible[entity.x, entity.y]:
            continue  # Skip entities that are not in the FOV.
        console.print(entity.x, entity.y, entity.char, fg=entity.color)

    visible.choose((gamemap.memory, light), out=gamemap.memory)
