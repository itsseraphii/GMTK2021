import pygame
import math

BULLET_IMAGE = "./res/bullet.png"
BULLET_SPEED = 20
WEAPON_COOLDOWN = 600 # MS

class Weapon:
    def __init__(self, player):
        self.player = player
        self.playerSize = self.player.GetSize()
        self.screenSize = pygame.display.get_window_size()
        self.damage = 1
        self.name = "Revolver"
        self.bulletImage = pygame.image.load(BULLET_IMAGE)
        self.bullets = []

        self.lastShotTime = 0

    def Fire(self):
        currentTime = pygame.time.get_ticks()

        if (currentTime >= self.lastShotTime + WEAPON_COOLDOWN):
            self.lastShotTime = currentTime
            pos = self.player.GetPos()
            angle = -math.radians(self.player.GetAngle())
            self.bullets.append([self.playerSize[0] / 2 + pos[0], self.playerSize[1] + pos[1], angle])

    def ComputeNewBulletPos(self, oldX, oldY, angle):
        newX = oldX + (BULLET_SPEED * math.cos(angle))
        newY = oldY + (BULLET_SPEED * math.sin(angle))
        return [newX, newY]

    def UpdateBullets(self):
        playerPos = self.player.GetPos()

        for i in range(len(self.bullets) - 1, -1, -1):
            if (self.bullets[i][0] > self.screenSize[0] / 2 + playerPos[0] or self.bullets[i][0] < -self.screenSize[0] / 2 + playerPos[0] or self.bullets[i][1] > self.screenSize[1] / 2 + playerPos[1] or self.bullets[i][1] < -self.screenSize[1] + playerPos[1]):
                self.bullets.pop(i)

        for i in range(len(self.bullets)):
            newPos = self.ComputeNewBulletPos(self.bullets[i][0], self.bullets[i][1], self.bullets[i][2])
            self.bullets[i][0] = newPos[0]
            self.bullets[i][1] = newPos[1]
    
    def Draw(self, screen):
        self.UpdateBullets()

        for bullet in self.bullets:
            screen.blit(self.bulletImage, (bullet[0], bullet[1]))