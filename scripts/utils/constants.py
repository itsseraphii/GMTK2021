import sys
from utils.story import STORY

TILE_SIZE = 32
PLAYER_SIZE = [32, 32]
PLAYER_HITBOX_SIZE = [20, 20]

BLACK = (0, 0, 0)
MENU_BG_COLOR = (10, 10, 10)
LEVEL_BG_COLOR = (33, 33, 35)
TEXT_COLOR = (200, 200, 200)

ENDING_MENU_PAGE = len(STORY)

if (hasattr(sys, '_MEIPASS')): # Path for data when the game is built by PyInstaller
    DATA_PATH = sys._MEIPASS
else:
    DATA_PATH = "."