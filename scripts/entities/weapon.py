import pygame
from enum import IntEnum
import math
import sys

try: # Path for files when app is built by PyInstaller
    BASE_PATH = sys._MEIPASS
except:
    BASE_PATH = "."

TILE_SIZE = 32

SWING_SOUND_FILE = BASE_PATH + "/sounds/swing.mp3"
GUNSHOT_SOUND_FILE = BASE_PATH + "/sounds/gunshot.mp3"
BULLET_IMAGE = BASE_PATH + "/res/bullet.png"
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
        self.playerSize = self.player.GetSize()
        self.screenSize = pygame.display.get_window_size()
        self.bulletImage = pygame.image.load(BULLET_IMAGE)
        self.bullets = []
        self.meleeRect = None

        self.swingSound = pygame.mixer.Sound(SWING_SOUND_FILE)
        self.gunshotSound = pygame.mixer.Sound(GUNSHOT_SOUND_FILE)

        self.CreateWeapons()
        self.lastAttackTime = 0

    def CreateWeapons(self):
        self.weapons = {}
        # key: name   value: [name, isRanged, damage, weaponCooldown]
        self.weapons[WeaponType.CROWBAR] = ["Crowbar", False, 2, 750]
        self.weapons[WeaponType.REVOLVER] = ["Revolver", True, 3, 800]
        self.weapons[WeaponType.RIFLE] = ["Assault Rifle", True, 1, 115]
        self.weapons[WeaponType.SNIPER] = ["Sniper", True, 8, 2000]

    def Attack(self, equippedWeapon, ammo):
        currentTime = pygame.time.get_ticks()

        if (currentTime >= self.lastAttackTime + self.weapons[equippedWeapon][3]): # Attack if cooldown has passed
            self.lastAttackTime = currentTime
            self.meleeRect = None

            if (self.weapons[equippedWeapon][1] and ammo > 0): # Ranged weapon with ammo
                playerPos = self.player.GetPos()
                angle = -math.radians(self.player.angle)

                # [posX, posY, angle, damage]
                self.bullets.append([self.playerSize[0] / 2 + playerPos[0], self.playerSize[1] + playerPos[1], angle, self.weapons[equippedWeapon][2]])

                self.gunshotSound.play()

                return True # Decrement ammo

            # TODO Cleanup le elif
            elif (not self.weapons[equippedWeapon][1]): # Melee Weapon 
                
                ### Rect hitbox generation of crowbar
                # translate l'angle en full 360
                NB_SEPARATORS = 8
                MELEE_REACH = 20
                angle = self.player.angle
                if(angle < 0): angle = 360 + angle
                
                # Décalage des quadrants
                angle += (360/NB_SEPARATORS)/2
                angle %= 360
                for i in range(NB_SEPARATORS) :
                    if angle >= 360/NB_SEPARATORS * i and angle < 360/NB_SEPARATORS*(i+1):
                        break
                meleePos = 0
                playerPos = self.player.GetPos()
                if   i == 0:
                    meleePos = [playerPos[0] + MELEE_REACH, playerPos[1]]
                elif i == 1:
                    meleePos = [playerPos[0] + MELEE_REACH/2, playerPos[1] - MELEE_REACH/2]
                elif i == 2:
                    meleePos = [playerPos[0], playerPos[1] - MELEE_REACH]
                elif i == 3:
                    meleePos = [playerPos[0] - MELEE_REACH/2, playerPos[1] - MELEE_REACH/2]
                elif i == 4:
                    meleePos = [playerPos[0] - MELEE_REACH, playerPos[1]]
                elif i == 5:
                    meleePos = [playerPos[0] - MELEE_REACH /2, playerPos[1] + MELEE_REACH /2]
                elif i == 6:
                    meleePos = [playerPos[0], playerPos[1] + MELEE_REACH]
                elif i == 7:
                    meleePos = [playerPos[0] + MELEE_REACH /2, playerPos[1] + MELEE_REACH /2]                

                self.meleeRect = pygame.Rect((meleePos[0], meleePos[1]), MELEE_SIZE)
                self.swingSound.play()

                for key in list(self.gameworld.monsters): # Check collisions with multiple monsters
                    if (pygame.Rect(self.gameworld.monsters[key].posX, self.gameworld.monsters[key].posY, self.gameworld.monsters[key].size[0], self.gameworld.monsters[key].size[1]).colliderect(self.meleeRect)):
                        self.gameworld.monsters[key].Stun(self.weapons[equippedWeapon][2] * 200) # More stun than ranged weapons
                        self.gameworld.monsters[key].Damage(self.weapons[equippedWeapon][2])
        return False

    def GetNextBulletPos(self, oldX, oldY, angle):
        newX = oldX + (BULLET_SPEED * math.cos(angle))
        newY = oldY + (BULLET_SPEED * math.sin(angle))
        return [newX, newY]

    def UpdateBullets(self):
        playerPos = self.player.GetPos()

        for i in range(len(self.bullets) - 1, -1, -1): # Check bullet out of screen
            if (self.bullets[i][0] > self.screenSize[0] / 2 + playerPos[0] or self.bullets[i][0] < -self.screenSize[0] / 2 + playerPos[0] or self.bullets[i][1] > self.screenSize[1] / 2 + playerPos[1] or self.bullets[i][1] < -self.screenSize[1] + playerPos[1]):
                self.bullets.pop(i)
            else:
                newPos = self.GetNextBulletPos(self.bullets[i][0], self.bullets[i][1], self.bullets[i][2])
                bulletRect = pygame.Rect(newPos[0], newPos[1], BULLET_SIZE, BULLET_SIZE)
                hasHit = False

                for monster in self.gameworld.monsters.values(): # Check collisions with monsters
                    if (pygame.Rect(monster.posX, monster.posY, monster.size[0], monster.size[1]).colliderect(bulletRect)):
                        monster.Stun(self.bullets[i][3] * 150)
                        monster.Damage(self.bullets[i][3])
                        self.bullets.pop(i) # Delete bullet
                        hasHit = True
                        break
                
                if (not hasHit): # Continue moving bullet
                    self.bullets[i][0] = newPos[0]
                    self.bullets[i][1] = newPos[1]
    
    def Draw(self, screen):
        self.UpdateBullets()

        for bullet in self.bullets:
            screen.blit(self.bulletImage, (bullet[0], bullet[1]))

        '''# Debug info - Uncomment to show crowbar hitbox :
        if(self.meleeRect is not None):
            pygame.draw.rect(screen, (255,0,0), self.meleeRect, 2)'''