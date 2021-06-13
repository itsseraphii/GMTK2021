import pygame
from game import Game
import sys

SIZE = (1600, 900)

try: # Path for files when app is built by PyInstaller
    BASE_PATH = sys._MEIPASS
except:
    BASE_PATH = "."

if (__name__ == "__main__"):
    pygame.init()
    pygame.display.set_caption('60 seconds')
    screen = pygame.display.set_mode((SIZE[0], SIZE[1]))
    game = Game(screen)
    game.Run()