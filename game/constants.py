from typing import Any

import numpy as np
import tcod
from numpy.typing import NDArray

# SHROUD represents unexplored, unseen tiles
SHROUD: NDArray[Any] = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=tcod.console.rgb_graphic)

""" Game Details Stuff """
author = "Jacob LeCoq"
version = 0.1
title = f"PyRRouge {version}"
title_extended = "<Insert Cool Title>: A Roguelike Venture!"

tileset = "data/16x16-RogueYun-AgmEdit.png"
tileset_rows = 16
tileset_columns = 16
tileset_bounds = (16, 16)  # (columns, rows)
charmap = tcod.tileset.CHARMAP_CP437
bg_img = "data/menu_background.png"
save_file = "savegame.sav"

""" Map Gen """
max_rooms = 30
room_min_size = 6
room_max_size = 10

""" Bounds """
# Screen
screen_width = 80
screen_height = 50
ui_width = 30

# Main Menu
menu_width = 24

""" Panels """
# Message Panel
log_panel_width = screen_width - 20
log_panel_height = 7
log_panel_x = 0
log_panel_y = screen_height - log_panel_height

# Side Panel
stats_panel_width = 20
stats_panel_height = screen_height
stats_panel_x = screen_width - stats_panel_width
stats_panel_y = 0

# Map Panel
map_width = 80 - stats_panel_width
map_height = 43
map_panel_width = 80 - stats_panel_width

# Inventory Panel
inventory_panel_x = map_width // 2
inventory_panel_y = map_height // 2
