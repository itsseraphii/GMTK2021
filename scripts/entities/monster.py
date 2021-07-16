import pygame
from pygame import Rect
from random import randint as RandInt, uniform as RandFloat
from math import sqrt, sin, cos, atan2, degrees
from enum import IntEnum
from utils.constants import PLAYER_HITBOX_SIZE, TILE_SIZE

class MonsterTypes(IntEnum):
    ZOMBIE = 165
    FATBOI = 166

class Monster:
    def __init__(self, id, monsterType, spawnLocation, gameworld):
        self.id = id
        self.type = monsterType
        self.gameworld = gameworld
        self.posX, self.posY = spawnLocation[0], spawnLocation[1]

        if (monsterType == MonsterTypes.FATBOI):
            self.speed = 1
            self.animationSpeed = 150 # ms
            self.targetAccuracy = 2 # Distance from target, lower is better
            self.targetCooldown = 1750 # ms
            self.size = [64, 64]
            self.health = 9
            imageName = "monster"
            deathSoundName = "meatDeath2"

            # Hitbox Info
            self.hitBoxWidth = 40
            self.hitBoxHeight = 40
            self.hitBoxOffestX = 12
            self.hitBoxOffestY = 12

        else:
            self.speed = 1.5
            self.animationSpeed = 84
            self.targetAccuracy = 3
            self.targetCooldown = 1250
            self.size = [32, 32]
            self.health = 6
            imageName = "zombie"
            deathSoundName = "meatDeath1"

            # Hitbox Info
            self.hitBoxWidth = 22
            self.hitBoxHeight = 22
            self.hitBoxOffestX = 5
            self.hitBoxOffestY = 5

        self.hitSounds = [self.gameworld.entitySounds["meatSlap1"], self.gameworld.entitySounds["meatSlap2"], self.gameworld.entitySounds["meatSlap3"]]
        self.deathSound = self.gameworld.entitySounds[deathSoundName]

        self.animation = self.gameworld.entityImages[imageName]
        self.target = gameworld.player.GetPos()
        self.obstacleSpeed = self.speed * 0.15
        self.nextTargetUpdate = -9999
        self.nextFrameTime = 0
        self.frameCounter = 0
        self.lastHitTime = 0
        self.angle = 0

        self.NextFrame()
        self.UpdateHitbox()

    def Damage(self, damage):
        self.health -= damage

        if (self.health > 0):
            self.hitSounds[RandInt(0, 2)].play()
        else:
            self.gameworld.deadMonsters.append(self.id) # Prevents respawn
            self.gameworld.monsters.pop(self.id)
            self.deathSound.play()
            self.gameworld.player.game.levelController.savedKills += 1

    def Stun(self, timeMS):
        self.lastHitTime = pygame.time.get_ticks() + timeMS

    def Move(self):
        currentTime = pygame.time.get_ticks()
        timeOver = self.gameworld.player.game.timeOver

        if (self.nextTargetUpdate < currentTime): # Update target pos
            self.nextTargetUpdate = currentTime + self.targetCooldown
            playerPos = self.gameworld.player.GetPos()

            if (timeOver or sqrt((self.posX - playerPos[0]) ** 2 + (self.posY - playerPos[1]) ** 2) < 160): # Close to the player
                self.target = playerPos
            else: # Choose a random target in a circle around the player
                targetAngle = RandFloat(0, 6.29) # 0 - 360 in radians
                self.target[0] = self.targetAccuracy * TILE_SIZE * sin(targetAngle) + (PLAYER_HITBOX_SIZE[0] / 2) + playerPos[0]
                self.target[1] = self.targetAccuracy * TILE_SIZE * cos(targetAngle) + (PLAYER_HITBOX_SIZE[1] / 2) + playerPos[1]

        if (self.lastHitTime < currentTime):
            if (self.nextFrameTime < currentTime):
                self.nextFrameTime = currentTime + self.animationSpeed
                self.UpdateAngle(self.gameworld.player.GetPos())
                self.NextFrame()

            if (self.target[0] > self.posX + 1):
                obstacleHitbox = Rect(self.posX + self.speed + self.hitBoxOffestX, self.posY + self.hitBoxOffestY, self.hitBoxWidth, self.hitBoxHeight)
                collisionType = self.GetObstacleCollision(obstacleHitbox)

                if (collisionType == 0): # No obstacle
                    self.posX += self.speed
                elif (timeOver and collisionType != 2): # 60 seconds are over and the obstacle is not the map border
                    self.posX += self.obstacleSpeed # Slow movement

            elif (self.target[0] < self.posX - 1):
                obstacleHitbox = Rect(self.posX - self.speed + self.hitBoxOffestX, self.posY + self.hitBoxOffestY, self.hitBoxWidth, self.hitBoxHeight)
                collisionType = self.GetObstacleCollision(obstacleHitbox)

                if (collisionType == 0):
                    self.posX -= self.speed
                elif (timeOver and collisionType != 2):
                    self.posX -= self.obstacleSpeed
            
            if (self.target[1] > self.posY + 1):
                obstacleHitbox = Rect(self.posX + self.hitBoxOffestX, self.posY + self.speed + self.hitBoxOffestY, self.hitBoxWidth, self.hitBoxHeight)
                collisionType = self.GetObstacleCollision(obstacleHitbox)

                if (collisionType == 0):
                    self.posY += self.speed
                elif (timeOver and collisionType != 2):
                    self.posY += self.obstacleSpeed

            elif (self.target[1] < self.posY - 1):
                obstacleHitbox = Rect(self.posX + self.hitBoxOffestX, self.posY - self.speed + self.hitBoxOffestY, self.hitBoxWidth, self.hitBoxHeight)
                collisionType = self.GetObstacleCollision(obstacleHitbox)

                if (collisionType == 0):
                    self.posY -= self.speed
                elif (timeOver and collisionType != 2):
                    self.posY -= self.obstacleSpeed

        self.UpdateHitbox()

    def NextFrame(self):
        self.frameCounter = (self.frameCounter + 1) % len(self.animation)
        self.image = pygame.transform.rotate(self.animation[self.frameCounter], int(-degrees(self.angle)))

    def UpdateAngle(self, playerPos):
        diffX = playerPos[0] - self.posX
        diffY = playerPos[1] - self.posY
        self.angle = atan2(diffY, diffX)

    def UpdateHitbox(self):
        spriteRect = self.image.get_rect()
        self.hitbox = Rect((spriteRect.width / 2) - (self.hitBoxWidth / 2) + self.posX, (spriteRect.height / 2) - (self.hitBoxHeight / 2) + self.posY, self.hitBoxWidth, self.hitBoxHeight)

    def GetObstacleCollision(self, mainRect):
        collisionType = 0

        for obstacle in self.gameworld.obstacles:
            if (obstacle.posY < 2 * TILE_SIZE + self.posY):
                if mainRect.colliderect(obstacle.hitbox):
                    if (obstacle.resistance < 3):
                        collisionType = 1
                    else:
                        return 2
            else:                
                return collisionType

        return collisionType

    def Draw(self, screen):
        screen.blit(self.image, (self.posX, self.posY))

        '''# Debug info - Uncomment to show hitboxes : 
        pygame.draw.rect(screen, (0, 0, 255), Rect(self.posX + self.hitBoxOffestX, self.posY + self.hitBoxOffestY, self.hitBoxWidth, self.hitBoxHeight), 2) # Internal hitbox (obstacles)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2) # External hitbox (bullets, crowbar and player) #'''