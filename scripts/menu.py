import pygame
from pygame.constants import KEYDOWN, K_ESCAPE, K_RETURN, QUIT, VIDEORESIZE
from math import floor
from utils.constants import MENU_BG_COLOR, LEVEL_BG_COLOR, TEXT_COLOR, CREDITS_PAGE, DATA_PATH
from musicController import StartMusicBoss, StartMusicCredits, ProcessMusicEvents
from utils.story import STORY

MEDIUM_BTN_SIZE = [300, 75]
SMALL_BTN_SIZE = [200, 50]

class Menu:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.screenSize = game.screenSize

        self.menuInitialized = False
        self.statsInitialized = False
        self.secretInitialized = False
        self.creditsInitialized = False
        self.selectLevelInitialized = False

    def InitMainMenu(self):
        self.menuInitialized = True
        buttonBasePos = [self.screenSize[0] / 2, (self.screenSize[1] / 2 - 75) + (self.screenSize[0] / 16)]

        self.menuButtons = {
            "select": Button(buttonBasePos[0] + 20, buttonBasePos[1], MEDIUM_BTN_SIZE, LEVEL_BG_COLOR, TEXT_COLOR, MENU_BG_COLOR, self.game.fontMedium, "Select Level"),
            "newGame": Button(buttonBasePos[0] - 150, buttonBasePos[1] + 120, MEDIUM_BTN_SIZE, LEVEL_BG_COLOR, TEXT_COLOR, MENU_BG_COLOR, self.game.fontMedium, "New Game"),
            "controls": Button(5, self.screenSize[1] - 55, SMALL_BTN_SIZE, LEVEL_BG_COLOR, TEXT_COLOR, MENU_BG_COLOR, self.game.fontMedium, "Controls"),
            "stats": Button(213, self.screenSize[1] - 55, SMALL_BTN_SIZE, LEVEL_BG_COLOR, TEXT_COLOR, MENU_BG_COLOR, self.game.fontMedium, "Stats"),
            "exit": Button(self.screenSize[0] - 205, self.screenSize[1] - 55, SMALL_BTN_SIZE, LEVEL_BG_COLOR, TEXT_COLOR, MENU_BG_COLOR, self.game.fontMedium, "Exit")
        }

        if (self.game.levelController.HasSavedProgress()): # If a save was found
            self.menuButtons["continue"] = Button(buttonBasePos[0] - 320, buttonBasePos[1], MEDIUM_BTN_SIZE, LEVEL_BG_COLOR, TEXT_COLOR, MENU_BG_COLOR, self.game.fontMedium, "Continue")
        else:
            self.menuButtons["continueDisabled"] = Button(buttonBasePos[0] - 320, buttonBasePos[1], MEDIUM_BTN_SIZE, MENU_BG_COLOR, LEVEL_BG_COLOR, MENU_BG_COLOR, self.game.fontMedium, "Continue")
        
    def InitStats(self):
        self.statsInitialized = True
        self.secretInitialized = False
        self.resetConfirmed = False
        self.resetReleased = False
        self.secretColor = TEXT_COLOR
        self.secretUnlocked = len(self.game.levelController.savedSecrets) > 0 # == CREDITS_PAGE - 1
        self.btnResetStats = Button(self.screenSize[0] - 135, self.screenSize[1] - 45, (130, 40), LEVEL_BG_COLOR, TEXT_COLOR, MENU_BG_COLOR, self.game.fontMedium, "Reset")

    def InitSecret(self):
        self.secretInitialized = True
        self.secretColor = TEXT_COLOR
        self.pickleBoy = pygame.transform.scale(pygame.image.load("res/pickleBoy.png"), (256, 256))
        self.pickleFriends = [
            pygame.transform.scale(pygame.image.load("res/pickleChest.png"), (64, 64)),
            pygame.transform.scale(pygame.image.load("res/pickleScreen.png"), (64, 64)),
            pygame.transform.scale(pygame.image.load("res/pickleWall.png"), (64, 64)),
            pygame.transform.scale(pygame.image.load("res/pickleWire.png"), (64, 64))
        ]
        StartMusicBoss()

    def InitCredits(self):
        self.creditsInitialized = True
        self.menuScrollY = self.screenSize[1] + floor(self.screenSize[0] / 15)
        self.creditsFontSmall = pygame.font.Font(DATA_PATH + "/fonts/FreeSansBold.ttf", floor(self.screenSize[0] / 52))
        self.creditsFontMedium = pygame.font.Font(DATA_PATH + "/fonts/FreeSansBold.ttf", floor(self.screenSize[0] / 42))
        self.creditsFontLarge = pygame.font.Font(DATA_PATH + "/fonts/FreeSansBold.ttf", floor(self.screenSize[0] / 35))
        self.creditsSpace = floor(self.screenSize[0] / 10)
        self.game.levelController.UpdateProgress([self.game.gameState, self.game.currentLevel, self.game.menuPage])
        StartMusicCredits()

    def InitSelectLevel(self):
        self.selectLevelInitialized = True
        self.selectLevelButtons = []

        for i in range(CREDITS_PAGE - 1):
            btnPos = [(self.screenSize[0] / 2 - 300) + (i % 3 * 300) - (SMALL_BTN_SIZE[0] / 2), floor(i / 3) * 100 + 100]

            if (i <= self.game.levelController.savedProgress[0]):
                self.selectLevelButtons.append(Button(btnPos[0], btnPos[1], SMALL_BTN_SIZE, LEVEL_BG_COLOR, TEXT_COLOR, MENU_BG_COLOR, self.game.fontMedium, "Level " + str(i + 1)))
            else:
                self.selectLevelButtons.append(Button(btnPos[0], btnPos[1], SMALL_BTN_SIZE, MENU_BG_COLOR, LEVEL_BG_COLOR, MENU_BG_COLOR, self.game.fontMedium, "Level " + str(i + 1)))

        offsetButtonCount = len(self.selectLevelButtons) % 3

        if (offsetButtonCount != 0): # Align last row if it has less than 3 buttons 
            for i in range (len(self.selectLevelButtons) - offsetButtonCount, len(self.selectLevelButtons)):
                self.selectLevelButtons[i].x += (3 - offsetButtonCount) * 150

    def CheckInputs(self):
        for event in pygame.event.get():
            if (event.type == QUIT):
                self.game.running = False

            elif (event.type == VIDEORESIZE):
                self.game.ResizeWindow(event.w, event.h)

            elif (self.game.menuPage == -1): # Main menu
                if (not self.menuInitialized):
                    self.InitMainMenu()

                mousePos = pygame.mouse.get_pos()
                mouseLeftClick = pygame.mouse.get_pressed()[0]

                for key in list(self.menuButtons):
                    if (self.menuButtons[key].IsMouseOver(mousePos) and mouseLeftClick):
                        if (key == "continue"):
                            self.game.currentLevel = self.game.levelController.savedProgress[0]
                            self.game.menuPage = self.game.levelController.savedProgress[1]
                        elif (key == "select"):
                            self.game.menuPage = -5
                        elif (key == "newGame"):
                            self.game.currentLevel = 0
                            self.game.menuPage = 0
                            self.game.levelController.savedProgress = [0, 0]
                        elif (key == "controls"):
                            self.game.menuPage = -3
                        elif (key == "stats"):
                            self.game.menuPage = -4
                        elif (key == "exit"):
                            self.game.running = False

            elif (self.game.menuPage == -5 and event.type != KEYDOWN): # Select level
                if (not self.selectLevelInitialized):
                    self.InitSelectLevel()

                mousePos = pygame.mouse.get_pos()
                mouseLeftClick = pygame.mouse.get_pressed()[0]

                for i in range(len(self.selectLevelButtons)):
                    if (self.selectLevelButtons[i].IsMouseOver(mousePos) and mouseLeftClick and i <= self.game.levelController.savedProgress[0]):
                        self.game.currentLevel = i
                        self.game.menuPage = i
                        break

            elif (event.type == KEYDOWN):
                if (self.game.menuPage == -4): # Stats
                    self.statsInitialized = False
                    self.game.menuPage = -1
                elif (self.game.menuPage < -1): # Press any key on title screen, in controls, in select level or in stats to go to the main menu
                    self.game.menuPage = -1
                elif (self.game.menuPage == CREDITS_PAGE): # Press any key on credits to go to title screen
                    self.creditsInitialized = False # Reset credits next time it's displayed
                    self.game.menuPage = -2

                elif (event.key == K_RETURN):
                    if (self.game.menuPage != self.game.currentLevel or self.game.menuPage == CREDITS_PAGE - 1):
                        self.game.menuPage += 1
                    else: # Start of a level
                        self.game.InitLevel()

                elif (event.key == K_ESCAPE):
                    self.game.menuPage = -1

            elif (self.game.menuPage == -4): # Stats
                if (not self.statsInitialized):
                    self.InitStats()

                mousePos = pygame.mouse.get_pos()
                mouseLeftClick = pygame.mouse.get_pressed()[0]
                
                self.resetReleased = self.resetReleased or self.resetConfirmed and not mouseLeftClick
                self.secretHovered = mousePos[0] > self.screenSize[0] / 2 - 320 and mousePos[0] < self.screenSize[0] / 2 - 80 and mousePos[1] > 265 and mousePos[1] < 289
                self.secretColor = LEVEL_BG_COLOR if (self.secretUnlocked and self.secretHovered) else TEXT_COLOR

                if (mouseLeftClick):
                    if (self.btnResetStats.IsMouseOver(mousePos)):
                        if (self.resetConfirmed and self.resetReleased):
                            self.game.levelController.ResetStats()
                            self.btnResetStats.hoverColor = LEVEL_BG_COLOR
                            self.btnResetStats.text = "Done"
                        else:
                            self.resetConfirmed = True
                            self.btnResetStats.text = "Confirm?"

                    elif (self.secretHovered):
                        self.game.menuPage = -6

            elif (event.type in self.game.musicEvents):
                ProcessMusicEvents(event.type)

    def Draw(self):
        self.screen.fill(MENU_BG_COLOR)

        if (self.game.menuPage == -5): # Select Level
            if (not self.selectLevelInitialized):
                self.InitSelectLevel()

            text = self.game.fontLarge.render("Select Level", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, 40))
            self.screen.blit(text, textRect)

            mousePos = pygame.mouse.get_pos()

            for button in self.selectLevelButtons:
                button.Draw(self.screen, button.IsMouseOver(mousePos))

            text = self.game.fontMedium.render("Press any key to go back", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] - 30))
            self.screen.blit(text, textRect)

        elif (self.game.menuPage == -4): # Stats
            if (not self.statsInitialized):
                self.InitStats()

            text = self.game.fontLarge.render("Stats", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, 40))
            self.screen.blit(text, textRect)

            text = self.game.fontMedium.render("Kills: " + str(self.game.levelController.savedKills), True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2 - 200, 125))
            self.screen.blit(text, textRect)

            text = self.game.fontMedium.render("Deaths: " + str(self.game.levelController.savedDeaths), True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2 + 200, 125))
            self.screen.blit(text, textRect)

            text = self.game.fontMedium.render("Rounds Fired: " + str(self.game.levelController.savedRoundsFired), True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2 - 200, 175))
            self.screen.blit(text, textRect)

            text = self.game.fontMedium.render("Rounds Hit: " + str(self.game.levelController.savedRoundsHit), True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2 + 200, 175))
            self.screen.blit(text, textRect)

            text = self.game.fontMedium.render("Items Picked Up: " + str(self.game.levelController.savedPickups), True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2 - 200, 225))
            self.screen.blit(text, textRect)

            text = self.game.fontMedium.render("Levels Completed: " + str(self.game.levelController.savedCompletions), True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2 + 200, 225))
            self.screen.blit(text, textRect)

            text = self.game.fontMedium.render("Secrets Found: " + str(len(self.game.levelController.savedSecrets)) + " / " + str(CREDITS_PAGE - 1), True, self.secretColor)
            textRect = text.get_rect(center = (self.screenSize[0] / 2 - 200, 275))
            self.screen.blit(text, textRect)

            text = self.game.fontMedium.render("Play Time: " + self.GetTimeString(self.game.levelController.savedPlayTime + pygame.time.get_ticks()), True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2 + 200, 275))
            self.screen.blit(text, textRect)

            text = self.game.fontMedium.render("Best Times", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, 375))
            self.screen.blit(text, textRect)

            bestTotalTimeMs = 0

            for key in list(self.game.levelController.savedTimes):
                level = int(key)
                bestTotalTimeMs += self.game.levelController.savedTimes[key]
                text = self.game.fontMedium.render("Level " + str(level + 1) + ": " + str(self.game.levelController.savedTimes[key] / 1000) + "s", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2 - 300 + (level % 3 * 300), floor(level / 3) * 50 + 425))
                self.screen.blit(text, textRect)

            if (len(self.game.levelController.savedTimes) == CREDITS_PAGE - 1):
                text = self.game.fontMedium.render("Best Total Time: " + str(bestTotalTimeMs / 1000) + "s", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, floor(level / 3) * 50 + 525))
                self.screen.blit(text, textRect)

            text = self.game.fontMedium.render("Press any key to go back", True, TEXT_COLOR)
            textRect = text.get_rect(topleft = (8, self.screenSize[1] - 40))
            self.screen.blit(text, textRect)

            self.btnResetStats.Draw(self.screen, self.btnResetStats.IsMouseOver(pygame.mouse.get_pos()))

        elif (self.game.menuPage == -6): # Secret
            if (not self.secretInitialized):
                self.InitSecret()

            text = self.game.fontLarge.render("Pickle Boy - The Return", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, 40))
            self.screen.blit(text, textRect)

            text = self.game.fontMedium.render("You found all secrets!", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, 80))
            self.screen.blit(text, textRect)

            self.screen.blit(self.pickleBoy, (self.screenSize[0] / 2 - 128, 160))

            for i in range(len(self.pickleFriends)):
                self.screen.blit(self.pickleFriends[i], (self.screenSize[0] / 2 - 256 + (i % 4 * 128) + 32, 500))

            text = self.game.fontMedium.render("Press any key to go back", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] - 30))
            self.screen.blit(text, textRect)

        elif (self.game.menuPage == -3): # Controls
            text = self.game.fontLarge.render("Controls", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, 40))
            self.screen.blit(text, textRect)

            controls = ["W A S D  -  Move", "", "Mouse  -  Aim", "", "Left click  -  Shoot", "", "Scrollwheel  -  Change weapons", "", "", "R  -  Restart level", "", "ESC  -  Go to main menu"]
            self.DrawParagraph(controls)
            text = self.game.fontMedium.render("Press any key to go back", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] - 30))
            self.screen.blit(text, textRect)

        elif (self.game.menuPage == -2): # Title screen
            text = self.game.fontTitle.render("Transgenesis", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] / 2))
            self.screen.blit(text, textRect)

        elif (self.game.menuPage == -1): # Main menu
            if (not self.menuInitialized):
                self.InitMainMenu()

            text = self.game.fontTitle.render("Transgenesis", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] / 3))
            self.screen.blit(text, textRect)

            mousePos = pygame.mouse.get_pos()

            for button in self.menuButtons.values():
                button.Draw(self.screen, button.IsMouseOver(mousePos))

        elif (self.game.menuPage >= CREDITS_PAGE):
            if (not self.creditsInitialized):
                self.InitCredits()

            if (13 * self.creditsSpace + self.menuScrollY > 0):
                text = self.game.fontTitle.render("Transgenesis", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, self.menuScrollY))
                self.screen.blit(text, textRect)

                text = self.creditsFontMedium.render("Psycho", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, 4 * self.creditsSpace + self.menuScrollY))
                self.screen.blit(text, textRect)
                text = self.creditsFontSmall.render("Developer, Software Architect, Level Designer, Writer, Texture Artist", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, 4 * self.creditsSpace + self.menuScrollY + floor(self.screenSize[0] / 40)))
                self.screen.blit(text, textRect)
                text = self.creditsFontMedium.render("Seraphii", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, 5 * self.creditsSpace + self.menuScrollY))
                self.screen.blit(text, textRect)
                text = self.creditsFontSmall.render("Developer, Assets Artist", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, 5 * self.creditsSpace + self.menuScrollY + floor(self.screenSize[0] / 40)))
                self.screen.blit(text, textRect)
                text = self.creditsFontMedium.render("Hypstersaurus", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, 6 * self.creditsSpace + self.menuScrollY))
                self.screen.blit(text, textRect)
                text = self.creditsFontSmall.render("Developer, Texture Artist", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, 6 * self.creditsSpace + self.menuScrollY + floor(self.screenSize[0] / 40)))
                self.screen.blit(text, textRect)
                text = self.creditsFontMedium.render("Parazyte", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, 7 * self.creditsSpace + self.menuScrollY))
                self.screen.blit(text, textRect)
                text = self.creditsFontSmall.render("Composer, Level Designer, Writer", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, 7 * self.creditsSpace + self.menuScrollY + floor(self.screenSize[0] / 40)))
                self.screen.blit(text, textRect)
                text = self.creditsFontMedium.render("Nemesis", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, 8 * self.creditsSpace + self.menuScrollY))
                self.screen.blit(text, textRect)
                text = self.creditsFontSmall.render("Enemy Designer, Writer", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, 8 * self.creditsSpace + self.menuScrollY + floor(self.screenSize[0] / 40)))
                self.screen.blit(text, textRect)

                text = self.creditsFontLarge.render("Thank you for playing!", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, 12 * self.creditsSpace + self.menuScrollY))
                self.screen.blit(text, textRect)

            elif (13 * self.creditsSpace + self.menuScrollY > -950):
                text = self.game.fontMedium.render("Press any key", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] - 30))
                self.screen.blit(text, textRect)

            elif (13 * self.creditsSpace + self.menuScrollY < -1000):
                self.menuScrollY = self.screenSize[1] + floor(self.screenSize[0] / 15)

            self.menuScrollY -= 1

        else: # Levels
            message = "Press Enter to start level " + str(self.game.currentLevel + 1) if (self.game.menuPage != CREDITS_PAGE - 1) else "Press Enter to continue"
            text = self.game.fontMedium.render(message, True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] - 30))
            self.screen.blit(text, textRect)
            self.DrawParagraph(STORY[self.game.menuPage])

    def DrawParagraph(self, lines):
        for i in range(len(lines)):
            text = self.game.fontMedium.render(lines[i], True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, (self.screenSize[1] / 5) + (i * 30)))
            self.screen.blit(text, textRect)

    def GetTimeString(self, milliseconds):
        seconds, milliseconds = divmod(milliseconds, 1000) 
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        seconds = floor(seconds + milliseconds / 1000)

        strDays = "" if (days < 1) else str(days) + ":"
        strHours = "0" + str(hours) if (hours < 10) else str(hours)
        strMinutes = "0" + str(minutes) if (minutes < 10) else str(minutes)
        strSeconds = "0" + str(seconds) if (seconds < 10) else str(seconds)

        return strDays + strHours + ":" + strMinutes + ":" + strSeconds

class Button:
    def __init__(self, x, y, size, bgColor, textColor, hoverColor, font, text):
        self.x = x
        self.y = y
        self.width = size[0]
        self.height = size[1]
        self.bgColor = bgColor
        self.textColor = textColor
        self.hoverColor = hoverColor
        self.font = font
        self.text = text

    def Draw(self, screen, mouseOver):
        pygame.draw.rect(screen, self.textColor, (self.x - 2 , self.y - 2 ,self.width + 4 ,self.height + 4), 0)

        if (mouseOver):
            pygame.draw.rect(screen, self.hoverColor, (self.x, self.y, self.width, self.height), 0)
        else:
            pygame.draw.rect(screen, self.bgColor, (self.x, self.y, self.width, self.height), 0)
        
        text = self.font.render(self.text, 1, self.textColor)
        screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def IsMouseOver(self, mousePos):
        if mousePos[0] > self.x and mousePos[0] < self.x + self.width:
            if mousePos[1] > self.y and mousePos[1] < self.y + self.height:
                return True

        return False