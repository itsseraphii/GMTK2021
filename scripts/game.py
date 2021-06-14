from math import exp
import pygame
from pygame.constants import KEYDOWN, K_RETURN, K_n, K_r, MOUSEBUTTONDOWN, QUIT
from gameworld import GameWorld, TILE_SIZE
from entities.player import Player
import sys

FPS = 100
TEXT_COLOR = (200, 200, 200)
LEVEL_TIME = 60000 # 60 seconds

try: # Path for files when app is built by PyInstaller
    BASE_PATH = sys._MEIPASS
except:
    BASE_PATH = "."

MAIN_MUSIC = BASE_PATH + "/music/Main_theme_v2_loopable.mp3"
# Path for each level 
LEVELS_MUSIC = [BASE_PATH + "/music/level_theme_v2.mp3", BASE_PATH + "/music/level_theme_v2.mp3"]
TIME_OVER_MUSIC = BASE_PATH + "/music/everything_goes_to_shit_v1.mp3"

class Game:
    def __init__(self, screen, currentLevel, menuPage = -1):
        self.screen = screen
        self.screenSize = pygame.display.get_window_size()

        self.currentLevel = currentLevel
        self.gameworld = GameWorld(currentLevel)
        self.player = Player(self, self.gameworld)
        self.gameworld.SetPlayer(self.player)
        
        self.fontGiant = pygame.font.Font(BASE_PATH + "/fonts/melted.ttf", 150)
        self.fontLarge = pygame.font.Font(BASE_PATH + "/fonts/FreeSansBold.ttf", 45)
        self.fontLargeMelted = pygame.font.Font(BASE_PATH + "/fonts/melted.ttf", 50)
        self.fontMedium = pygame.font.Font(BASE_PATH + "/fonts/FreeSansBold.ttf", 25)
        self.fontSmall = pygame.font.Font(BASE_PATH + "/fonts/FreeSansBold.ttf", 15)

        self.menuPage = menuPage

        self.Run()

    def StartMenuMusic(self):
        pygame.mixer.music.fadeout # Fade out last music
        pygame.mixer.music.load(MAIN_MUSIC) # Start menu music
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(-1) # Loop forever

    def StartLevelMusic(self):
        pygame.mixer.music.fadeout  # Fade out last music
        pygame.mixer.music.load(LEVELS_MUSIC[self.currentLevel]) # Start level music
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play() # play once

    def StartTimeOverMusic(self):
        pygame.mixer.music.fadeout  # Fade out last music
        pygame.mixer.music.load(TIME_OVER_MUSIC) # Start level music
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play() # play once

    def CheckInputs(self):
        for event in pygame.event.get():
            if (event.type == QUIT):
                self.running =  False

            elif (event.type == KEYDOWN):
                if (event.key == K_RETURN and not self.playing):
                    if (self.menuPage != self.currentLevel):
                        self.menuPage += 1
                    else:
                        self.startTime = pygame.time.get_ticks()
                        self.playing = True
                        self.StartLevelMusic()

                elif (event.key == K_r and self.playing):
                    self.RestartCurrentLevel()

                elif (event.key == K_n and self.playing): # TODO remove
                    self.NextLevel()

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
            if (self.timeOver):
                self.screen.blit(self.fontLargeMelted.render("They're coming", True, TEXT_COLOR), (10, 10))
            else:
                msLeft = int(max(0, LEVEL_TIME - pygame.time.get_ticks() + self.startTime))
                self.screen.blit(self.fontLarge.render("Time left: " + str(round(msLeft / 1000, 2)), True, TEXT_COLOR), (10, 10))            

    def DrawProgress(self): # TODO
        var1 = self.gameworld.startMiddleY - self.gameworld.middleY
        var2 = self.gameworld.startMiddleY - self.gameworld.goalPosY

        percentComplete = var1 / var2 * 100
        #self.screen.blit(self.fontLarge.render("Progress: " + str(percentComplete) + "%", True, TEXT_COLOR), (self.screenSize[0] - 360, 10))

    def DrawUI(self):
        self.DrawTimeLeft()
        self.DrawProgress()
        self.screen.blit(self.fontMedium.render("Equipped: " + str(self.player.weaponInventory[self.player.equippedWeaponIndex]), True, TEXT_COLOR), (10, self.screenSize[1] - 70))
        self.screen.blit(self.fontMedium.render("Ammo: " + str(self.player.ammo), True, TEXT_COLOR), (10, self.screenSize[1] - 40))

    def DrawParagraph(self, allText):
        for i in range(len(allText)):
                text = self.fontMedium.render(allText[i], True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, (self.screenSize[1] / 4) + (i * 30)))
                self.screen.blit(text, textRect)

    def DrawMenu(self):
        if (self.menuPage == -1): # Start lore
            allText = ["The year is 2082, scientists have found a miracle cure to cancer.", " The treatment modifies DNA, forcing the cancerous cell to regenerate as an healthy cell.", "", "In hindsight, forcing cells to reboot had some... unforeseen consequences.", "", "The treatment forces ANY cell it infects to regenerate and then spread the modified DNA, transforming the", "organism into a melted goo of skin and muscles.", "", "Any physical contact with an amalgamates will turn you into one of those monsters.", "", "Be really careful out there survivor."]
            self.DrawParagraph(allText)
            text = self.fontMedium.render("Press Enter to continue", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] - 30))
            self.screen.blit(text, textRect)
        else:
            if (self.menuPage == 0): # Title screen (also level 1 screen)
                text = self.fontGiant.render("Transgenesis", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] / 2))
                self.screen.blit(text, textRect)

            elif (self.menuPage == 1): # Level 2 screen
                allText = ["Well... that was the last can.", "", "I need to go out for supplies.", "", "There has to be other survivors out there.", "There must be."]
                self.DrawParagraph(allText)

            elif (self.menuPage == 2): # Level 3 screen
                allText = ["--------------------------------ARCHIVE #002184--------------------------------", "July 3rd 2084                                 Agent Marshall", "", "Amalgamated organisms have demonstrated the ability to produce sounds", "that could be described as human speech.", "", "Different voices can be heard, sometimes alternating, sometimes in unison", "", "The experience is deeply disturbing and yet, fascinating.", "", "Further investigation is required.", "-----------------------------------------------------------------------------------------"]
                self.DrawParagraph(allText)

            elif (self.menuPage == 3): # Level 4 screen
                allText = [] # TODO
                self.DrawParagraph(allText)

            elif (self.menuPage == 4): # Level 5 screen
                allText = [] # TODO
                self.DrawParagraph(allText)

            text = self.fontMedium.render("Press Enter to start level " + str(self.currentLevel + 1), True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] - 30))
            self.screen.blit(text, textRect)

    def Draw(self):
        if (self.playing):
            self.gameworld.Draw(self.screen)
            self.player.Draw(self.screen)
            self.DrawUI()

            for monsterId in self.gameworld.monsters:
                self.gameworld.monsters[monsterId].Draw(self.screen)

            for collectableId in self.gameworld.collectables:
                self.gameworld.collectables[collectableId].Draw(self.screen)
        
            self.DrawTimeLeft()
        else:
            self.screen.fill((10, 10, 10))
            self.DrawMenu()

        pygame.display.update()

    def UpdateAI(self):
        for monsterId in self.gameworld.monsters:
            self.gameworld.monsters[monsterId].Move()

    def RestartCurrentLevel(self):
        self.__init__(self.screen, self.currentLevel, self.currentLevel)

    def NextLevel(self):
        nextLevel = self.currentLevel + 1
        self.__init__(self.screen, nextLevel, nextLevel)

    def TriggerGameOver(self, victory):
        self.gameOver = True

        if (victory):
            self.NextLevel()
        else:
            self.RestartCurrentLevel()

    def Run(self):
        self.running = True # True while game is not exited
        self.playing = False # True while a level is beeing played
        self.timeOver = False # True while a level is beeing played and the 60 seconds are over
        self.gameOver = False # True when the level is over
        
        clock = pygame.time.Clock()

        self.StartMenuMusic()

        while (self.running):
            self.CheckInputs()
            self.Draw()

            if (self.playing) :
                self.UpdateAI()

            if (self.playing and not self.timeOver and pygame.time.get_ticks() - self.startTime > LEVEL_TIME):
                self.timeOver = True
                self.gameworld.SpawnTimeOverEnemies()
                self.StartTimeOverMusic()

            clock.tick(FPS)