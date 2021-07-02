import pygame
from pygame import Rect
import random
import math
from enum import IntEnum
from utils.constants import TILE_SIZE

TURN_ANGLE = 2

class MonsterType(IntEnum):
    ZOMBIE = 165
    FATBOI = 166

class Monster:
    def __init__(self, id, monsterType, spawnLocation, gameworld):
        self.gameworld = gameworld
        self.id = id
        self.type = monsterType
        self.posX = spawnLocation[0]
        self.posY = spawnLocation[1]
        self.lastHitTime = 0
        self.angle = 0

        if (monsterType == MonsterType.FATBOI):
            self.speed = 1
            self.animationSpeed = 150
            self.accuracy = 2
            self.targetCooldown = 1750 #ms
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
            self.accuracy = 3 # Range of target, lower is better
            self.targetCooldown = 1250 #ms
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
        self.lastFrameTime = 0
        self.lastTargetUpdate = 0
        self.target = gameworld.player.GetPos()
        self.frameCounter = 0
        self.NextFrame()

    def Damage(self, damage):
        self.health -= damage

        if (self.health > 0):
            self.hitSounds[random.randint(0, 2)].play()
        else:
            self.gameworld.deadMonsters.append(self.id) # Prevents respawn
            self.gameworld.monsters.pop(self.id)
            self.deathSound.play()
            self.gameworld.player.game.levelController.savedKills += 1

    def Stun(self, timeMS):
        self.lastHitTime = pygame.time.get_ticks() + timeMS

    def Move(self): # TODO optimiser et cleanup
        currentTime = pygame.time.get_ticks()

        if currentTime > self.lastTargetUpdate + self.targetCooldown :
            self.lastTargetUpdate = currentTime
            playerLocation = self.gameworld.player.GetPos()

            # Faraway
            if abs(playerLocation[0]) - abs(self.posX) > 100 or abs(playerLocation[1]) - abs(self.posY) > 100 :
                # Draws a zone around the player, choosing a random angle to select a target
                targetAngle = math.degrees(random.uniform(0, 6.29))
                self.target[0] = playerLocation[0] + (self.accuracy * TILE_SIZE) * math.sin(targetAngle)
                self.target[1] = playerLocation[1] + (self.accuracy * TILE_SIZE) * math.cos(targetAngle)
            else: # straight to the player
                self.target = playerLocation

        if (self.lastHitTime < pygame.time.get_ticks()):
            if (currentTime >= self.lastFrameTime + self.animationSpeed ):
                self.lastFrameTime = currentTime
                self.NextFrame()

            if self.target[0] > self.posX :
                self.posX += self.speed
                if (self.angle > 90 and self.angle <= 270): 
                    self.angle -= TURN_ANGLE
                elif (self.angle < 90 or self.angle > 270): 
                    self.angle += TURN_ANGLE
                if(self.gameworld.player.CheckCollisionWithObstacles( 
                Rect(
                    self.posX + self.hitBoxOffestX, 
                    self.posY + self.hitBoxOffestY,
                    self.hitBoxWidth, self.hitBoxHeight
                    ))):
                    self.posX -= self.speed
            elif self.target[0] < self.posX :
                self.posX -= self.speed
                if (self.angle > 270 or self.angle <= 90): 
                    self.angle -= TURN_ANGLE

                elif (self.angle < 270 and self.angle > 90): 
                    self.angle += TURN_ANGLE
                if(self.gameworld.player.CheckCollisionWithObstacles( 
                Rect(
                    self.posX + self.hitBoxOffestX, 
                    self.posY + self.hitBoxOffestY,
                    self.hitBoxWidth, self.hitBoxHeight
                    ))):
                    self.posX += self.speed
            
            if self.target[1] > self.posY :
                self.posY += self.speed
                if (self.angle > 180): 
                    self.angle += TURN_ANGLE
                elif (self.angle <= 180): 
                    self.angle -= TURN_ANGLE
                if(self.gameworld.player.CheckCollisionWithObstacles( 
                Rect(
                    self.posX + self.hitBoxOffestX, 
                    self.posY + self.hitBoxOffestY,
                    self.hitBoxWidth, self.hitBoxHeight
                    ))):
                    self.posY -= self.speed
            elif self.target[1] < self.posY :
                self.posY -= self.speed
                if (self.angle < 180): 
                    self.angle += TURN_ANGLE
                elif (self.angle >= 180): 
                    self.angle -= TURN_ANGLE
                if(self.gameworld.player.CheckCollisionWithObstacles( 
                Rect(
                    self.posX + self.hitBoxOffestX, 
                    self.posY + self.hitBoxOffestY,
                    self.hitBoxWidth, self.hitBoxHeight
                    ))):
                    self.posY += self.speed

    def NextFrame(self):
        self.frameCounter = (self.frameCounter + 1) % len(self.animation)

        # Update l'angle s'il va plus que 360 ou moins que 0 après calculs
        if (self.angle < 0):
            self.angle = 360 + self.angle
        else: 
            self.angle %= 360

        self.image = pygame.transform.rotate(self.animation[self.frameCounter], int(self.angle))

    def Draw(self, screen):
        screen.blit(self.image, (self.posX, self.posY))

        # Debug info - Uncomment to show hitboxes : 
        pygame.draw.rect(screen, (255, 0, 0), Rect(self.posX + self.hitBoxOffestX, self.posY + self.hitBoxOffestY, self.hitBoxWidth, self.hitBoxHeight), 2)
        
        imageRect = self.image.get_rect(topleft=(self.posX, self.posY)) # Test hitbox
        pygame.draw.rect(screen, (0, 0, 255), imageRect, 2) # Test hitbox

        # Looking pretty sweet, noice
        pygame.draw.rect(screen, (0, 255, 0), Rect((imageRect.width / 2) - (self.hitBoxWidth / 2) + self.posX, (imageRect.height / 2) - (self.hitBoxHeight / 2) + self.posY, self.hitBoxWidth, self.hitBoxHeight), 2)