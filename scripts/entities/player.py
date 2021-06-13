import pygame
from pygame.constants import K_a, K_d, K_s, K_w
from spriteUtils import getFrames
import math
from entities.weapon import Weapon
from pygame import Rect

SPEED = 2
IMAGE_FILE = "./res/player_gun.png"
WALKING_ANIMATION = "player_unarmed.png"
ANIMATION_SPEED = 84 # ms
PLAYER_SIZE = [32, 32]

class Player:
    def __init__(self, gameworld):
        self.gameworld = gameworld
        self.screenSize = pygame.display.get_window_size()
        self.posX, self.posY = self.screenSize[0] / 2, self.screenSize[1] / 4 * 3

        self.walking_frames = getFrames(WALKING_ANIMATION, PLAYER_SIZE)
        self.frame_counter = 0
        self.lastFrameTime = 0

        self.image = pygame.transform.scale(pygame.image.load(IMAGE_FILE), (30, 30))
        self.rotatedImage = self.image

        self.weapon = Weapon(self, gameworld)
        self.weaponInventory = ["Revolver", "Crowbar", "Assault Rifle", "Sniper"] # TODO remove start weapons
        self.equippedWeaponIndex = 0
        self.ammo = 13

    def setIsMoving(self, pressedKeys):
        if pressedKeys[K_w] or pressedKeys[K_a] or pressedKeys[K_s] or pressedKeys[K_d]:
            self.isMoving = True
        else :
            self.isMoving = False

    def Move(self, pressedKeys):
        self.setIsMoving(pressedKeys)
        if pressedKeys[K_w]:
            if (self.posY < self.screenSize[1] / 2):
                self.gameworld.IncreaseOffsetY(SPEED)
            else:
                self.posY -= SPEED
        if pressedKeys[K_a]:
            self.posX -= SPEED
        if pressedKeys[K_s]:
            if (self.posY + SPEED  < self.screenSize[1] - PLAYER_SIZE[1]):
                self.posY += SPEED
        if pressedKeys[K_d]:
            self.posX += SPEED

        currentTime = pygame.time.get_ticks()

        if (currentTime >= self.lastFrameTime + ANIMATION_SPEED and self.isMoving ):
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

    def PickupWeapon(self, weaponName):
        self.weaponInventory.append(weaponName)
    
    def SwitchWeapon(self, nextWeapon):
        if (nextWeapon): # Switch to next weapon
            self.equippedWeaponIndex = (self.equippedWeaponIndex + 1) % len(self.weaponInventory)
        else: # Switch to previous weapon
            self.equippedWeaponIndex = self.equippedWeaponIndex - 1 if (self.equippedWeaponIndex > 0) else len(self.weaponInventory) - 1

    def Attack(self):
        if (self.weapon.Attack(self.weaponInventory[self.equippedWeaponIndex], self.ammo)):
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

    def CheckCollisionWithObstacles(self):
        for ob in self.gameworld.obstacles:
            if Rect(self.posX, self.posY, 32, 32).colliderect(Rect(ob.GetY(), ob.GetX(), 32, 32)):
                return True

        return False
