import pygame
from pygame.constants import QUIT
from player import Player

FPS = 100

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player()

    def CheckInputs(self):
        for event in pygame.event.get():
            if (event.type == QUIT):
                self.running =  False

        pressedKeys = pygame.key.get_pressed()
        self.player.Move(pressedKeys)

        mouseX, mouseY = pygame.mouse.get_pos()
        self.player.LookAtMouse(mouseX, mouseY)

    def Draw(self):
        self.screen.fill((31, 31, 31))
        self.player.Draw(self.screen)
        pygame.display.update()

    def Run(self):
        self.running = True
        clock = pygame.time.Clock()

        while (self.running):
            self.CheckInputs()

            self.Draw()

            clock.tick(FPS)