import pygame
from enum import IntEnum
from math import floor, radians, cos, sin
from utils.constants import TILES_COUNT_X, TILE_SIZE, DATA_PATH, PLAYER_SIZE

SWING_SOUND_FILE = DATA_PATH + "/sounds/swing.mp3"
GUNSHOT_SOUND_FILE = DATA_PATH + "/sounds/gunshot.mp3"
EMPTY_GUN_SOUND_FILE = DATA_PATH + "/sounds/emptyGun.mp3"
BULLET_IMAGE_PATH = DATA_PATH + "/res/bullet.png"

BULLET_SPEED = 20
BULLET_SIZE = 3
BULLET_STUN_MULTIPLIER = 150

MELEE_REACH = 15
MELEE_SIZE = [TILE_SIZE * 1.5] * 2
MELEE_STUN_MULTIPLIER = 200

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
                    playerPos = self.player.GetPos()
                    angleRad = -radians(self.player.angle)

                    # [posX, posY, angle, damage, caliber]
                    self.bullets.append([PLAYER_SIZE[0] / 2 + playerPos[0], PLAYER_SIZE[1] / 2 + playerPos[1], angleRad, self.weapons[equippedWeapon][2], self.weapons[equippedWeapon][4]])

                    self.gunshotSound.play()
                    self.emptyGunSoundPlayed = False
                    self.player.game.levelController.savedRoundsFired += 1

                    return True # Decrement ammo
                
                elif (not self.emptyGunSoundPlayed):
                    self.emptyGunSoundPlayed = True
                    self.emptyGunSound.play()

            elif (not self.weapons[equippedWeapon][1]): # Melee Weapon
                playerPos = self.player.GetPos()
                angleRad = -radians(self.player.angle)

                meleeCenterX = playerPos[0] + (MELEE_REACH * cos(angleRad))
                meleeCenterY = playerPos[1] + (MELEE_REACH * sin(angleRad))

                meleeRect = pygame.Rect(((PLAYER_SIZE[0] / 2) + meleeCenterX - (MELEE_SIZE[0] / 2), (PLAYER_SIZE[1] / 2) + meleeCenterY - (MELEE_SIZE[1] / 2)), MELEE_SIZE)

                self.swingSound.play()
                
                for key in list(self.gameworld.monsters): # Check collisions with all monsters
                    monster = self.gameworld.monsters[key]

                    if (meleeRect.colliderect(monster.hitbox)):
                        monster.Stun(self.weapons[equippedWeapon][2] * MELEE_STUN_MULTIPLIER)
                        monster.Damage(self.weapons[equippedWeapon][2])

        return False # Don't decrement ammo

    def GetNextBulletPos(self, oldX, oldY, angle):
        newX = oldX + (BULLET_SPEED * cos(angle))
        newY = oldY + (BULLET_SPEED * sin(angle))
        return [newX, newY]

    def UpdateBullets(self):
        playerPos = self.player.GetPos()

        for i in range(len(self.bullets) - 1, -1, -1): # Check if the bullet is out of the screen on y axis
            if (self.bullets[i][1] > self.screenSize[1] / 2 + playerPos[1] or self.bullets[i][1] < -self.screenSize[1] + playerPos[1]):
                self.bullets.pop(i) # Delete bullet
            else:
                self.UpdateBullet(i)

    def UpdateBullet(self, id):
        newPos = self.GetNextBulletPos(self.bullets[id][0], self.bullets[id][1], self.bullets[id][2])
        bulletRect = pygame.Rect(newPos[0], newPos[1], BULLET_SIZE, BULLET_SIZE)

        for key in list(self.gameworld.monsters): # Check collisions with monsters
            monster = self.gameworld.monsters[key]

            if (bulletRect.colliderect(monster.hitbox)):
                monster.Stun(self.bullets[id][3] * BULLET_STUN_MULTIPLIER)
                monster.Damage(self.bullets[id][3])
                self.player.game.levelController.savedRoundsHit += 1

                # If the weapon uses high caliber and the monster dies, don't destroy the bullet
                if (self.bullets[id][4] < 2 or key not in self.gameworld.deadMonsters):
                    self.bullets.pop(id)
                    return
        
        # Check collisions with obstacles if the bullet is not destroyed
        bulletTileId = (TILES_COUNT_X * floor(newPos[1] / TILE_SIZE)) + (floor(newPos[0] / TILE_SIZE))

        for y in range(-1, 2): # Only checks obstacles in a 3x3 square around the bullet
            for x in range(-1, 2):
                checkedTileId = y * TILES_COUNT_X + x + bulletTileId

                if (checkedTileId in self.gameworld.obstacles and self.gameworld.obstacles[checkedTileId].resistance >= self.bullets[id][4] and bulletRect.colliderect(self.gameworld.obstacles[checkedTileId].hitbox)):
                    self.bullets.pop(id)
                    return
        
        # Continue moving bullet if it's not destroyed
        self.bullets[id][0] = newPos[0]
        self.bullets[id][1] = newPos[1]

    def Draw(self, screen):
        self.UpdateBullets()

        for bullet in self.bullets:
            screen.blit(self.bulletImage, (bullet[0], bullet[1]))

        '''# Debug info - Uncomment to show bullet hitboxes :
        for bullet in self.bullets:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(bullet[0], bullet[1], BULLET_SIZE, BULLET_SIZE)) #'''

        '''# Debug info - Uncomment to show crowbar hitbox : (Currently broken)
        if (self.meleeRect is not None):
            pygame.draw.rect(screen, (255, 0, 0), self.meleeRect, 2) #'''