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

tileset = "data/dejavu16x16_gs_tc.png"
# tileset = "data/16x16-RogueYun-AgmEdit.png"
tileset_rows = 8
tileset_columns = 32
charmap = tcod.tileset.CHARMAP_TCOD
# charmap = tcod.tileset.CHARMAP_CP437
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

# Main Menu
menu_width = 24
ui_width = 30

""" Panels """
# Message Panel
log_panel_width = screen_width - 20
log_panel_height = 9
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
