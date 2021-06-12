import pygame
from game import Game

SIZE_X, SIZE_Y = 1600, 900

if (__name__ == "__main__"):
    screen = pygame.display.set_mode((SIZE_X, SIZE_Y))
    game = Game(screen)
    game.Run()