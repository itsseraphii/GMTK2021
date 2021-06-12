import pygame
from pygame.constants import K_a, K_d, K_s, K_w
import math
from entities.weapon import Weapon

SPEED = 2
IMAGE_FILE = "./res/player_gun.png"
PLAYER_SIZE = [32, 32]

class Player:
    def __init__(self, background):
        self.background = background
        self.screenSize = pygame.display.get_window_size()
        self.image = pygame.transform.scale(pygame.image.load(IMAGE_FILE), (30, 30))
        self.rotatedImage = self.image
        self.posX, self.posY = self.screenSize[0] / 2, self.screenSize[1] / 4 * 3

        self.hasRangedWeapon = True
        self.weapon = Weapon(self)

    def Move(self, pressedKeys):
        if pressedKeys[K_w]:
            if (self.posY < self.screenSize[1] / 2):
                self.background.IncreaseOffsetY(SPEED)
            else:
                self.posY -= SPEED
        if pressedKeys[K_a]:
           if (self.posX - SPEED > self.screenSize[0] / 2 - 200):
                self.posX -= SPEED
        if pressedKeys[K_s]:
            if (self.posY + SPEED  < self.screenSize[1] - PLAYER_SIZE[1]):
                self.posY += SPEED
        if pressedKeys[K_d]:
            if (self.posX + SPEED < self.screenSize[0] / 2 + 200):
                self.posX += SPEED

    def LookAtMouse(self, mouseX, mouseY):
        relativeX, relativeY = mouseX - self.posX, mouseY - self.posY
        self.angle = (180 / math.pi) * -math.atan2(relativeY, relativeX)
        self.rotatedImage = pygame.transform.rotate(self.image, int(self.angle))

    def Attack(self):
        if (self.hasRangedWeapon):
            self.weapon.Fire()

    def GetSize(self):
        return PLAYER_SIZE

    def GetPos(self):
        return [self.posX, self.posY]

    def GetAngle(self):
        return self.angle
    
    def Draw(self, screen):
        self.weapon.Draw(screen)
        screen.blit(self.rotatedImage, (self.posX, self.posY))