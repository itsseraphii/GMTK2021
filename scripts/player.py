import pygame
from pygame.constants import K_a, K_d, K_s, K_w
import math

SPEED = 2
IMAGE_FILE = "./res/arrow.png"
PLAYER_SIZE = [30, 30]

class Player:
    def __init__(self, background):
        self.background = background
        self.screenSize = pygame.display.get_window_size()
        self.image = pygame.transform.scale(pygame.image.load(IMAGE_FILE), (30, 30))
        self.rotatedImage = self.image
        self.posX, self.posY = self.screenSize[0] / 2, self.screenSize[1] - PLAYER_SIZE[1]
        self.background.SetPlayerSize(PLAYER_SIZE)

    def Move(self, pressedKeys):
        if pressedKeys[K_w]:
            if (self.posY < self.screenSize[1] / 2):
                self.background.IncreaseOffsetY(SPEED)
            else:
                self.posY -= SPEED
        if pressedKeys[K_a]:
           if (self.background.InWidthBounds(self.posX - SPEED)):
                self.posX -= SPEED
        if pressedKeys[K_s]:
            if (self.posY + SPEED  < self.screenSize[1] - PLAYER_SIZE[1]):
                self.posY += SPEED
        if pressedKeys[K_d]:
            if (self.background.InWidthBounds(self.posX + SPEED)):
                self.posX += SPEED

    def LookAtMouse(self, mouseX, mouseY):
        relativeX, relativeY = mouseX - self.posX, mouseY - self.posY
        angle = (180 / math.pi) * -math.atan2(relativeY, relativeX)
        self.rotatedImage = pygame.transform.rotate(self.image, int(angle))
    
    def Draw(self, screen):
        screen.blit(self.rotatedImage, (self.posX, self.posY))