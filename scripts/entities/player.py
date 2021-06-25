import pygame
from pygame.constants import K_a, K_d, K_s, K_w
from pygame import Rect
import math
import sys
from entities.weapon import Weapon
from spriteUtils import GetFrames

try: # Path for files when app is built by PyInstaller
    BASE_PATH = sys._MEIPASS
except:
    BASE_PATH = "."

PISTOL_ANIMATION = "playerPistol.png"
RIFLE_ANIMATION = "playerRifle.png"
SNIPER_ANIMATION = "playerSniper.png"
WALKING_ANIMATION = "playerUnarmed.png"

SPEED = 2
ANIMATION_SPEED = 84 # ms
PLAYER_SIZE = [32, 32]
PLAYER_HITBOX_SIZE = [20,20]

class Player:
    def __init__(self, game, gameworld):
        self.game = game
        self.gameworld = gameworld
        self.screenSize = pygame.display.get_window_size()
        self.posX, self.posY = self.screenSize[0] / 2, self.screenSize[1] / 4 * 3

        self.walking_frames = GetFrames(WALKING_ANIMATION, PLAYER_SIZE)
        self.pistol_frames = GetFrames(PISTOL_ANIMATION, PLAYER_SIZE)
        self.rifle_frames = GetFrames(RIFLE_ANIMATION, [48, 32])
        self.sniper_frames = GetFrames(SNIPER_ANIMATION, [48, 32])
        self.frame_counter = 0
        self.lastFrameTime = 0

        self.image = self.walking_frames[0]
        self.rotatedImage = self.image

        self.weapon = Weapon(self, gameworld)
        self.weaponInventory = ["Crowbar"]
        self.equippedWeaponIndex = 0
        self.ammo = 0

    def SetIsMoving(self, pressedKeys):
        if pressedKeys[K_w] or pressedKeys[K_a] or pressedKeys[K_s] or pressedKeys[K_d]:
            self.isMoving = True
        else:
            self.isMoving = False

    def Move(self, pressedKeys):
        self.SetIsMoving(pressedKeys)

        if pressedKeys[K_w]:
            if(not self.CheckCollisionWithObstacles(Rect(self.posX + PLAYER_HITBOX_SIZE[0]/2, self.posY + PLAYER_HITBOX_SIZE[1]/2 - SPEED, PLAYER_HITBOX_SIZE[0], PLAYER_HITBOX_SIZE[1]))):
                if (self.posY < self.screenSize[1] / 2):
                    self.gameworld.IncreaseOffsetY(SPEED)
                else:
                    self.posY -= SPEED
                
        if pressedKeys[K_a]:
            self.posX -= SPEED
            if (self.CheckCollisionWithObstacles(Rect(self.posX + PLAYER_HITBOX_SIZE[0]/2, self.posY + PLAYER_HITBOX_SIZE[1]/2, PLAYER_HITBOX_SIZE[0], PLAYER_HITBOX_SIZE[1]))):
                self.posX += SPEED
                
        if pressedKeys[K_s]:
            if (self.posY + SPEED  < self.screenSize[1] - PLAYER_SIZE[1]):
                self.posY += SPEED
                if (self.CheckCollisionWithObstacles(Rect(self.posX + PLAYER_HITBOX_SIZE[0]/2, self.posY + PLAYER_HITBOX_SIZE[1]/2, PLAYER_HITBOX_SIZE[0], PLAYER_HITBOX_SIZE[1]))):
                    self.posY -= SPEED

        if pressedKeys[K_d]:
            self.posX += SPEED
            if (self.CheckCollisionWithObstacles(Rect(self.posX + PLAYER_HITBOX_SIZE[0]/2, self.posY + PLAYER_HITBOX_SIZE[1]/2, 
                PLAYER_HITBOX_SIZE[0], PLAYER_HITBOX_SIZE[1]))):
                self.posX -= SPEED

        currentTime = pygame.time.get_ticks()

        if (currentTime >= self.lastFrameTime + ANIMATION_SPEED and self.isMoving):
            self.lastFrameTime = currentTime
            self.NextFrame()

        if (self.CheckCollisionWithMonsters(Rect(self.posX, self.posY, PLAYER_HITBOX_SIZE[0], PLAYER_HITBOX_SIZE[1]))):
            self.game.TriggerGameOver(False)

        self.CheckCollisionWithCollectables(Rect(self.posX, self.posY, PLAYER_HITBOX_SIZE[0], PLAYER_HITBOX_SIZE[1]))
    
    def NextFrame(self):
        # Change image based on weapon held
        # TODO change all weapon pointers to an ENUM
        if self.weaponInventory[self.equippedWeaponIndex] == "Revolver":
            current_animation = self.pistol_frames
        elif self.weaponInventory[self.equippedWeaponIndex] == "Assault Rifle":
            current_animation = self.rifle_frames
        elif self.weaponInventory[self.equippedWeaponIndex] == "Sniper":
            current_animation = self.sniper_frames
        else:
            current_animation = self.walking_frames

        self.frame_counter += 1

        if (self.frame_counter >= len(current_animation)) :
            self.frame_counter = 0

        self.image = current_animation[self.frame_counter]

    def LookAtMouse(self, mousePos):
        relativeX, relativeY = mousePos[0] - self.posX, mousePos[1] - self.posY
        self.angle = (180 / math.pi) * -math.atan2(relativeY, relativeX)
        self.rotatedImage = pygame.transform.rotate(self.image, int(self.angle))
    
    def SwitchWeapon(self, nextWeapon):
        if (nextWeapon): # Switch to next weapon
            self.equippedWeaponIndex = (self.equippedWeaponIndex + 1) % len(self.weaponInventory)
        else: # Switch to previous weapon
            self.equippedWeaponIndex = self.equippedWeaponIndex - 1 if (self.equippedWeaponIndex > 0) else len(self.weaponInventory) - 1

    def AddWeapon(self, ammo, duplicateAmmo, weaponName):
        if (weaponName not in self.weaponInventory):
            self.ammo += ammo
            self.weaponInventory.append(weaponName)
            self.equippedWeaponIndex = len(self.weaponInventory) - 1
        else:
            self.ammo += duplicateAmmo

    def Attack(self):
        if (self.weapon.Attack(self.weaponInventory[self.equippedWeaponIndex], self.ammo)):
            self.ammo -= 1

    def GetSize(self):
        return PLAYER_SIZE

    def GetPos(self):
        return [self.posX, self.posY]
    
    def Draw(self, screen):
        self.weapon.Draw(screen)
        screen.blit(self.rotatedImage, (self.posX, self.posY))

        '''# Debug info - Uncomment to show hitboxes : 
        pygame.draw.rect(screen, (255,0,0), Rect(self.posX + PLAYER_HITBOX_SIZE[0]/2, self.posY + PLAYER_HITBOX_SIZE[1]/2, PLAYER_HITBOX_SIZE[0], PLAYER_HITBOX_SIZE[1]), 2)
        # pygame.draw.circle(screen, (255,0,0), (self.posX + PLAYER_SIZE[0]/2, self.posY + PLAYER_SIZE[0]/2), PLAYER_SIZE[0]/2, 4)'''

    def CheckCollisionWithObstacles(self, rect):
        for ob in self.gameworld.obstacles:
            if rect.colliderect(Rect(ob.GetX() + ob.GetHitBoxOffsetX(), ob.GetY() + ob.GetHitBoxOffsetY(), ob.GetHitboxWidth(), ob.GetHitboxLength())):
                return True

        return False

    def CheckCollisionWithMonsters(self, playerRect):
        for monster in self.gameworld.monsters.values():
            if playerRect.colliderect(Rect(monster.posX + monster.hitBoxOffestX, monster.posY + monster.hitBoxOffestY, monster.hitBoxWidth, monster.hitBoxLength)):
                return True

        return False
    
    def CheckCollisionWithCollectables(self, playerRect):
        for collectable in self.gameworld.collectables.values():
            if not collectable.collected:
                if playerRect.colliderect(Rect(collectable.posX, collectable.posY, collectable.size[0], collectable.size[1])):
                    collectable.Pickup()