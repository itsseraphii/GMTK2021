import sys

TILE_SIZE = 32
PLAYER_SIZE = [32, 32]
PLAYER_HITBOX_SIZE = [20, 20]

try: # Path for files when the game is built by PyInstaller
    BASE_PATH = sys._MEIPASS
except:
    BASE_PATH = "."