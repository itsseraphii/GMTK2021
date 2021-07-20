import pygame
from pygame.constants import K_a, K_d, K_s, K_w
from pygame import Rect
from math import pi, atan2, floor
from weaponController import WeaponController, WeaponTypes
from utils.spriteUtils import GetFramesFromFile
from utils.constants import PLAYER_SIZE, PLAYER_HITBOX_SIZE, TILES_COUNT_X, TILE_SIZE

SPEED = 2
ANIMATION_SPEED = 84 # ms

class Player:
    def __init__(self, game, gameworld):
        self.game = game
        self.gameworld = gameworld
        self.screenSize = pygame.display.get_window_size()

        spawn = self.gameworld.FindPlayerSpawn()
        self.posX, self.posY = spawn[0], spawn[1]

        self.walkingFrames = GetFramesFromFile("playerUnarmed.png", PLAYER_SIZE)
        self.pistolFrames = GetFramesFromFile("playerPistol.png", PLAYER_SIZE)
        self.rifleFrames = GetFramesFromFile("playerRifle.png", PLAYER_SIZE)
        self.sniperFrames = GetFramesFromFile("playerSniper.png", PLAYER_SIZE)
        self.animFrameCounter = 0
        self.nextFrameTime = 0

        self.image = self.walkingFrames[0]
        self.rotatedImage = self.image

        self.weaponController = WeaponController(self, gameworld)
        self.weaponInventory = [WeaponTypes.CROWBAR]
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

        if (currentTime >= self.nextFrameTime and self.isMoving):
            self.nextFrameTime = currentTime + ANIMATION_SPEED
            self.NextFrame()

        currentHitbox = Rect(PLAYER_HITBOX_SIZE[0] / 2 + self.posX, PLAYER_HITBOX_SIZE[1] / 2 + self.posY, PLAYER_HITBOX_SIZE[0], PLAYER_HITBOX_SIZE[1])

        if (self.game.frameCounter % 2 == 0 and self.CheckCollisionWithMonsters(currentHitbox)): # Check collisions with monsters on even frames
            self.game.levelController.savedDeaths += 1
            self.game.TriggerGameOver(False)
        elif (self.game.frameCounter % 2 == 1): # Check collisions with collectables on odd frames
            self.CheckCollisionWithCollectables(currentHitbox)

    def SetAnimation(self, currentWeapon): # Change animations based on weapon held
        if currentWeapon == WeaponTypes.REVOLVER:
            self.currentAnimation = self.pistolFrames
        elif currentWeapon == WeaponTypes.RIFLE:
            self.currentAnimation = self.rifleFrames
        elif currentWeapon == WeaponTypes.SNIPER:
            self.currentAnimation = self.sniperFrames
        else:
            self.currentAnimation = self.walkingFrames

        self.NextFrame() # Start new animation
    
    def NextFrame(self): # Switch to the animation's next frame
        self.animFrameCounter = (self.animFrameCounter + 1) % len(self.currentAnimation)
        self.image = self.currentAnimation[self.animFrameCounter]

    def LookAtMouse(self, mousePos):
        relativeX, relativeY = mousePos[0] - (PLAYER_SIZE[0] / 2 + self.posX), mousePos[1] - (PLAYER_SIZE[1] / 2 + self.posY)
        self.angle = (180 / pi) * -atan2(relativeY, relativeX)
        self.rotatedImage = pygame.transform.rotate(self.image, floor(self.angle))
    
    def SwitchWeapon(self, nextWeapon):
        if (nextWeapon): # Switch to next weapon
            self.equippedWeaponIndex = (self.equippedWeaponIndex + 1) % len(self.weaponInventory)
        else: # Switch to previous weapon
            self.equippedWeaponIndex = self.equippedWeaponIndex - 1 if (self.equippedWeaponIndex > 0) else len(self.weaponInventory) - 1

        self.SetAnimation(self.weaponInventory[self.equippedWeaponIndex])
        self.weaponController.emptyGunSoundPlayed = False

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

    def GetPos(self):
        return [self.posX, self.posY]

    def GetEquippedWeaponName(self):
        return self.weaponController.weapons[self.weaponInventory[self.equippedWeaponIndex]][0]
    
    def CheckCollisionWithObstacles(self, mainRect):
        playerTileId = (TILES_COUNT_X * floor(self.posY / TILE_SIZE)) + (floor(self.posX / TILE_SIZE))

        for y in range(-1, 3): # Only checks obstacles in a 4x4 square around the player
            for x in range(-1, 3):
                checkedTileId = y * TILES_COUNT_X + x + playerTileId

                if (checkedTileId in self.gameworld.obstacles and mainRect.colliderect(self.gameworld.obstacles[checkedTileId].hitbox)):
                    return True

        return False

    def CheckCollisionWithMonsters(self, mainRect):
        for monster in self.gameworld.monsters.values():
            if mainRect.colliderect(monster.hitbox):
                return False

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
        pygame.draw.rect(screen, (255, 0, 0), Rect(PLAYER_HITBOX_SIZE[0] / 2 + self.posX, PLAYER_HITBOX_SIZE[1] / 2 + self.posY, PLAYER_HITBOX_SIZE[0], PLAYER_HITBOX_SIZE[1]), 2) #'''