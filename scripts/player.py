import pygame
from pygame.constants import K_a, K_d, K_s, K_w
import math

SPEED = 2
IMAGE_FILE = "./res/arrow.png"

class Player:
    def __init__(self):
        self.posX, self.posY = 0, 0
        self.image = pygame.transform.smoothscale(pygame.image.load(IMAGE_FILE), (30, 30))
        self.rotatedImage = self.image

    def Move(self, pressedKeys):
        if pressedKeys[K_w]:
            self.posY -= SPEED
        if pressedKeys[K_a]:
            self.posX -= SPEED
        if pressedKeys[K_s]:
            self.posY += SPEED
        if pressedKeys[K_d]:
            self.posX += SPEED

    def LookAtMouse(self, mouseX, mouseY):
        relativeX, relativeY = mouseX - self.posX, mouseY - self.posY
        angle = (180 / math.pi) * -math.atan2(relativeY, relativeX)
        self.rotatedImage = pygame.transform.rotate(self.image, int(angle))
    
    def Draw(self, screen):
        screen.blit(self.rotatedImage, (self.posX, self.posY))