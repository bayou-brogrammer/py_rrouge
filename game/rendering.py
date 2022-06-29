from __future__ import annotations

import numpy as np
import tcod

import g
import game.color
import game.constants
import game.engine
import game.game_map
import game.render_functions
from game.tiles import tile_graphics


def render_map(console: tcod.Console, gamemap: game.game_map.GameMap) -> None:
    # The default graphics are of tiles that are visible.
    light = tile_graphics[gamemap.tiles]

    # Apply effects to create a darkened map of tile graphics.
    dark = gamemap.memory.copy()
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
    # Otherwise, the default graphic is "SHROUD".
    console.rgb[0 : gamemap.width, 0 : gamemap.height] = np.select(
        condlist=[visible, gamemap.explored],
        choicelist=[light, dark],
        default=dark,
    )

    for entity in sorted(gamemap.entities, key=lambda x: x.render_order.value):
        if not gamemap.visible[entity.x, entity.y]:
            continue  # Skip entities that are not in the FOV.
        console.print(entity.x, entity.y, entity.char, fg=entity.color)

    visible.choose((gamemap.memory, light), out=gamemap.memory)


def render_log(console: tcod.Console, engine: game.engine.Engine) -> None:
    game.render_functions.render_panel(
        console,
        x=game.constants.log_panel_x,
        y=game.constants.log_panel_y,
        width=game.constants.log_panel_width,
        height=game.constants.log_panel_height,
        title="Log",
        title_fg=game.color.yellow,
    )

    engine.message_log.render(
        console,
        x=game.constants.log_panel_x + 1,
        y=game.constants.log_panel_y + 1,
        width=game.constants.log_panel_width - 1,
        height=game.constants.log_panel_height - 2,
    )


def render_stats(console: tcod.Console, engine: game.engine.Engine) -> None:
    game.render_functions.render_panel(
        console,
        x=game.constants.stats_panel_x,
        y=game.constants.stats_panel_y,
        width=game.constants.stats_panel_width,
        height=game.constants.stats_panel_height,
        title="Stats",
        title_fg=game.color.yellow,
    )

    game.render_functions.render_bar(
        console=console,
        x=game.constants.stats_panel_x + 1,
        y=game.constants.stats_panel_y + 1,
        current_value=engine.player.fighter.hp,
        maximum_value=engine.player.fighter.max_hp,
        total_width=game.constants.stats_panel_width - 2,
    )


def render_ui(console: tcod.Console, engine: game.engine.Engine) -> None:
    # Log Panel.
    render_log(console=console, engine=engine)
    # Stats Panel
    render_stats(console=console, engine=engine)

    # Tooltips
    game.render_functions.render_names_at_mouse_location(console=console, engine=engine)
