import pygame
from pygame.constants import KEYDOWN, MOUSEBUTTONDOWN, QUIT, VIDEORESIZE
from utils.constants import DEFAULT_WINDOW_SIZE
from levelController import LevelController

if (__name__ == "__main__"):
    pygame.init()
    pygame.display.set_caption('Transgenesis')
    pygame.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONDOWN, VIDEORESIZE])
    
    screen = pygame.display.set_mode(DEFAULT_WINDOW_SIZE, pygame.RESIZABLE)
    
    LevelController(screen)

    pygame.quit()