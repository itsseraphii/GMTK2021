import pygame
from pygame.constants import K_a, K_d, K_s, K_w
from pygame import Rect
import math
from entities.weapon import WeaponController, WeaponType
from spriteUtils import GetFramesFromFile

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

        self.walkingFrames = GetFramesFromFile(WALKING_ANIMATION, PLAYER_SIZE)
        self.pistolFrames = GetFramesFromFile(PISTOL_ANIMATION, PLAYER_SIZE)
        self.rifleFrames = GetFramesFromFile(RIFLE_ANIMATION, [48, 32])
        self.sniperFrames = GetFramesFromFile(SNIPER_ANIMATION, [48, 32])
        self.frameCounter = 0
        self.lastFrameTime = 0

        self.image = self.walkingFrames[0]
        self.rotatedImage = self.image

        self.weaponController = WeaponController(self, gameworld)
        self.weaponInventory = [WeaponType.CROWBAR]
        self.equippedWeaponIndex = 0
        self.ammo = 0

        self.SetAnimation(self.weaponInventory[self.equippedWeaponIndex])

    def Move(self, pressedKeys):
        self.isMoving = pressedKeys[K_w] or pressedKeys[K_a] or pressedKeys[K_s] or pressedKeys[K_d]

        if pressedKeys[K_w]:
            if(not self.CheckCollisionWithObstacles(Rect(self.posX + PLAYER_HITBOX_SIZE[0] / 2, self.posY + PLAYER_HITBOX_SIZE[1] / 2 - SPEED, PLAYER_HITBOX_SIZE[0], PLAYER_HITBOX_SIZE[1]))):
                if (self.posY < self.screenSize[1] / 2):
                    self.gameworld.IncreaseOffsetY(SPEED)
                else:
                    self.posY -= SPEED
                
        if pressedKeys[K_a]:
            self.posX -= SPEED
            if (self.CheckCollisionWithObstacles(Rect(self.posX + PLAYER_HITBOX_SIZE[0] / 2, self.posY + PLAYER_HITBOX_SIZE[1] / 2, PLAYER_HITBOX_SIZE[0], PLAYER_HITBOX_SIZE[1]))):
                self.posX += SPEED
                
        if pressedKeys[K_s]:
            if (self.posY + SPEED  < self.screenSize[1] - PLAYER_SIZE[1]):
                self.posY += SPEED
                if (self.CheckCollisionWithObstacles(Rect(self.posX + PLAYER_HITBOX_SIZE[0] / 2, self.posY + PLAYER_HITBOX_SIZE[1] / 2, PLAYER_HITBOX_SIZE[0], PLAYER_HITBOX_SIZE[1]))):
                    self.posY -= SPEED

        if pressedKeys[K_d]:
            self.posX += SPEED
            if (self.CheckCollisionWithObstacles(Rect(self.posX + PLAYER_HITBOX_SIZE[0] / 2, self.posY + PLAYER_HITBOX_SIZE[1] / 2, PLAYER_HITBOX_SIZE[0], PLAYER_HITBOX_SIZE[1]))):
                self.posX -= SPEED

        currentTime = pygame.time.get_ticks()

        if (currentTime >= self.lastFrameTime + ANIMATION_SPEED and self.isMoving):
            self.lastFrameTime = currentTime
            self.NextFrame()

        currentHitbox = Rect(self.posX, self.posY, PLAYER_HITBOX_SIZE[0], PLAYER_HITBOX_SIZE[1])

        if (self.CheckCollisionWithMonsters(currentHitbox)):
            self.game.TriggerGameOver(False)
        else:
            self.CheckCollisionWithCollectables(currentHitbox)

    def SetAnimation(self, currentWeapon): # Change animations based on weapon held
        if currentWeapon == WeaponType.REVOLVER:
            self.currentAnimation = self.pistolFrames
        elif currentWeapon == WeaponType.RIFLE:
            self.currentAnimation = self.rifleFrames
        elif currentWeapon == WeaponType.SNIPER:
            self.currentAnimation = self.sniperFrames
        else:
            self.currentAnimation = self.walkingFrames
    
    def NextFrame(self): # Switch to the animation's next frame
        self.frameCounter = (self.frameCounter + 1) % len(self.currentAnimation)
        self.image = self.currentAnimation[self.frameCounter]

    def LookAtMouse(self, mousePos):
        relativeX, relativeY = mousePos[0] - self.posX, mousePos[1] - self.posY
        self.angle = (180 / math.pi) * -math.atan2(relativeY, relativeX)
        self.rotatedImage = pygame.transform.rotate(self.image, int(self.angle))
    
    def SwitchWeapon(self, nextWeapon):
        if (nextWeapon): # Switch to next weapon
            self.equippedWeaponIndex = (self.equippedWeaponIndex + 1) % len(self.weaponInventory)
        else: # Switch to previous weapon
            self.equippedWeaponIndex = self.equippedWeaponIndex - 1 if (self.equippedWeaponIndex > 0) else len(self.weaponInventory) - 1

        self.SetAnimation(self.weaponInventory[self.equippedWeaponIndex])

    def AddWeapon(self, ammo, duplicateAmmo, weapon):
        if (weapon not in self.weaponInventory):
            self.ammo += ammo
            self.weaponInventory.append(weapon)
            self.equippedWeaponIndex = len(self.weaponInventory) - 1
            self.SetAnimation(self.weaponInventory[self.equippedWeaponIndex])
        else:
            self.ammo += duplicateAmmo

    def Attack(self):
        if (self.weaponController.Attack(self.weaponInventory[self.equippedWeaponIndex], self.ammo)):
            self.ammo -= 1

    def GetSize(self):
        return PLAYER_SIZE

    def GetPos(self):
        return [self.posX, self.posY]

    def GetEquippedWeaponName(self):
        return self.weaponController.weapons[self.weaponInventory[self.equippedWeaponIndex]][0]
    
    def CheckCollisionWithObstacles(self, mainRect):
        for obstacle in self.gameworld.obstacles:
            if mainRect.colliderect(Rect(obstacle.posX + obstacle.offsetX, obstacle.posY + obstacle.offsetY, obstacle.width, obstacle.height)):
                return True

        return False

    def CheckCollisionWithMonsters(self, mainRect):
        for monster in self.gameworld.monsters.values():
            if mainRect.colliderect(Rect(monster.posX + monster.hitBoxOffestX, monster.posY + monster.hitBoxOffestY, monster.hitBoxWidth, monster.hitBoxHeight)):
                return True

        return False
    
    def CheckCollisionWithCollectables(self, mainRect):
        for collectable in self.gameworld.collectables.values():
            if not collectable.collected:
                if mainRect.colliderect(Rect(collectable.posX, collectable.posY, collectable.size[0], collectable.size[1])):
                    collectable.Pickup()
                    return # Max one pickup per frame

    def Draw(self, screen):
        self.weaponController.Draw(screen)
        screen.blit(self.rotatedImage, (self.posX, self.posY))

        '''# Debug info - Uncomment to show hitboxes : 
        pygame.draw.rect(screen, (255,0,0), Rect(self.posX + PLAYER_HITBOX_SIZE[0]/2, self.posY + PLAYER_HITBOX_SIZE[1]/2, PLAYER_HITBOX_SIZE[0], PLAYER_HITBOX_SIZE[1]), 2)
        # pygame.draw.circle(screen, (255,0,0), (self.posX + PLAYER_SIZE[0]/2, self.posY + PLAYER_SIZE[0]/2), PLAYER_SIZE[0]/2, 4)'''
