import pygame
import random
from entities.collectable import Collectable, CollectableType
from entities.monster import Monster, MonsterType
from entities.obstacle import HITBOX_SIZES, Obstacle
from utils.spriteUtils import GetFramesFromFile
from utils.constants import TILE_SIZE, BASE_PATH

TILESHEET_SIZE = (15, 15)
TILESHEET_PIXEL_SIZE = (TILESHEET_SIZE[0] * 16, TILESHEET_SIZE[1] * 16)
TILESHEET_PATH = BASE_PATH + "/res/Tilesheet.png"

OBSTACLES_LAST_ID = 165 # Ids < than this are obstacles or background tiles
ENTITIES_LAST_ID = 195 # Ids < than this and >= OBSTACLES_LAST_ID are entities
COLLECTABLES_LAST_ID = 225 # Ids < than this and >= ENTITIES_LAST_ID are collectables

CSV_PATH_BG = [BASE_PATH + "/levels/level", "/background.csv"]
CSV_PATH_FG = [BASE_PATH + "/levels/level", "/foreground.csv"]

OBSTACLES = []

class GameWorld():
    def __init__(self, currentLevel):
        self.screenSize = pygame.display.get_window_size()
        self.tileSheet = pygame.image.load(TILESHEET_PATH).convert_alpha()
        self.tileSheet = pygame.transform.scale(self.tileSheet, (TILESHEET_PIXEL_SIZE[0] * 2, TILESHEET_PIXEL_SIZE[1] * 2)) # Scale tilesheet 2x

        self.currentLevel = currentLevel if (currentLevel > -1) else 0 
        
        self.monsters = {}
        self.obstacles = []
        self.collectables = {}
        self.LoadTileCSV()
        self.LoadObstacleRessources()
        self.LoadEntityRessources()

        self.screenNbTilesY = int(self.screenSize[1] / TILE_SIZE) + 2
        self.startOffsetY = (-self.backgroundSize[1] + self.screenSize[1]) / 2
        self.offsetY = self.startOffsetY
        self.startMiddleY = (self.backgroundSize[1] - (self.offsetY - self.startOffsetY) - (self.screenSize[1] / 2)) / TILE_SIZE
        self.middleY = -1

        self.enemyTypes = list(MonsterType)
        self.nbEnemyTypes = len(self.enemyTypes)

        self.deadMonsters = []

    def GetTileImage(self, posX, posY):
        rect = pygame.Rect(posX * TILE_SIZE, posY * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        image.blit(self.tileSheet, (0, 0), rect)
        return image

    def LoadTileCSV(self):
        self.tileLayoutBG = []
        self.tileLayoutFG = []
        self.tileImages = {}

        bgCSV = CSV_PATH_BG[0] + str(self.currentLevel + 1) + CSV_PATH_BG[1]
        fgCSV = CSV_PATH_FG[0] + str(self.currentLevel + 1) + CSV_PATH_FG[1]
        allCSV = [bgCSV, fgCSV]

        for i in range(len(allCSV)):
            csvFile = open(allCSV[i], 'r')

            for line in csvFile:
                currentRow = []
                
                for tileNum in line.split(','):
                    intTileNum = int(tileNum)
                    currentRow.append(intTileNum)

                    # If the image will be used (it's part of the background / obstacles) and it's not already loaded, load it in memory
                    if (intTileNum < OBSTACLES_LAST_ID and intTileNum not in self.tileImages):
                        tilePosY = int(intTileNum / TILESHEET_SIZE[0])
                        tilePosX = intTileNum - (tilePosY * TILESHEET_SIZE[0])
                        self.tileImages[intTileNum] = self.GetTileImage(tilePosX, tilePosY) # Load the image from the tileset

                if (i == 0):
                    self.tileLayoutBG.append(currentRow)
                else:
                    self.tileLayoutFG.append(currentRow)
            
        self.backgroundSize = (len(self.tileLayoutBG[0]) * TILE_SIZE, len(self.tileLayoutBG) * TILE_SIZE)

    def LoadObstacleRessources(self):
        soundNames = ["ammoPickup", "gunPickup", "levelComplete"]
        imageNames = ["pistol", "rifle", "sniper", "ammoBig", "goal", "ammo"]

        self.collectableSounds = dict.fromkeys(soundNames)
        self.collectableImages = dict.fromkeys(imageNames)

        for sound in soundNames:
            self.collectableSounds[sound] = pygame.mixer.Sound(BASE_PATH + "/sounds/" + sound + ".mp3")

        for image in imageNames:
            self.collectableImages[image] = pygame.image.load(BASE_PATH + "/res/" + image + ".png").convert_alpha()

    def LoadEntityRessources(self):
        soundNames = ["meatSlap1", "meatSlap2", "meatSlap3", "meatDeath1", "meatDeath2"]
        imageNames = ["monster", "zombie"]
        imageFrameSizes = [[64, 64], [32, 32]]

        self.entitySounds = dict.fromkeys(soundNames)
        self.entityImages = dict.fromkeys(imageNames)

        for sound in soundNames:
            self.entitySounds[sound] = pygame.mixer.Sound(BASE_PATH + "/sounds/" + sound + ".mp3")

        for i in range(len(imageNames)):
            self.entityImages[imageNames[i]] = GetFramesFromFile(imageNames[i] + ".png", imageFrameSizes[i])

    def SetPlayer(self, player):
        self.player = player

    def SpawnTimeOverEnemy(self, id, spawnY):
        spawnX = (self.screenSize[0] / 2) - (self.backgroundSize[0] / 2) + random.randrange(2 * TILE_SIZE, self.backgroundSize[0] - (4 * TILE_SIZE))
        self.monsters[id] = Monster(id, self.enemyTypes[random.randrange(0, self.nbEnemyTypes)], [spawnX, spawnY], self)
        self.monsters[id].health *= 1.5
        self.monsters[id].speed *= 1.25

    def IncreaseOffsetY(self, offsetY):
        self.offsetY += offsetY

        for monsterId in self.monsters:
            self.monsters[monsterId].posY += offsetY

        for collectableId in self.collectables:
            self.collectables[collectableId].posY += offsetY

    def FindGoalPosY(self):
        for y in range(min(20, len(self.tileLayoutFG))):
            for x in range(len(self.tileLayoutFG[y])):
                if (self.tileLayoutFG[y][x] in list(CollectableType) and self.tileLayoutFG[y][x] == CollectableType.GOAL):
                    return y

        print("LEVEL ERROR - The goal is too far from the top of the map")

    def Draw(self, screen):
        self.middleY = (self.backgroundSize[1] - (self.offsetY - self.startOffsetY) - (self.screenSize[1] / 2)) / TILE_SIZE
        self.obstacles = []

        for y in range(int(max(0, self.middleY - (self.screenNbTilesY / 2))), int(min(len(self.tileLayoutBG), self.middleY + (self.screenNbTilesY / 2) + 1))):
            for x in range(len(self.tileLayoutBG[y])):
                posX = (x * TILE_SIZE) + (self.screenSize[0] / 2) - (self.backgroundSize[0] / 2)
                posY = (y * TILE_SIZE) + (self.screenSize[1] / 2) - (self.backgroundSize[1] / 2) + self.offsetY

                if (self.tileLayoutBG[y][x] != -1): # Draw background
                    screen.blit(self.tileImages[self.tileLayoutBG[y][x]], (posX, posY))

                if (self.tileLayoutFG[y][x] != -1): # Draw foreground (obstacles, entities and collectables)
                    if (self.tileLayoutFG[y][x] < OBSTACLES_LAST_ID): # Id is an obstacle
                        screen.blit(self.tileImages[self.tileLayoutFG[y][x]], (posX, posY))

                        if (self.tileLayoutFG[y][x] in HITBOX_SIZES): # The obstacle has a custom hitbox 
                            customHitbox = HITBOX_SIZES.get(self.tileLayoutFG[y][x])

                            self.obstacles.append(Obstacle(True, True, posX, posY, customHitbox))

                            '''# Debug info - Uncomment to show hitboxes : 
                            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(posX + customHitbox[2], posY + customHitbox[3], customHitbox[0], customHitbox[1]), 2)'''
                            
                        else: # Use the default hitbox
                            self.obstacles.append(Obstacle(True, True, posX, posY, [TILE_SIZE, TILE_SIZE, 0, 0]))

                            '''# Debug info - Uncomment to show hitboxes :  
                            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(posX, posY, TILE_SIZE, TILE_SIZE), 2)'''
                    
                    else:
                        tileId = y * self.screenNbTilesY + x
                        
                        if (self.tileLayoutFG[y][x] < ENTITIES_LAST_ID): # Id is an entity
                            if (tileId not in self.monsters and tileId not in self.deadMonsters): # It has not spawned or died
                                self.monsters[tileId] = Monster(tileId, (self.tileLayoutFG[y][x]), [posX, posY], self)

                        elif (tileId not in self.collectables): # Id is a collectable that has not spawned
                            self.collectables[tileId] = Collectable(tileId, (self.tileLayoutFG[y][x]), [posX, posY], self)