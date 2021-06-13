from enum import Enum
from spriteUtils import getFrames
import pygame

class MonsterType(Enum):
    FATBOI = 105
    ZOMBIE = 110

class Monster:
    def __init__(self, id, monster_type, spawn_location, gameworld):
        self.gameworld = gameworld
        self.id = id
        self.posX = spawn_location[0]
        self.posY = spawn_location[1]
        self.lastHitTime = 0

        if (MonsterType(monster_type) == MonsterType.FATBOI) :
            self.speed = 1
            self.image_source = "monster1.png"
            self.animation_speed = 150
            self.monster_size = [64, 64]
            self.health = 9
        else:
            self.speed = 1.5
            self.image_source = "zombie1.png"
            self.animation_speed = 84
            self.monster_size = [32, 32]
            self.health = 6

        self.animation = getFrames(self.image_source, self.monster_size)
        self.lastFrameTime = 0
        self.frame_counter = 0

    def Draw(self, screen):
        currentTime = pygame.time.get_ticks()

        if (currentTime >= self.lastFrameTime + self.animation_speed ):
            self.lastFrameTime = currentTime
            self.NextFrame()
        
        screen.blit(self.image, (self.posX, self.posY))

    def Damage(self, damage):
        self.health -= damage

        if (self.health <= 0):
            # TODO death anim (currently just deleting)
            self.gameworld.monsters.pop(self.id)

    def Stun(self, timeMS):
        self.lastHitTime = pygame.time.get_ticks() + timeMS

    def MoveTowardsPlayer(self):
        if (self.lastHitTime < pygame.time.get_ticks()):
            playerLocation = self.gameworld.player.GetPos()

            if playerLocation[0] > self.posX :
                self.posX += self.speed
            elif playerLocation[0] < self.posX :
                self.posX -= self.speed
            
            if playerLocation[1] > self.posY :
                self.posY += self.speed
            elif playerLocation[1] < self.posY :
                self.posY -= self.speed

    def NextFrame(self):
        self.frame_counter += 1

        if (self.frame_counter >= len(self.animation)) :
            self.frame_counter = 0

        self.image = self.animation[self.frame_counter]


