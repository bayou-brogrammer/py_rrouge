from __future__ import annotations

from typing import Optional, Tuple

import tcod

import game.color
import game.constants
import game.engine
import game.entity
import game.game_map
from game.typing import Color_Type


def get_names_at_location(x: int, y: int, game_map: game.game_map.GameMap) -> Optional[str]:
    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return None

    entity_names_at_location = [e.name for e in game_map.entities_at_location(x, y, game.entity.Entity)]
    if len(entity_names_at_location) == 0:
        return None

    return ", ".join(sorted(n.capitalize() for n in entity_names_at_location))


def render_bar(
    console: tcod.Console, current_value: int, maximum_value: int, total_width: int, *, x: int, y: int
) -> None:
    bar_width = int(float(current_value) / maximum_value * total_width)

    console.draw_rect(x=x, y=y, width=total_width, height=1, ch=1, bg=game.color.bar_empty)

    if bar_width > 0:
        console.draw_rect(x=x, y=y, width=bar_width, height=1, ch=1, bg=game.color.bar_filled)

    console.print(x=x, y=y, string=f" HP: {current_value}/{maximum_value}", fg=game.color.bar_text)


def render_dungeon_level(console: tcod.Console, dungeon_level: int, location: Tuple[int, int]) -> None:
    """
    Render the level the player is currently on, at the given location.
    """
    x, y = location
    console.print(x=x, y=y, string=f"Dungeon level: {dungeon_level}")


def render_names_at_mouse_location(console: tcod.Console, engine: game.engine.Engine) -> None:
    mouse_x, mouse_y = engine.mouse_location
    names_at_mouse_location = get_names_at_location(x=mouse_x, y=mouse_y, game_map=engine.gamemap)

    if names_at_mouse_location is None:
        return

    x = mouse_x + 1
    tooltip_str = f"<-{names_at_mouse_location}"
    if x > game.constants.screen_width // 2:
        x -= len(names_at_mouse_location) + 3
        tooltip_str = f"{names_at_mouse_location}->"

    console.print(x=x, y=mouse_y, string=tooltip_str, fg=game.color.white)


def render_panel(
    console: tcod.Console,
    x: int,
    y: int,
    width: int,
    height: int,
    title: Optional[str],
    frame_fg: Optional[Color_Type] = None,
    frame_bg: Optional[Color_Type] = None,
    title_fg: Optional[Color_Type] = None,
    title_bg: Optional[Color_Type] = None,
) -> None:
    console.draw_frame(x=x, y=y, width=width, height=height, fg=frame_fg, bg=frame_bg)

    if title:
        console.print(x=x + 1, y=y, string=title, fg=title_fg, bg=title_bg)
