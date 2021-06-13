import pygame
from game import Game

SIZE = (1280, 720)

if (__name__ == "__main__"):
    pygame.init()
    pygame.display.set_caption('Transgenesis')
    screen = pygame.display.set_mode((SIZE[0], SIZE[1]))
    Game(screen, 0)