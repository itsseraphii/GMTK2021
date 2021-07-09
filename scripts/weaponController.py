import pygame
from enum import IntEnum
import math
from utils.constants import TILE_SIZE, DATA_PATH, PLAYER_SIZE

SWING_SOUND_FILE = DATA_PATH + "/sounds/swing.mp3"
GUNSHOT_SOUND_FILE = DATA_PATH + "/sounds/gunshot.mp3"
EMPTY_GUN_SOUND_FILE = DATA_PATH + "/sounds/emptyGun.mp3"
BULLET_IMAGE_PATH = DATA_PATH + "/res/bullet.png"

BULLET_SPEED = 20
BULLET_SIZE = 3

MELEE_SIZE = [TILE_SIZE * 1.5] * 2
MELEE_REACH = 15

class WeaponTypes(IntEnum):
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
        self.emptyGunSound = pygame.mixer.Sound(EMPTY_GUN_SOUND_FILE)

        self.CreateWeapons()
        self.lastAttackTime = 0

    def CreateWeapons(self):
        self.weapons = {}
        # key: name   value: [name, isRanged, damage, weaponCooldown, caliber]
        self.weapons[WeaponTypes.CROWBAR] = ["crowbar", False, 2, 750, 0]
        self.weapons[WeaponTypes.REVOLVER] = ["revolver", True, 3, 800, 1]
        self.weapons[WeaponTypes.RIFLE] = ["rifle", True, 1, 115, 1]
        self.weapons[WeaponTypes.SNIPER] = ["sniper", True, 8, 2000, 2]

    def Attack(self, equippedWeapon, ammo):
        currentTime = pygame.time.get_ticks()

        if (currentTime >= self.lastAttackTime + self.weapons[equippedWeapon][3]): # Attack if cooldown has passed
            self.lastAttackTime = currentTime

            if (self.weapons[equippedWeapon][1]): # Ranged weapon
                if (ammo > 0):
                    self.emptyGunSoundPlayed = False
                    playerPos = self.player.GetPos()
                    angleRad = -math.radians(self.player.angle)

                    # [posX, posY, angle, damage, caliber]
                    self.bullets.append([PLAYER_SIZE[0] / 2 + playerPos[0], PLAYER_SIZE[1] / 2 + playerPos[1], angleRad, self.weapons[equippedWeapon][2], self.weapons[equippedWeapon][4]])

                    self.gunshotSound.play()

                    return True # Decrement ammo
                
                elif (not self.emptyGunSoundPlayed):
                    self.emptyGunSoundPlayed = True
                    self.emptyGunSound.play()

            elif (not self.weapons[equippedWeapon][1]): # Melee Weapon
                playerPos = self.player.GetPos()
                angleRad = -math.radians(self.player.angle)

                meleeCenterX = playerPos[0] + (MELEE_REACH * math.cos(angleRad))
                meleeCenterY = playerPos[1] + (MELEE_REACH * math.sin(angleRad))

                meleeRect = pygame.Rect(((PLAYER_SIZE[0] / 2) + meleeCenterX - (MELEE_SIZE[0] / 2), (PLAYER_SIZE[1] / 2) + meleeCenterY - (MELEE_SIZE[1] / 2)), MELEE_SIZE)

                self.swingSound.play()
                
                for key in list(self.gameworld.monsters): # Check collisions with all monsters
                    monster = self.gameworld.monsters[key]

                    if (meleeRect.colliderect(monster.hitbox)):
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

                    if (bulletRect.colliderect(monster.hitbox)):
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

        '''# Debug info - Uncomment to show crowbar hitbox : (Brisé pour optimisations, sorry)
        if (self.meleeRect is not None):
            pygame.draw.rect(screen, (255, 0, 0), self.meleeRect, 2)'''