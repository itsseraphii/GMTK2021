import pygame
from pygame.constants import KEYDOWN, K_RETURN, QUIT, VIDEORESIZE
from utils.constants import MENU_BG_COLOR, LEVEL_BG_COLOR, TEXT_COLOR, ENDING_MENU_PAGE
from utils.story import STORY

class Menu():
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.screenSize = self.game.screenSize

        buttonBasePos = [self.screenSize[0] / 2, self.screenSize[1] / 2 - 50 + self.screenSize[0] / 16]
        buttonSize = [300, 75]

        self.menuButtons = {
            "continue" : Button(buttonBasePos[0] - 350, buttonBasePos[1], buttonSize, LEVEL_BG_COLOR, TEXT_COLOR, MENU_BG_COLOR, self.game.fontMedium, "Continue"),
            "newGame": Button(buttonBasePos[0] + 50, buttonBasePos[1], buttonSize, LEVEL_BG_COLOR, TEXT_COLOR, MENU_BG_COLOR, self.game.fontMedium, "New Game"),
            "controls": Button(buttonBasePos[0] - 350, buttonBasePos[1] + 150, buttonSize, LEVEL_BG_COLOR, TEXT_COLOR, MENU_BG_COLOR, self.game.fontMedium, "Controls"),
            "exit": Button(buttonBasePos[0] + 50, buttonBasePos[1] + 150, buttonSize, LEVEL_BG_COLOR, TEXT_COLOR, MENU_BG_COLOR, self.game.fontMedium, "Exit")
        }

    def CheckInputs(self):
        for event in pygame.event.get():
            if (event.type == QUIT):
                self.game.running =  False

            elif (event.type == VIDEORESIZE): # Can only resize in menus (between levels)
                self.game.ResizeWindow(event.w, event.h)

            elif (self.game.menuPage == -1):
                for key in list(self.menuButtons):
                    if (self.menuButtons[key].IsMouseOver(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]):
                        if (key == "continue"):
                            self.game.menuPage += 1
                        elif (key == "newGame"):
                            self.game.currentLevel = 0
                            self.game.menuPage += 1
                            self.game.TriggerGameOver(False)
                        elif (key == "controls"):
                            self.game.menuPage = -3
                        else:
                            self.game.running = False

            elif (event.type == KEYDOWN):
                if (self.game.menuPage == -2): # Press any key on title screen to go to menu
                    self.game.menuPage += 1
                elif (self.game.menuPage == ENDING_MENU_PAGE): # Press any key on credits to go to title screen
                    self.game.menuPage = -2
                elif (self.game.menuPage == -3): # Press any key on controls to go to menu
                    self.game.menuPage = -1

                elif (event.key == K_RETURN):
                    if (self.game.menuPage != self.game.currentLevel or self.game.menuPage == ENDING_MENU_PAGE - 1):
                        self.game.menuPage += 1
                    else: # Start of a level
                        self.game.InitLevel()

    def Draw(self):
        self.screen.fill(MENU_BG_COLOR)

        if (self.game.menuPage == -3): # Controls
            controls = ["W A S D to move", "", "Mouse to aim", "", "Left click to shoot", "", "Scrollwheel to change weapons", "", "R to restart a level"]
            self.DrawParagraph(controls)
            text = self.game.fontMedium.render("Press any key to return to the menu", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] - 30))
            self.screen.blit(text, textRect)

        elif (self.game.menuPage == -2): # Title screen
            text = self.game.fontTitle.render("Transgenesis", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] / 2))
            self.screen.blit(text, textRect)

        elif (self.game.menuPage == -1): # Menu
            text = self.game.fontTitle.render("Transgenesis", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] / 3))
            self.screen.blit(text, textRect)

            mousePos = pygame.mouse.get_pos()

            for button in self.menuButtons.values():
                button.Draw(self.screen, button.IsMouseOver(mousePos))

        elif (self.game.menuPage == ENDING_MENU_PAGE): # Credits
            text = self.game.fontTitle.render("Transgenesis", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] / 2 - 50))
            self.screen.blit(text, textRect)
            text = self.game.fontLarge.render("Thank you for playing!", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] - 200))
            self.screen.blit(text, textRect)

        else: # Levels
            message = "Press Enter to start level " + str(self.game.currentLevel + 1) if (self.game.menuPage != ENDING_MENU_PAGE - 1) else "Press Enter to continue"
            text = self.game.fontMedium.render(message, True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] - 30))
            self.screen.blit(text, textRect)
            self.DrawParagraph(STORY[self.game.menuPage])

    def DrawParagraph(self, lines):
        for i in range(len(lines)):
            text = self.game.fontMedium.render(lines[i], True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, (self.screenSize[1] / 4) + (i * 30)))
            self.screen.blit(text, textRect)

class Button():
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