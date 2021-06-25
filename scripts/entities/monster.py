import pygame
from pygame import Rect
import random
import math
from enum import IntEnum
from spriteUtils import BASE_PATH, GetFrames

TURN_ANGLE = 2

class MonsterType(IntEnum):
    ZOMBIE = 165
    FATBOI = 166

HITSOUND_1 = "meatSlap1.mp3"
HITSOUND_2 = "meatSlap2.mp3"
HITSOUND_3 = "meatSlap3.mp3"
DEATHSOUND_1 = "meatDeath1.mp3"
DEATHSOUND_2 = "meatDeath2.mp3"

class Monster:
    def __init__(self, id, monsterType, spawnLocation, gameworld):
        self.gameworld = gameworld
        self.id = id
        self.monster_type = monsterType
        self.posX = spawnLocation[0]
        self.posY = spawnLocation[1]
        self.lastHitTime = 0
        self.angle = 0

        if (monsterType == MonsterType.FATBOI) :
            self.speed = 1
            self.image_source = "monster.png"
            self.animation_speed = 150
            self.accuracy = 2
            self.target_cooldown = 1750 #ms
            self.monster_size = [64, 64]
            deathsound = BASE_PATH + "/sounds/" + DEATHSOUND_2
            self.health = 9

            # Hitbox Info
            self.hitBoxOffestX = 15
            self.hitBoxOffestY = 15
            self.hitBoxWidth = 30
            self.hitBoxLength = 30

        else:
            self.speed = 1.5
            self.image_source = "zombie.png"
            self.animation_speed = 84
            self.accuracy = 3 # Range of target, lower is better
            self.target_cooldown = 1250 #ms
            self.monster_size = [32, 32]
            deathsound = BASE_PATH + "/sounds/" + DEATHSOUND_1
            self.health = 6

            # Hitbox Info
            self.hitBoxWidth = 15
            self.hitBoxLength = 15
            self.hitBoxOffestX = self.hitBoxWidth/2
            self.hitBoxOffestY = self.hitBoxLength/2

        self.hit_1 = pygame.mixer.Sound(BASE_PATH + "/sounds/" + HITSOUND_1)
        self.hit_2 = pygame.mixer.Sound(BASE_PATH + "/sounds/" + HITSOUND_2)
        self.hit_3 = pygame.mixer.Sound(BASE_PATH + "/sounds/" + HITSOUND_3)
        self.death_sound = pygame.mixer.Sound(deathsound)

        self.animation = GetFrames(self.image_source, self.monster_size)
        self.lastFrameTime = 0
        self.lastTargetUpdate = 0
        self.target = gameworld.player.GetPos()
        self.frame_counter = 0
        self.NextFrame()

    def Damage(self, damage):
        self.health -= damage

        if (self.health > 0):
            hitsound = random.randint(1, 3)
            
            if hitsound == 1 :
                self.hit_1.play()
            elif hitsound == 2:
                self.hit_2.play()
            else :
                self.hit_3.play()
        else:
            self.gameworld.deadMonsters.append(self.id) # Prevents respawn
            self.gameworld.monsters.pop(self.id)
            self.death_sound.play()

    def Stun(self, timeMS):
        self.lastHitTime = pygame.time.get_ticks() + timeMS

    def Move(self):
        currentTime = pygame.time.get_ticks()

        if currentTime > self.lastTargetUpdate + self.target_cooldown :
            self.lastTargetUpdate = currentTime
            playerLocation = self.gameworld.player.GetPos()

            # Faraway
            if abs(playerLocation[0]) - abs(self.posX) > 100 or abs(playerLocation[1]) - abs(self.posY) > 100 :
                # Draws a zone around the player, choosing a random angle to select a target
                targetAngle = math.degrees(random.uniform(0, 6.29))
                self.target[0] = playerLocation[0] + (self.accuracy * self.gameworld.tile_size) * math.sin(targetAngle)
                self.target[1] = playerLocation[1] + (self.accuracy * self.gameworld.tile_size) * math.cos(targetAngle)
            else: # straight to the player
                self.target = playerLocation

        if (self.lastHitTime < pygame.time.get_ticks()):
            if (currentTime >= self.lastFrameTime + self.animation_speed ):
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
                    self.hitBoxWidth, self.hitBoxLength
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
                    self.hitBoxWidth, self.hitBoxLength
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
                    self.hitBoxWidth, self.hitBoxLength
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
                    self.hitBoxWidth, self.hitBoxLength
                    ))):
                    self.posY += self.speed

    def NextFrame(self):
        self.frame_counter += 1

        if (self.frame_counter >= len(self.animation)) :
            self.frame_counter = 0

        # update l'angle s'il va plus que 360 ou moins que 0 après calculs
        if (self.angle < 0):
            self.angle = 360 + self.angle
        else: 
            self.angle %= 360

        self.image = pygame.transform.rotate(self.animation[self.frame_counter], int(self.angle))

    def Draw(self, screen):
        screen.blit(self.image, (self.posX, self.posY))

        '''# Debug info - Uncomment to show hitboxes : 
        pygame.draw.rect(screen, (255,0,0), Rect(self.posX + self.hitBoxOffestX, self.posY + self.hitBoxOffestY, self.hitBoxWidth, self.hitBoxLength), 2)'''