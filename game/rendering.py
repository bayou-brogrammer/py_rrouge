from __future__ import annotations

from typing import Optional, Tuple

import numpy as np
import tcod

import g
import game.color
import game.engine
import game.game_map
from game import constants
from game.tiles import tile_graphics
from game.typing import Color_Type


class Renderer:
    """Class to handle rendering for handlers"""

    def render(self, root_console: tcod.Console) -> None:
        """Render loop for handler"""
        raise NotImplementedError()

    def render_panel(
        self,
        console: tcod.Console,
        x: int,
        y: int,
        width: int,
        height: int,
        *,
        title: Optional[str],
        frame_fg: Optional[Color_Type] = None,
        frame_bg: Optional[Color_Type] = None,
        title_fg: Optional[Color_Type] = None,
        title_bg: Optional[Color_Type] = None,
    ) -> None:
        console.draw_frame(x=x, y=y, width=width, height=height, fg=frame_fg, bg=frame_bg)

        if title:
            console.print(x=x + 1, y=y, string=title, fg=title_fg, bg=title_bg)

    def render_bar(
        self,
        console: tcod.Console,
        current_value: int,
        maximum_value: int,
        total_width: int,
        *,
        x: int,
        y: int,
    ) -> None:
        bar_width = int(float(current_value) / maximum_value * total_width)
        console.draw_rect(x=x, y=y, width=total_width, height=1, ch=1, bg=game.color.bar_empty)

        if bar_width > 0:
            console.draw_rect(x=x, y=y, width=bar_width, height=1, ch=1, bg=game.color.bar_filled)

        console.print(x=x, y=y, string=f" HP: {current_value}/{maximum_value}", fg=game.color.bar_text)


class GameRenderer(Renderer):
    """Renderer for main game handler"""

    map_console: tcod.Console = tcod.Console(constants.screen_width, constants.screen_height, order="F")
    stats_console: tcod.Console = tcod.Console(constants.screen_width, constants.screen_height, order="F")
    log_console: tcod.Console = tcod.Console(constants.log_panel_width, constants.log_panel_height, order="F")

    def render_tooltips(self, console: tcod.Console) -> None:
        mouse_x, mouse_y = g.engine.mouse_location
        names_at_mouse_location = g.engine.gamemap.get_names_at_location(x=mouse_x, y=mouse_y)

        if names_at_mouse_location is None:
            return

        x = mouse_x + 1
        tooltip_str = f"<-{names_at_mouse_location}"
        if x > constants.screen_width // 2:
            x -= len(names_at_mouse_location) + 3
            tooltip_str = f"{names_at_mouse_location}->"

        console.print(x=x, y=mouse_y, string=tooltip_str, fg=game.color.white)

    def render_dungeon_level(self, console: tcod.Console, dungeon_level: int, location: Tuple[int, int]) -> None:
        """
        Render the level the player is currently on, at the given location.
        """
        x, y = location
        console.print(x=x, y=y, string=f"Dungeon level: {dungeon_level}")

    def render_map(self, root_console: tcod.Console) -> None:
        gamemap = g.engine.gamemap

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
        root_console.rgb[0 : gamemap.width, 0 : gamemap.height] = np.select(
            condlist=[visible, gamemap.explored],
            choicelist=[light, dark],
            default=dark,
        )

        for entity in sorted(gamemap.entities, key=lambda x: x.render_order.value):
            if not gamemap.visible[entity.x, entity.y]:
                continue  # Skip entities that are not in the FOV.
            root_console.print(entity.x, entity.y, entity.char, fg=entity.color)

        visible.choose((gamemap.memory, light), out=gamemap.memory)

    def render_stats(self, console: tcod.Console) -> None:
        self.render_panel(
            console,
            x=0,
            y=0,
            width=constants.stats_panel_width,
            height=constants.stats_panel_height,
            title="Stats",
            title_fg=game.color.yellow,
        )

        self.render_bar(
            console=console,
            x=1,
            y=1,
            current_value=g.engine.player.fighter.hp,
            maximum_value=g.engine.player.fighter.max_hp,
            total_width=constants.stats_panel_width - 2,
        )

    def render_log(self, console: tcod.Console) -> None:
        self.render_panel(
            console,
            x=0,
            y=0,
            width=constants.log_panel_width,
            height=constants.log_panel_height,
            title="Log",
            title_fg=game.color.yellow,
        )

        g.engine.message_log.render(
            console,
            x=1,
            y=1,
            width=constants.log_panel_width - 1,
            height=constants.log_panel_height - 2,
        )

    def render_ui(self, root_console: tcod.Console) -> None:
        # Log Panel.
        self.render_log(self.log_console)
        # Stats Panel
        self.render_stats(self.stats_console)
        # Tooltips
        self.render_tooltips(root_console)

        self.log_console.blit(root_console, constants.log_panel_x, constants.log_panel_y)
        self.stats_console.blit(root_console, constants.stats_panel_x, constants.stats_panel_y)

    def render(self, root_console: tcod.Console) -> None:
        self.render_map(root_console)
        self.render_ui(root_console)


class InventoryRenderer(GameRenderer):
    """Renderer for inventory handler"""

    TITLE = "<missing title>"

    def render_inventory(self, console: tcod.Console) -> None:
        """Render an inventory menu, which displays the items in the inventory, and the letter to select them.
        Will move to a different position based on where the player is located, so the player can always see where
        they are.
        """

        number_of_items_in_inventory = len(g.engine.player.inventory.items)
        height = number_of_items_in_inventory + 2

        if height <= 3:
            height = 3

        width = len(self.TITLE) + 4
        x = game.constants.inventory_panel_x - width // 2
        y = game.constants.inventory_panel_y

        self.render_panel(
            console,
            x,
            y,
            width,
            height,
            title=f" {self.TITLE} ",
            title_fg=(0, 0, 0),
            title_bg=(255, 255, 255),
        )

        if number_of_items_in_inventory > 0:
            for i, item in enumerate(g.engine.player.inventory.items):
                item_key = chr(ord("a") + i)

                # is_equipped = g.engine.player.equipment.item_is_equipped(item)

                item_string = f"({item_key}) {item.name}"

                # if is_equipped:
                #     item_string = f"{item_string} (E)"

                console.print(x + 1, y + i + 1, item_string)
        else:
            console.print(x + width // 2, y + 1, "[Empty]", fg=game.color.error, alignment=tcod.constants.CENTER)

    def render(self, root_console: tcod.Console) -> None:
        super().render(root_console)
        self.render_inventory(root_console)
