import pygame
from pygame.constants import K_a, K_d, K_s, K_w
from spriteUtils import getFrames
import math
from entities.weapon import Weapon

SPEED = 2
IMAGE_FILE = "./res/player_gun.png"
WALKING_ANIMATION = "player_unarmed.png"
ANIMATION_SPEED = 84 # ms
PLAYER_SIZE = [32, 32]

class Player:
    def __init__(self, background):
        self.background = background
        self.screenSize = pygame.display.get_window_size()
        self.posX, self.posY = self.screenSize[0] / 2, self.screenSize[1] / 4 * 3

        self.walking_frames = getFrames(WALKING_ANIMATION, 32)
        self.frame_counter = 0
        self.lastFrameTime = 0

        self.image = pygame.transform.scale(pygame.image.load(IMAGE_FILE), (30, 30))
        self.rotatedImage = self.image

        self.equippedWeapon = "Revolver"
        self.ammo = 13
        self.weapon = Weapon(self)

    def Move(self, pressedKeys):
        moving = False
        if pressedKeys[K_w]:
            moving = True
            if (self.posY < self.screenSize[1] / 2):
                self.background.IncreaseOffsetY(SPEED)
            else:
                self.posY -= SPEED
        if pressedKeys[K_a]:
            moving = True
            self.posX -= SPEED
        if pressedKeys[K_s]:
            moving = True
            if (self.posY + SPEED  < self.screenSize[1] - PLAYER_SIZE[1]):
                self.posY += SPEED
        if pressedKeys[K_d]:
            moving = True
            self.posX += SPEED

        currentTime = pygame.time.get_ticks()

        if (currentTime >= self.lastFrameTime + ANIMATION_SPEED and moving ):
            self.lastFrameTime = currentTime
            self.NextFrame()

    def NextFrame(self):
        self.frame_counter += 1

        if (self.frame_counter >= len(self.walking_frames)) :
            self.frame_counter = 0

        self.image = self.walking_frames[self.frame_counter]

    def LookAtMouse(self, mouseX, mouseY):
        relativeX, relativeY = mouseX - self.posX, mouseY - self.posY
        self.angle = (180 / math.pi) * -math.atan2(relativeY, relativeX)
        self.rotatedImage = pygame.transform.rotate(self.image, int(self.angle))

    def Attack(self):
        if (self.ammo > 0):
            if (self.weapon.Attack(self.equippedWeapon)):
                self.ammo -= 1

    def GetSize(self):
        return PLAYER_SIZE

    def GetPos(self):
        return [self.posX, self.posY]

    def GetAngle(self):
        return self.angle
    
    def Draw(self, screen):
        self.weapon.Draw(screen)
        screen.blit(self.rotatedImage, (self.posX, self.posY))