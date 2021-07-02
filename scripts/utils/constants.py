import os
import sys
from utils.story import STORY

DEFAULT_WINDOW_SIZE = (1280, 720)

TILE_SIZE = 32
PLAYER_SIZE = [32, 32]
PLAYER_HITBOX_SIZE = [20, 20]

WEAPON_IMAGE_SIZE = [32, 15]

BLACK = (0, 0, 0)
MENU_BG_COLOR = (10, 10, 10)
LEVEL_BG_COLOR = (33, 33, 35)
TEXT_COLOR = (200, 200, 200)

CREDITS_PAGE = len(STORY)

if (hasattr(sys, '_MEIPASS')): # Path for data when the game is built by PyInstaller
    DATA_PATH = sys._MEIPASS
else:
    DATA_PATH = "."

SAVE_PATH = os.getenv('APPDATA') + "\\Transgenesis\\save.dat"

# Very unsecure, but still prevents the average gamer from editing his save file
SAVE_KEY = b"mNixSeRoW1JXa27N4F2VR8vttF82yqtSSeQAI_nrTPo="