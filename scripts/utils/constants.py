import sys

TILE_SIZE = 32

try: # Path for files when app is built by PyInstaller
    BASE_PATH = sys._MEIPASS
except:
    BASE_PATH = "."