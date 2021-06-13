from enum import Enum
from spriteUtils import BASE_PATH, getFrames
import random
import math
import pygame

class MonsterType(Enum):
    FATBOI = 105
    ZOMBIE = 110

HITSOUND_1 = "meat_slap1.wav"
HITSOUND_2 = "meat_slap2.wav"
HITSOUND_3 = "meat_slap3.wav"
DEATHSOUND_1 = "meatDeath.wav"
DEATHSOUND_2 = "meatDeath2.wav"

class Monster:
    def __init__(self, id, monster_type, spawn_location, gameworld):
        self.gameworld = gameworld
        self.id = id
        self.posX = spawn_location[0]
        self.posY = spawn_location[1]
        self.lastHitTime = 0

        if (MonsterType(monster_type) == MonsterType.FATBOI) :
            self.monster_type = MonsterType.FATBOI
            self.speed = 1
            self.image_source = "monster_n1.png"
            self.animation_speed = 150
            self.accuracy = 2
            self.target_cooldown = 1750 #ms
            self.monster_size = [64, 64]
            deathsound = BASE_PATH + "/sounds/" + DEATHSOUND_2
            self.health = 9
        else:
            self.monster_type = MonsterType.ZOMBIE
            self.speed = 1.5
            self.image_source = "zombie1.png"
            self.animation_speed = 84
            self.accuracy = 3 # Range of target, lower is better
            self.target_cooldown = 1250 #ms
            self.monster_size = [32, 32]
            deathsound = BASE_PATH + "/sounds/" + DEATHSOUND_1
            self.health = 6

        self.hit_1 = pygame.mixer.Sound(BASE_PATH + "/sounds/" + HITSOUND_1)
        self.hit_2 = pygame.mixer.Sound(BASE_PATH + "/sounds/" + HITSOUND_2)
        self.hit_3 = pygame.mixer.Sound(BASE_PATH + "/sounds/" + HITSOUND_3)
        self.death_sound = pygame.mixer.Sound(deathsound)

        self.animation = getFrames(self.image_source, self.monster_size)
        self.lastFrameTime = 0
        self.lastTargetUpdate = 0
        self.target = gameworld.player.GetPos()
        self.frame_counter = 0
        self.NextFrame()

    def Draw(self, screen):
        screen.blit(self.image, (self.posX, self.posY))

    def Damage(self, damage):
        self.health -= damage

        if (self.health <= 0):
            self.gameworld.deadMonsters.append(self.id) # Prevents respawn
            self.gameworld.monsters.pop(self.id)
            self.death_sound.play()
        else:
            hitsound = random.randint(1, 3)
            if hitsound == 1 :
                self.hit_1.play()
            elif hitsound == 2:
                self.hit_2.play()
            else :
                self.hit_3.play()

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
            elif self.target[0] < self.posX :
                self.posX -= self.speed
            
            if self.target[1] > self.posY :
                self.posY += self.speed
            elif self.target[1] < self.posY :
                self.posY -= self.speed

    def NextFrame(self):
        self.frame_counter += 1

        if (self.frame_counter >= len(self.animation)) :
            self.frame_counter = 0

        self.image = self.animation[self.frame_counter]