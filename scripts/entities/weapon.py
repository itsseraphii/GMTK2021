import pygame
import math

BULLET_IMAGE = "./res/bullet.png"
BULLET_SPEED = 20

class Weapon:
    def __init__(self, player):
        self.player = player
        self.playerSize = self.player.GetSize()
        self.screenSize = pygame.display.get_window_size()
        self.bulletImage = pygame.image.load(BULLET_IMAGE)
        self.bullets = []

        self.CreateWeapons()
        self.lastShotTime = 0

    def CreateWeapons(self):
        self.weapons = {}
        # key: name   value: [isRanged, damage, weaponCooldown]
        self.weapons.update({"Crowbar": [False, 2, 1200]})
        self.weapons.update({"Revolver": [True, 3, 800]})
        self.weapons.update({"Assault Rifle": [True, 1, 115]})
        self.weapons.update({"Sniper": [True, 10, 2000]})

    def Attack(self, equippedWeapon):
        if (self.weapons[equippedWeapon][0]): # Ranged weapon
            currentTime = pygame.time.get_ticks()

            if (currentTime >= self.lastShotTime + self.weapons[equippedWeapon][2]):
                self.lastShotTime = currentTime
                pos = self.player.GetPos()
                angle = -math.radians(self.player.GetAngle())

                # [posX, posY, angle, damage]
                self.bullets.append([self.playerSize[0] / 2 + pos[0], self.playerSize[1] + pos[1], angle, self.weapons[equippedWeapon][1]])

                return True
        else:
            pass # Melee Weapon

        return False

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