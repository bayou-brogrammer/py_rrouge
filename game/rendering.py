from __future__ import annotations

import numpy as np
import tcod

import g
from game import ecs
from game.components.position import Position
from game.components.renderable import Renderable
from game.tiles import tile_graphics

# RENDERABLE_QUERY = Query([Position, Renderable]).compile()


# class Renderer(Node):
#     """Creates the main rendering root console with the tileset, and manages the rendering
#     between the different console panels.
#     """

#     root: tcod.Console

#     def __init__(self) -> None:
#         super().__init__()
#         self.root = g.console

#     def clear(self) -> None:
#         self.root.clear()

#     def render(self) -> None:
#         """Render method [Must be overridden by subclasses]"""
#         raise NotImplementedError()


# class MainMenuRenderer(Renderer):
#     # Load the background image.  Pillow returns an object convertable into a NumPy array.
#     background_image = Image.open(Path(settings.bg_img))

#     def __init__(self) -> None:
#         super().__init__()

#     def render(self) -> None:
# self.root.draw_semigraphics(self.background_image, 0, 0)

# self.root.print(
#     self.root.width // 2,
#     self.root.height // 2 - 4,
#     settings.title_extended,
#     fg=game.color.menu_title,
#     alignment=tcod.CENTER,
# )
# self.root.print(
#     self.root.width // 2,
#     self.root.height - 2,
#     f"By {settings.author}",
#     fg=game.color.menu_title,
#     alignment=tcod.CENTER,
# )

# for i, text in enumerate(["[N] Play a new game", "[C] Continue last game", "[Q] Quit"]):
#     self.root.print(
#         self.root.width // 2,
#         self.root.height // 2 - 2 + i,
#         text.ljust(settings.menu_width),
#         fg=game.color.menu_text,
#         bg=game.color.black,
#         alignment=tcod.CENTER,
#         bg_blend=tcod.BKGND_ALPHA(64),
#     )


# class MainRenderer(Renderer):
#     def __init__(self) -> None:
#         super().__init__()

#         self.map_panel = tcod.Console(settings.map_panel_width, settings.map_height, order="F")
#         self.log_panel = tcod.Console(settings.screen_width, settings.log_panel_height, order="F")
#         self.stats_panel = tcod.Console(settings.stats_panel_width, settings.stats_panel_height, order="F")

# def __render_map__(self, console: tcod.Console) -> None:
#     """Draw Map"""
#     gamemap = g.engine.gamemap

#     # The default graphics are of tiles that are visible.
#     light = tile_graphics[gamemap.tiles]

#     # Apply effects to create a darkened map of tile graphics.
#     dark = light.copy()
#     dark["fg"] //= 2
#     dark["bg"] //= 8

#     # If a tile is in the "visible" array, then draw it with the "light" colors.
#     # If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
#     # Otherwise, the default graphic is "SHROUD".
#     console.rgb[0 : gamemap.width, 0 : gamemap.height] = np.select(
#         condlist=[gamemap.visible, gamemap.explored],
#         choicelist=[light, dark],
#         default=light,
#         # default=SHROUD,
#     )

# def __render_entities__(self, console: tcod.Console) -> None:
#     p: Position
#     r: Renderable
#     for _, (p, r) in RENDERABLE_QUERY:  # type: ignore
#         console.print(p.x, p.y, r.char, r.color)

#     def render(self) -> None:
#         self.__render_map__(self.map_panel)
#         self.__render_entities__(self.map_panel)

#         # Blit consoles onto root console
#         self.map_panel.blit(self.root, 0, 0)

#         # Clear Map Console
#         self.map_panel.clear()


RENDERABLE_QUERY = ecs.typed_compiled_query((Position, Renderable))


def render_map(console: tcod.Console) -> None:
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

    for _, (p, r) in sorted(RENDERABLE_QUERY(), key=lambda x: x[1][1].render_order.value):
        if not visible[p.x, p.y]:
            continue  # Skip entities that are not in the FOV.
        light[p.x, p.y]["ch"] = ord(r.char)
        light[p.x, p.y]["fg"] = r.color

    # If a tile is in the "visible" array, then draw it with the "light" colors.
    # If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
    # Otherwise, the default graphic is "dark".
    console.rgb[0 : gamemap.width, 0 : gamemap.height] = np.select(
        condlist=[visible, gamemap.explored],
        choicelist=[light, dark],
        default=dark,
    )

    for _, (p, r) in sorted(RENDERABLE_QUERY(), key=lambda x: x[-1][-1].render_order.value):
        if not visible[p.x, p.y]:
            continue  # Skip entities that are not in the FOV.
        console.print(p.x, p.y, r.char, r.color)

    visible.choose((gamemap.memory, light), out=gamemap.memory)
