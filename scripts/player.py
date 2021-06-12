import pygame
from pygame.constants import K_a, K_d, K_s, K_w
from spriteUtils import getFrames
import math

SPEED = 2
IMAGE_FILE = "./res/player_gun.png"
WALKING_ANIMATION = "player_unarmed.png"
PLAYER_SIZE = [30, 30]

class Player:
    def __init__(self, background):
        self.background = background
        self.screenSize = pygame.display.get_window_size()
        self.image = pygame.transform.scale(pygame.image.load(IMAGE_FILE), (32, 32))
        self.rotatedImage = self.image
        self.posX, self.posY = self.screenSize[0] / 2, self.screenSize[1] / 4 * 3
        self.walking_frames = getFrames(WALKING_ANIMATION, 32)
        self.frame_counter = 0

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

    def NextFrame(self):
        self.frame_counter += 1

        if (self.frame_counter >= len(self.walking_frames)) :
            self.frame_counter = 0

        print(self.frame_counter)
        self.image = self.walking_frames[self.frame_counter]

    def LookAtMouse(self, mouseX, mouseY):
        relativeX, relativeY = mouseX - self.posX, mouseY - self.posY
        angle = (180 / math.pi) * -math.atan2(relativeY, relativeX)
        self.rotatedImage = pygame.transform.rotate(self.image, int(angle))

    def GetSize(self):
        return PLAYER_SIZE

    def GetPos(self):
        return [self.posX, self.posY]
    
    def Draw(self, screen):
        screen.blit(self.rotatedImage, (self.posX, self.posY))