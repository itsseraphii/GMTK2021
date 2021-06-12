import pygame
from game import Game

SIZE = (1600, 900)

if (__name__ == "__main__"):
    pygame.init()
    pygame.display.set_caption('60 seconds')
    screen = pygame.display.set_mode((SIZE[0], SIZE[1]))
    game = Game(screen)
    game.Run()