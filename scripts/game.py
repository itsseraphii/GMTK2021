import pygame
from pygame.constants import KEYDOWN, K_n, K_r, MOUSEBUTTONDOWN, QUIT
from gameworld import GameWorld
from entities.player import Player
from utils.constants import TILE_SIZE, DATA_PATH, BLACK, LEVEL_BG_COLOR, TEXT_COLOR
from menu import Menu

MENU_FPS = 30
LEVEL_FPS = 100

LEVEL_TIME = 60000 # 60 seconds
TIME_OVER_ENEMIES_SPAWN_FREQUENCY = 15 # One spawn each x frames
PLAYER_CENTER_POS_Y = 358 # When the player is at the center of the screen, this will always be it's position 

MAIN_MUSIC = DATA_PATH + "/music/Main_theme_v2_loopable.mp3"
# Path for each level 
LEVELS_MUSIC = [DATA_PATH + "/music/level_theme_v2.mp3", DATA_PATH + "/music/level_theme_v2.mp3", DATA_PATH + "/music/level_theme_v2.mp3", DATA_PATH + "/music/level_theme_v2.mp3", DATA_PATH + "/music/level_theme_v2.mp3"]
TIME_OVER_MUSIC = DATA_PATH + "/music/everything_goes_to_shit_v1.mp3"

