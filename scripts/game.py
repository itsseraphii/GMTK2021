import pygame
from pygame.constants import KEYDOWN, K_RETURN, K_n, K_r, MOUSEBUTTONDOWN, QUIT
from gameworld import GameWorld, TILE_SIZE
from entities.player import Player
from story import STORY
import sys

MENU_FPS = 30
LEVEL_FPS = 100

LEVEL_TIME = 60000 # 60 seconds

BLACK = (0, 0, 0)
MENU_BG_COLOR = (10, 10, 10)
LEVEL_BG_COLOR = (33, 33, 35)
TEXT_COLOR = (200, 200, 200)

try: # Path for files when app is built by PyInstaller
    BASE_PATH = sys._MEIPASS
except:
    BASE_PATH = "."

MAIN_MUSIC = BASE_PATH + "/music/Main_theme_v2_loopable.mp3"
# Path for each level 
LEVELS_MUSIC = [BASE_PATH + "/music/level_theme_v2.mp3", BASE_PATH + "/music/level_theme_v2.mp3", BASE_PATH + "/music/level_theme_v2.mp3"]
TIME_OVER_MUSIC = BASE_PATH + "/music/everything_goes_to_shit_v1.mp3"

class Game:
    def __init__(self, screen, currentLevel, menuPage = -1):
        self.screen = screen
        self.screenSize = pygame.display.get_window_size()
        self.SetResizeAllowed(True)

        self.clock = pygame.time.Clock()
        self.fps = MENU_FPS

        self.menuPage = menuPage
        self.currentLevel = currentLevel
        
        self.gameworld = GameWorld(currentLevel)
        self.player = Player(self, self.gameworld)
        self.gameworld.SetPlayer(self.player)

        self.InitUI()
        
        self.Run()

    def InitUI(self):
        self.goalPosY = self.gameworld.FindGoalPosY() + 1 # +1 to see the end of the progress bar before touching the goal
        self.startMiddleY = (self.gameworld.backgroundSize[1] - (self.gameworld.offsetY - self.gameworld.startOffsetY) - (self.screenSize[1] / 2)) / TILE_SIZE
        self.lastProgressHeight = 1000000 # Forces first progress drawing
        self.progressBarBackground = pygame.Rect(self.screenSize[0] - 25, 10, 15, self.screenSize[1] - 20)
        self.progressRatio = (self.screenSize[1] - 20) / -(self.goalPosY - self.startMiddleY)

        self.fontTitle = pygame.font.Font(BASE_PATH + "/fonts/melted.ttf", int(self.screenSize[0] / 8))
        self.fontLarge = pygame.font.Font(BASE_PATH + "/fonts/FreeSansBold.ttf", 45)
        self.fontLargeMelted = pygame.font.Font(BASE_PATH + "/fonts/melted.ttf", 50)
        self.fontMedium = pygame.font.Font(BASE_PATH + "/fonts/FreeSansBold.ttf", 25)

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

            elif (event.type == pygame.VIDEORESIZE): # Can only resize in menus (between levels)
                self.screenSize = [max(1280, event.w), max(720, event.h)]
                self.screen = pygame.display.set_mode((self.screenSize[0], self.screenSize[1]), pygame.RESIZABLE)
                self.RestartLevel()

            elif (event.type == KEYDOWN):
                if (event.key == K_RETURN and not self.playing):
                    if (self.menuPage != self.currentLevel):
                        self.menuPage += 1
                        self.fps = MENU_FPS

                    else: # Start of a level
                        self.SetResizeAllowed(False)
                        self.fps = LEVEL_FPS
                        self.startTime = pygame.time.get_ticks()
                        self.playing = True
                        self.StartLevelMusic()
                        self.screen.fill(LEVEL_BG_COLOR)
                        pygame.draw.rect(self.screen, BLACK, self.progressBarBackground)

                elif (event.key == K_r and self.playing):
                    self.RestartLevel()

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

    def SetResizeAllowed(self, allowed):
        if (allowed):
            self.screen = pygame.display.set_mode((self.screenSize[0], self.screenSize[1]), pygame.RESIZABLE)
        else:
            self.screen = pygame.display.set_mode((self.screenSize[0], self.screenSize[1]))

    def DrawTimeLeft(self):
        if (self.playing):
            if (self.timeOver):
                self.screen.blit(self.fontLargeMelted.render("They're coming", True, TEXT_COLOR, LEVEL_BG_COLOR), (10, 10))
            else:
                msLeft = int(max(0, LEVEL_TIME - pygame.time.get_ticks() + self.startTime))
                self.screen.blit(self.fontLarge.render("Time left: " + str(round(msLeft / 1000, 1)), True, TEXT_COLOR, LEVEL_BG_COLOR), (10, 10))            

    def DrawProgress(self):
        currentPos = self.gameworld.middleY - self.startMiddleY
        newProgressHeight = int(max(13, currentPos * self.progressRatio + self.screenSize[1] - 14))

        if (newProgressHeight < self.lastProgressHeight): # Player has progressed
            self.lastProgressHeight = newProgressHeight
            progressBarForeground = pygame.Rect(self.screenSize[0] - 22, newProgressHeight, 9, min(self.screenSize[1] - 26, 1))
            pygame.draw.rect(self.screen, TEXT_COLOR, progressBarForeground)

    def DrawUI(self):
        self.DrawTimeLeft()
        self.DrawProgress()
        pygame.draw.rect(self.screen, LEVEL_BG_COLOR, pygame.Rect((10, self.screenSize[1] - 70), (300, 60))) # Cover last frame's text
        self.screen.blit(self.fontMedium.render("Equipped: " + str(self.player.weaponInventory[self.player.equippedWeaponIndex]), True, TEXT_COLOR), (10, self.screenSize[1] - 70))
        self.screen.blit(self.fontMedium.render("Ammo: " + str(self.player.ammo), True, TEXT_COLOR), (10, self.screenSize[1] - 40))

        '''# Debug info - Uncomment to show fps average over the last 10 frames
        fps = round(self.clock.get_fps(), 2)

        if (fps < 80):
            fpsColor = (255, 0, 0)
        elif (fps < 90):
            fpsColor = (255, 255, 0)
        else:
            fpsColor = (0, 255, 0)

        self.screen.blit(self.fontMedium.render("FPS: " + str(fps), True, fpsColor, LEVEL_BG_COLOR), (10, self.screenSize[1] / 2))'''

    def DrawParagraph(self, allText):
        for i in range(len(allText)):
                text = self.fontMedium.render(allText[i], True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, (self.screenSize[1] / 4) + (i * 30)))
                self.screen.blit(text, textRect)

    def DrawMenu(self):
        self.screen.fill(MENU_BG_COLOR)

        if (self.menuPage == -1): # Start lore
            self.DrawParagraph(STORY[self.menuPage])
            text = self.fontMedium.render("Press Enter to continue", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] - 30))
            self.screen.blit(text, textRect)
        
        else:
            text = self.fontMedium.render("Press Enter to start level " + str(self.currentLevel + 1), True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] - 30))
            self.screen.blit(text, textRect)

            if (self.menuPage == 0): # Title page (level 1)
                text = self.fontTitle.render("Transgenesis", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] / 2))
                self.screen.blit(text, textRect)

            else: # Story for each other level
                self.DrawParagraph(STORY[self.menuPage])

    def Draw(self):
        if (self.playing):
            self.gameworld.Draw(self.screen)

            for collectableId in self.gameworld.collectables:
                self.gameworld.collectables[collectableId].Draw(self.screen)

            self.player.Draw(self.screen)

            for monsterId in self.gameworld.monsters:
                self.gameworld.monsters[monsterId].Draw(self.screen)
        
            self.DrawTimeLeft()
            self.DrawUI()

        else:
            self.DrawMenu()

        pygame.display.update()

    def UpdateAI(self):
        for monsterId in self.gameworld.monsters:
            self.gameworld.monsters[monsterId].Move()

    def RestartLevel(self):
        self.__init__(self.screen, self.currentLevel, self.menuPage)

    def NextLevel(self):
        self.__init__(self.screen, self.currentLevel + 1, self.menuPage + 1)

    def TriggerGameOver(self, victory):
        self.gameOver = True

        if (victory):
            self.NextLevel()
        else:
            self.RestartLevel()

    def Run(self):
        self.running = True # True while game is not exited
        self.playing = False # True while a level is beeing played
        self.timeOver = False # True while a level is beeing played and the 60 seconds are over
        self.gameOver = False # True when the level is over

        self.StartMenuMusic()

        while (self.running):
            self.CheckInputs()
            self.Draw()

            if (self.playing) :
                self.UpdateAI()

            if (self.playing and not self.timeOver and pygame.time.get_ticks() - self.startTime > LEVEL_TIME): # 60 seconds are over
                self.timeOver = True
                self.gameworld.SpawnTimeOverEnemies()
                self.StartTimeOverMusic()

            self.clock.tick(self.fps)