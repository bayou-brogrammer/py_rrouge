from __future__ import annotations

from typing import Tuple

import tcod

import game.color
import game.engine
import game.gamemap
from game import ecs
from game.components import Name, Position, Renderable

ENTITY_SEARCH_QUERY = ecs.typed_compiled_query((Position, Renderable, Name))


def get_names_at_location(x: int, y: int, gamemap: game.gamemap.GameMap) -> str | None:
    if not gamemap.in_bounds(x, y) or not gamemap.visible[x, y]:
        return None

    entities_at_location = list(
        filter(lambda entity: entity[-1][0].x == x and entity[-1][0].y == y, ENTITY_SEARCH_QUERY())
    )
    if len(entities_at_location) == 0:
        return None

    names = ", ".join(entity[-1][-1].name for entity in entities_at_location)
    return names.capitalize()


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


def render_names_at_mouse_location(console: tcod.Console, x: int, y: int, engine: game.engine.Engine) -> None:
    mouse_x, mouse_y = engine.mouse_location

    names_at_mouse_location = get_names_at_location(x=mouse_x, y=mouse_y, gamemap=engine.gamemap)
    if names_at_mouse_location is None:
        return

    if mouse_x > 40:  # display to the right
        x = mouse_x - len(names_at_mouse_location) - 2
        text = f"{names_at_mouse_location}->"
    else:
        x = mouse_x + 1
        text = f"<-{names_at_mouse_location}"

    console.print(x=x, y=mouse_y, string=text, fg=game.color.white, bg=game.color.black)
