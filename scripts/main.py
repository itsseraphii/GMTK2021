import pygame
from pygame.constants import KEYDOWN, MOUSEBUTTONDOWN, QUIT, VIDEORESIZE
from utils.constants import DEFAULT_WINDOW_SIZE, DATA_PATH
from levelController import LevelController

if (__name__ == "__main__"):
    pygame.display.init()
    pygame.mixer.init()
    pygame.font.init()

    pygame.display.set_caption('Transgenesis')
    pygame.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONDOWN, VIDEORESIZE])
    
    screen = pygame.display.set_mode(DEFAULT_WINDOW_SIZE, pygame.RESIZABLE)
    pygame.display.set_icon(pygame.image.load(DATA_PATH + "/res/icon/icon.png"))
    
    LevelController(screen)

    pygame.quit()