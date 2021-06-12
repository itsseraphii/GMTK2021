import pygame
from pygame.constants import KEYDOWN, K_RETURN, QUIT
from background import Background
from entities.player import Player

FPS = 100

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screenSize = pygame.display.get_window_size()

        self.background = Background()
        self.fontH1 = pygame.font.Font("./ui/FreeSansBold.ttf", 45)
        
        self.player = Player(self.background)
        self.background.SetPlayer(self.player)

    def CheckInputs(self):
        for event in pygame.event.get():
            if (event.type == QUIT):
                self.running =  False

            elif (event.type == KEYDOWN):
                if (event.key == K_RETURN and not self.playing):
                    self.startTime = pygame.time.get_ticks()
                    self.playing = True

        if (self.playing):
            pressedKeys = pygame.key.get_pressed()
            self.player.Move(pressedKeys)

            mouseX, mouseY = pygame.mouse.get_pos()
            self.player.LookAtMouse(mouseX, mouseY)

            if (pygame.mouse.get_pressed()[0]):
                self.player.Attack()

    def DrawTimeLeft(self):
        if (self.playing):
            self.screen.blit(self.fontH1.render("Time left: " + str(int((61000 - pygame.time.get_ticks() + self.startTime) / 1000)), True, (0, 0, 0)), (10, 10))
        elif (self.gameOver):
            self.screen.blit(self.fontH1.render("Game over", True, (0, 0, 0)), (10, 10))
        else:
            self.screen.blit(self.fontH1.render("Press Enter to start", True, (0, 0, 0)), (10, 10))

    def Draw(self):
        self.background.Draw(self.screen)
        self.player.Draw(self.screen)
        self.DrawTimeLeft()
        pygame.display.update()

    def Run(self):
        self.running = True
        self.playing = False
        self.gameOver = False
        
        clock = pygame.time.Clock()

        while (self.running):
            self.CheckInputs()
            self.Draw()

            if (self.playing and not self.gameOver and pygame.time.get_ticks() - self.startTime > 61000):
                self.playing = False
                self.gameOver = True

            clock.tick(FPS)