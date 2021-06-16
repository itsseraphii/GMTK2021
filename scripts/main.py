import pygame
from game import Game

DEFAULT_WINDOW_SIZE = (1280, 720)

if (__name__ == "__main__"):
    pygame.init()
    pygame.display.set_caption('Transgenesis')
    screen = pygame.display.set_mode(DEFAULT_WINDOW_SIZE, pygame.RESIZABLE)
    Game(screen, 0)
    
    # comment debug info