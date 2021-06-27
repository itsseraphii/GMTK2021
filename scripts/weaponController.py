import pygame
from enum import IntEnum
import math
from utils.constants import TILE_SIZE, BASE_PATH, PLAYER_SIZE

SWING_SOUND_FILE = BASE_PATH + "/sounds/swing.mp3"
GUNSHOT_SOUND_FILE = BASE_PATH + "/sounds/gunshot.mp3"
BULLET_IMAGE_PATH = BASE_PATH + "/res/bullet.png"
BULLET_SPEED = 20
BULLET_SIZE = 3

MELEE_OFFSET_XY = -(TILE_SIZE / 2)
MELEE_SIZE = [TILE_SIZE * 1.5] * 2

class WeaponType(IntEnum):
    CROWBAR = 0
    REVOLVER = 1
    RIFLE = 2
    SNIPER = 3

class WeaponController:
    def __init__(self, player, gameworld):
        self.player = player
        self.gameworld = gameworld
        self.screenSize = pygame.display.get_window_size()
        self.bulletImage = pygame.image.load(BULLET_IMAGE_PATH).convert()
        self.bullets = []

        self.swingSound = pygame.mixer.Sound(SWING_SOUND_FILE)
        self.gunshotSound = pygame.mixer.Sound(GUNSHOT_SOUND_FILE)

        self.CreateWeapons()
        self.lastAttackTime = 0

    def CreateWeapons(self):
        self.weapons = {}
        # key: name   value: [name, isRanged, damage, weaponCooldown, caliber]
        self.weapons[WeaponType.CROWBAR] = ["Crowbar", False, 2, 750, 0]
        self.weapons[WeaponType.REVOLVER] = ["Revolver", True, 3, 800, 1]
        self.weapons[WeaponType.RIFLE] = ["Assault Rifle", True, 1, 115, 1]
        self.weapons[WeaponType.SNIPER] = ["Sniper", True, 8, 2000, 2]

    def Attack(self, equippedWeapon, ammo):
        currentTime = pygame.time.get_ticks()

        if (currentTime >= self.lastAttackTime + self.weapons[equippedWeapon][3]): # Attack if cooldown has passed
            self.lastAttackTime = currentTime

            if (self.weapons[equippedWeapon][1] and ammo > 0): # Ranged weapon with ammo
                playerPos = self.player.GetPos()
                angle = -math.radians(self.player.angle)

                # [posX, posY, angle, damage, caliber]
                self.bullets.append([PLAYER_SIZE[0] / 2 + playerPos[0], PLAYER_SIZE[1] / 2 + playerPos[1], angle, self.weapons[equippedWeapon][2], self.weapons[equippedWeapon][4]])

                self.gunshotSound.play()

                return True # Decrement ammo

            # TODO Cleanup ce elif
            elif (not self.weapons[equippedWeapon][1]): # Melee Weapon 
                ### Rect hitbox generation of crowbar
                # translate l'angle en full 360
                NB_SEPARATORS = 8
                MELEE_REACH = 20
                angle = self.player.angle
                if(angle < 0): angle = 360 + angle
                
                # Décalage des quadrants
                angle += (360 / NB_SEPARATORS) / 2
                angle %= 360

                for i in range(NB_SEPARATORS) :
                    if angle >= 360 / NB_SEPARATORS * i and angle < 360 / NB_SEPARATORS * (i + 1):
                        break

                meleePos = 0
                playerPos = self.player.GetPos()
                if   i == 0:
                    meleePos = [playerPos[0] + MELEE_REACH, playerPos[1]]
                elif i == 1:
                    meleePos = [playerPos[0] + MELEE_REACH / 2, playerPos[1] - MELEE_REACH / 2]
                elif i == 2:
                    meleePos = [playerPos[0], playerPos[1] - MELEE_REACH]
                elif i == 3:
                    meleePos = [playerPos[0] - MELEE_REACH / 2, playerPos[1] - MELEE_REACH / 2]
                elif i == 4:
                    meleePos = [playerPos[0] - MELEE_REACH, playerPos[1]]
                elif i == 5:
                    meleePos = [playerPos[0] - MELEE_REACH / 2, playerPos[1] + MELEE_REACH / 2]
                elif i == 6:
                    meleePos = [playerPos[0], playerPos[1] + MELEE_REACH]
                elif i == 7:
                    meleePos = [playerPos[0] + MELEE_REACH / 2, playerPos[1] + MELEE_REACH / 2]                

                self.swingSound.play()

                meleeRect = pygame.Rect((meleePos[0], meleePos[1]), MELEE_SIZE)
                
                for key in list(self.gameworld.monsters): # Check collisions with multiple monsters
                    monster = self.gameworld.monsters[key]

                    if (meleeRect.colliderect(pygame.Rect(monster.posX + monster.hitBoxOffestX, monster.posY + monster.hitBoxOffestY, monster.hitBoxWidth, monster.hitBoxHeight))):
                        monster.Stun(self.weapons[equippedWeapon][2] * 200) # More stun than ranged weapons
                        monster.Damage(self.weapons[equippedWeapon][2])

        return False

    def GetNextBulletPos(self, oldX, oldY, angle):
        newX = oldX + (BULLET_SPEED * math.cos(angle))
        newY = oldY + (BULLET_SPEED * math.sin(angle))
        return [newX, newY]

    def UpdateBullets(self):
        playerPos = self.player.GetPos()

        for i in range(len(self.bullets) - 1, -1, -1): # Check if the bullet is out of the screen on y axis
            if (self.bullets[i][1] > self.screenSize[1] / 2 + playerPos[1] or self.bullets[i][1] < -self.screenSize[1] + playerPos[1]):
                self.bullets.pop(i) # Delete bullet
            else:
                newPos = self.GetNextBulletPos(self.bullets[i][0], self.bullets[i][1], self.bullets[i][2])
                bulletRect = pygame.Rect(newPos[0], newPos[1], BULLET_SIZE, BULLET_SIZE)
                isDestroyed = False

                for key in list(self.gameworld.monsters): # Check collisions with monsters
                    monster = self.gameworld.monsters[key]

                    if (bulletRect.colliderect(pygame.Rect(monster.posX + monster.hitBoxOffestX, monster.posY + monster.hitBoxOffestY, monster.hitBoxWidth, monster.hitBoxHeight))):
                        monster.Stun(self.bullets[i][3] * 150)
                        monster.Damage(self.bullets[i][3])

                        if (self.bullets[i][4] < 2 or key not in self.gameworld.deadMonsters): # If the weapon uses high caliber and the monster dies, don't destroy the bullet
                            self.bullets.pop(i)
                            isDestroyed = True
                            break

                if (not isDestroyed): # Check collisions with obstacles
                    for obstacle in self.gameworld.obstacles: # Check collisions with obstacles
                        if (obstacle.resistance >= self.bullets[i][4] and bulletRect.colliderect(pygame.Rect(obstacle.posX + obstacle.offsetX, obstacle.posY + obstacle.offsetY, obstacle.width, obstacle.height))):
                            self.bullets.pop(i)
                            isDestroyed = True
                            break
                
                if (not isDestroyed): # Continue moving bullet
                    self.bullets[i][0] = newPos[0]
                    self.bullets[i][1] = newPos[1]

    def Draw(self, screen):
        self.UpdateBullets()

        for bullet in self.bullets:
            screen.blit(self.bulletImage, (bullet[0], bullet[1]))

        '''# Debug info - Uncomment to show crowbar hitbox : (Brisé pour optimisiations, sorry)
        if (self.meleeRect is not None):
            pygame.draw.rect(screen, (255, 0, 0), self.meleeRect, 2)'''