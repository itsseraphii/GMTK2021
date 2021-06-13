import pygame
from pygame.constants import KEYDOWN, K_RETURN, MOUSEBUTTONDOWN, QUIT
from gameworld import GameWorld, TILE_SIZE
from entities.player import Player

FPS = 100

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screenSize = pygame.display.get_window_size()

        self.gameworld = GameWorld()
        self.player = Player(self.gameworld)
        self.gameworld.SetPlayer(self.player)

        self.fontGiant = pygame.font.Font("./fonts/FreeSansBold.ttf", 60)
        self.fontLarge = pygame.font.Font("./fonts/FreeSansBold.ttf", 45)
        self.fontMedium = pygame.font.Font("./fonts/FreeSansBold.ttf", 25)
        self.fontSmall = pygame.font.Font("./fonts/FreeSansBold.ttf", 15)

        self.menuPage = 0

    def StartMenuMusic(self):
        pygame.mixer.music.fadeout # Fade out last music
        pygame.mixer.music.load("./music/Main_theme_v2_loopable.mp3") # Start menu music
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(-1) # Loop forever

    def StartLevelMusic(self):
        pygame.mixer.music.fadeout  # Fade out last music
        pygame.mixer.music.load("./music/level_theme_v2.mp3") # Start level music
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play() # play once

    def CheckInputs(self):
        for event in pygame.event.get():
            if (event.type == QUIT):
                self.running =  False

            elif (event.type == KEYDOWN):
                if (event.key == K_RETURN and not self.playing):
                    if (self.menuPage < 1):
                        self.menuPage += 1
                    else:
                        self.startTime = pygame.time.get_ticks()
                        self.playing = True
                        self.StartLevelMusic()

            elif (self.playing and event.type == MOUSEBUTTONDOWN):
                if (event.button == 4): # Mouse wheel up
                    self.player.SwitchWeapon(False)
                elif event.button == 5: # Mouse wheel down
                    self.player.SwitchWeapon(True)

        if (self.playing):
            pressedKeys = pygame.key.get_pressed()
            self.player.Move(pressedKeys)

            mouseX, mouseY = pygame.mouse.get_pos()
            self.player.LookAtMouse(mouseX, mouseY)

            if (pygame.mouse.get_pressed()[0]):
                self.player.Attack()

    def DrawTimeLeft(self):
        if (self.playing):
            msLeft = int(60000 - pygame.time.get_ticks() + self.startTime)
            self.screen.blit(self.fontLarge.render("Time left: " + str(round(msLeft / 1000, 2)), True, (0, 0, 0)), (10, 10))
        elif (self.gameOver):
            self.screen.blit(self.fontLarge.render("Game over", True, (0, 0, 0)), (10, 10))

    def DrawProgress(self):
        percentComplete = min(100, round((self.gameworld.backgroundSize[1] - (self.gameworld.middleY * TILE_SIZE)) / self.gameworld.backgroundSize[1] * 100, 1))
        self.screen.blit(self.fontLarge.render("Progress: " + str(percentComplete) + "%", True, (0, 0, 0)), (self.screenSize[0] - 360, 10))

    def DrawUI(self):
        self.DrawTimeLeft()
        self.DrawProgress()
        self.screen.blit(self.fontMedium.render("Equipped: " + str(self.player.weaponInventory[self.player.equippedWeaponIndex]), True, (0, 0, 0)), (10, self.screenSize[1] - 70))
        self.screen.blit(self.fontMedium.render("Ammo: " + str(self.player.ammo), True, (0, 0, 0)), (10, self.screenSize[1] - 40))

    def DrawMenu(self):
        if (self.menuPage == 0):
            text = self.fontMedium.render("TODO put story here", True, (200, 200, 200))
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] / 3 + 30))
            self.screen.blit(text, textRect)

            text = self.fontMedium.render("Press Enter to continue", True, (200, 200, 200))
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] - 30))
            self.screen.blit(text, textRect)

        else:
            text = self.fontGiant.render("Beeg Game Name", True, (200, 200, 200))
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] / 2))
            self.screen.blit(text, textRect)

            text = self.fontMedium.render("Press Enter to start", True, (200, 200, 200))
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] - 30))
            self.screen.blit(text, textRect)

    def Draw(self):
        if (self.playing):
            self.gameworld.Draw(self.screen)
            self.player.Draw(self.screen)
            self.DrawUI()

            for monsterId in self.gameworld.monsters:
                self.gameworld.monsters[monsterId].Draw(self.screen)
        
            self.DrawTimeLeft()

        else:
            self.screen.fill((0, 0, 0))
            self.DrawMenu()

        pygame.display.update()

    def UpdateAI(self):
        for monsterId in self.gameworld.monsters:
            self.gameworld.monsters[monsterId].Move()

    def Run(self):
        self.running = True
        self.playing = False
        self.gameOver = False
        
        clock = pygame.time.Clock()

        self.StartMenuMusic()

        while (self.running):
            self.CheckInputs()
            self.Draw()

            if (self.playing) :
                self.UpdateAI()

            if (self.playing and not self.gameOver and pygame.time.get_ticks() - self.startTime > 60000):
                self.playing = False
                self.gameOver = True
                self.StartMenuMusic()

            clock.tick(FPS)