class Game:
    def Init(self, levelController, screen, currentLevel, menuPage):
        self.screen = screen
        self.screenSize = pygame.display.get_window_size()

        self.clock = pygame.time.Clock()

        self.gameState = -1
        self.menuPage = menuPage
        self.currentLevel = currentLevel
        self.levelController = levelController

        self.InitMenu()
        self.Run()

        return [self.gameState, self.currentLevel, self.menuPage]

    def InitMenu(self):
        self.SetResizeAllowed(True)
        self.fps = MENU_FPS

        self.fontTitle = pygame.font.Font(DATA_PATH + "/fonts/melted.ttf", int(self.screenSize[0] / 8))
        self.fontLarge = pygame.font.Font(DATA_PATH + "/fonts/FreeSansBold.ttf", 45)
        self.fontLargeMelted = pygame.font.Font(DATA_PATH + "/fonts/melted.ttf", 48)
        self.fontMedium = pygame.font.Font(DATA_PATH + "/fonts/FreeSansBold.ttf", 25)

        self.menu = Menu(self.screen, self)

        self.StartMenuMusic()

    def InitLevel(self):
        self.gameworld = GameWorld(self.currentLevel)
        self.player = Player(self, self.gameworld)
        self.gameworld.SetPlayer(self.player)

        self.SetResizeAllowed(False)
        
        self.goalPosY = self.gameworld.FindGoalPosY() + 1 # +1 to see the end of the progress bar before touching the goal
        self.startMiddleY = self.gameworld.startMiddleY
        self.lastProgressHeight = 1000000 # Forces first progress drawing
        self.progressBarBackground = pygame.Rect(self.screenSize[0] - 25, 10, 15, self.screenSize[1] - 20)
        self.progressRatio = (self.screenSize[1] - 20) / -(self.goalPosY - self.startMiddleY)

        self.nbTimeOverFrames = -1
        self.maxTimeOverEnemies = -1
        self.timeOverEnemySpawned = 0
        self.timeOverSpawnsY = []

        self.playing = True
        self.drawnAmmo = -1
        self.drawnWeaponIndex = -1
        self.fps = LEVEL_FPS
        self.startTime = pygame.time.get_ticks()

        self.StartLevelMusic()

        self.screen.fill(LEVEL_BG_COLOR)
        pygame.draw.rect(self.screen, BLACK, self.progressBarBackground)
        self.screen.blit(self.fontMedium.render("Ammo:", True, TEXT_COLOR), (10, self.screenSize[1] - 40))
        self.screen.blit(self.fontMedium.render("Equipped:", True, TEXT_COLOR), (10, self.screenSize[1] - 70))

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
        if (self.playing):
            for event in pygame.event.get():
                if (event.type == QUIT):
                    self.running =  False

                elif (event.type == KEYDOWN):
                    if (event.key == K_r and self.playing):
                        self.TriggerGameOver(False)

                    # Debug info - Uncomment to allow level skipping
                    elif (event.key == K_n and self.playing):
                        self.TriggerGameOver(True)

                elif (event.type == MOUSEBUTTONDOWN):
                    if (event.button == 4): # Mouse wheel up
                        self.player.SwitchWeapon(False)
                    elif event.button == 5: # Mouse wheel down
                        self.player.SwitchWeapon(True)

            self.player.Move(pygame.key.get_pressed())
            self.player.LookAtMouse(pygame.mouse.get_pos())

            if (pygame.mouse.get_pressed()[0]):
                self.player.Attack()
        else:
            self.menu.CheckInputs()

    def ResizeWindow(self, width, height):
        self.screenSize = [max(1280, width), max(720, height)]
        self.screen = pygame.display.set_mode((self.screenSize[0], self.screenSize[1]), pygame.RESIZABLE)
        self.TriggerGameOver(False)

    def SetResizeAllowed(self, allowed):
        if (allowed):
            self.screen = pygame.display.set_mode((self.screenSize[0], self.screenSize[1]), pygame.RESIZABLE)
        else:
            self.screen = pygame.display.set_mode((self.screenSize[0], self.screenSize[1]))

    def DrawTimeLeft(self):
        if (not self.timeOver):
            msLeft = max(0, LEVEL_TIME - pygame.time.get_ticks() + self.startTime)
            secLeft = round(msLeft / 1000, 2)
            extra0 = "0" if (secLeft) < 10 else ""
            self.screen.blit(self.fontLarge.render(extra0 + str(secLeft), True, TEXT_COLOR, LEVEL_BG_COLOR), (10, 0))

    def DrawProgress(self):
        currentPos = self.gameworld.middleY - self.startMiddleY
        newProgressHeight = int(max(13, currentPos * self.progressRatio + self.screenSize[1] - 14))

        if (newProgressHeight < self.lastProgressHeight): # Player has progressed
            self.lastProgressHeight = newProgressHeight
            progressBarForeground = pygame.Rect(self.screenSize[0] - 22, newProgressHeight, 9, min(self.screenSize[1] - 26, 1))
            pygame.draw.rect(self.screen, TEXT_COLOR, progressBarForeground)

    def DrawWeaponUI(self):
        if (self.player.equippedWeaponIndex != self.drawnWeaponIndex): # Draw new equipped weapon
            self.drawnWeaponIndex = self.player.equippedWeaponIndex
            pygame.draw.rect(self.screen, LEVEL_BG_COLOR, pygame.Rect((137, self.screenSize[1] - 68), (150, 29))) # Cover last drawn weapon name
            self.screen.blit(self.fontMedium.render(self.player.GetEquippedWeaponName(), True, TEXT_COLOR), (138, self.screenSize[1] - 70))

        if (self.player.ammo != self.drawnAmmo): # Draw new ammo count
            self.drawnAmmo = self.player.ammo
            pygame.draw.rect(self.screen, LEVEL_BG_COLOR, pygame.Rect((104, self.screenSize[1] - 38), (60, 28))) # Cover last drawn ammo
            self.screen.blit(self.fontMedium.render(str(self.drawnAmmo), True, TEXT_COLOR), (105, self.screenSize[1] - 40))

    def DrawUI(self):
        self.DrawTimeLeft()
        self.DrawProgress()
        self.DrawWeaponUI()

        '''# Debug info - Uncomment to show fps average over the last 10 frames
        fps = round(self.clock.get_fps(), 2)

        if (fps < 80):
            fpsColor = (255, 0, 0)
        elif (fps < 90):
            fpsColor = (255, 255, 0)
        else:
            fpsColor = (0, 255, 0)

        self.screen.blit(self.fontMedium.render("FPS: " + str(fps), True, fpsColor, LEVEL_BG_COLOR), (10, self.screenSize[1] / 2))'''

    def Draw(self):
        if (self.playing):
            self.gameworld.Draw(self.screen)

            for collectableId in self.gameworld.collectables:
                self.gameworld.collectables[collectableId].Draw(self.screen)

            self.player.Draw(self.screen)

            for monsterId in self.gameworld.monsters:
                self.gameworld.monsters[monsterId].Draw(self.screen)
        
            self.DrawUI()

        else:
            self.menu.Draw()

        pygame.display.update()

    def UpdateAI(self):
        for monster in self.gameworld.monsters.values():
            monster.Move()

    def CheckTimeOver(self):
        if (pygame.time.get_ticks() - self.startTime > LEVEL_TIME):
            self.timeOver = True
            self.screen.blit(self.fontLargeMelted.render("They're here", True, TEXT_COLOR, LEVEL_BG_COLOR), (10, 10))
            self.StartTimeOverMusic()

    def SpawnTimeOverEnemies(self):
        if (self.timeOverEnemySpawned < self.maxTimeOverEnemies): # Check if there are enemies to spawn
            self.nbTimeOverFrames += 1

            if (self.nbTimeOverFrames % TIME_OVER_ENEMIES_SPAWN_FREQUENCY == 0): # Check if it's time to spawn an enemy
                if (len(self.timeOverSpawnsY) == 2 and not self.gameworld.middleY - self.gameworld.screenNbTilesY > self.startMiddleY - (self.gameworld.backgroundSize[1] / TILE_SIZE) + 6): # If ennemies can no longer spawn over
                    self.timeOverSpawnsY.pop(0)
                
                self.gameworld.SpawnTimeOverEnemy(-self.timeOverEnemySpawned, self.timeOverSpawnsY[self.timeOverEnemySpawned % len(self.timeOverSpawnsY)])
                self.timeOverEnemySpawned += 1
                
        elif (self.maxTimeOverEnemies < 0): # Generate info required to spawn enemies
            self.maxTimeOverEnemies = min((self.currentLevel + 1) * 10 + 5, 50)
            
            # Can spawn over player
            if (self.gameworld.middleY - self.gameworld.screenNbTilesY > self.startMiddleY - (self.gameworld.backgroundSize[1] / TILE_SIZE) + 7):
                self.timeOverSpawnsY.append(PLAYER_CENTER_POS_Y - (self.screenSize[1] / 2) - (2 * TILE_SIZE))
            
            # Can spawn under player
            if (self.gameworld.middleY - self.startMiddleY + (self.gameworld.screenNbTilesY / 2) < 0):
                self.timeOverSpawnsY.append(PLAYER_CENTER_POS_Y + (self.screenSize[1] / 2))

    def TriggerGameOver(self, victory):
        self.gameState = 1 if (victory) else 0
        self.running = False

    def Run(self):
        self.running = True # True while the game is not exited
        self.playing = False # True while a level is being played
        self.timeOver = False # True while a level is being played and the 60 seconds are over

        while (self.running):
            self.CheckInputs()
            self.Draw()

            if (self.playing):
                self.UpdateAI()

            if (self.timeOver):
                self.SpawnTimeOverEnemies()
            elif (self.playing):
                self.CheckTimeOver()

            self.clock.tick(self.fps)