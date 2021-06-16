import pygame
from entities.collectable import Collectable, CollectableType
from entities.obstacle import Obstacle
import sys
from entities.monster import Monster, MonsterType
import random

try: # Path for files when app is built by PyInstaller
    BASE_PATH = sys._MEIPASS
except:
    BASE_PATH = "."

TILE_SIZE = 32
TILESHEET_SIZE = (15, 15)
TILESHEET_PIXEL_SIZE = (TILESHEET_SIZE[0] * 16, TILESHEET_SIZE[1] * 16)
TILESHEET_PATH = BASE_PATH + "/res/Tilesheet.png"

OBSTACLES_LAST_ID = 165
ENTITIES_LAST_ID = 195

CSV_PATH_BG = [BASE_PATH + "/levels/level", "/background.csv"]
CSV_PATH_FG = [BASE_PATH + "/levels/level", "/foreground.csv"]

DICT_HITBOX_SIZES = {
    28 : [16, 16, 7, 7],
    43 : [32, 28, 0, 0],
    44 : [32, 28, 0, 0],
    58 : [32, 28, 0, 0],
    59 : [32, 28, 0, 0],
    73 : [32, 16, 0, 7],
    74 : [16, 32, 7, 0]
}

OBSTACLES = []

class GameWorld():
    def __init__(self, currentLevel):
        self.tile_size = TILE_SIZE
        self.screenSize = pygame.display.get_window_size()
        self.tileSheet = pygame.image.load(TILESHEET_PATH).convert_alpha()
        self.tileSheet = pygame.transform.scale(self.tileSheet, (TILESHEET_PIXEL_SIZE[0] * 2, TILESHEET_PIXEL_SIZE[1] * 2))

        self.currentLevel = currentLevel if (currentLevel > -1) else 0 

        self.monsters = {}
        self.collectables = {}
        self.LoadTileCSV()

        self.screenNbTilesY = int(self.screenSize[1] / TILE_SIZE) + 2
        self.startOffsetY = (-self.backgroundSize[1] + self.screenSize[1]) / 2
        self.offsetY = self.startOffsetY
        self.middleY = -1

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
                        self.tileImages.update({intTileNum: self.GetTileImage(tilePosX, tilePosY)}) # Load the image from the tileset

                if (i == 0):
                    self.tileLayoutBG.append(currentRow)
                else:
                    self.tileLayoutFG.append(currentRow)
            
        self.backgroundSize = (len(self.tileLayoutBG[0]) * TILE_SIZE, len(self.tileLayoutBG) * TILE_SIZE)

    def SetPlayer(self, player):
        self.player = player
        self.playerSize = player.GetSize()

    def SpawnTimeOverEnemies(self):
        nbEnemies = min((self.currentLevel + 1) * 15, 50)
        selectedEnemyType = 0
        possibleEnemyTypes = list(MonsterType)
        playerPos = self.player.GetPos()

        for i in range(nbEnemies):
            spawnSide = random.randrange(0, 3)

            if (i not in self.monsters):
                if (spawnSide == 0):
                    self.monsters[i] = Monster(i, possibleEnemyTypes[selectedEnemyType], [playerPos[0] + (self.screenSize[0] / 3 * 2), playerPos[1] + (i * TILE_SIZE * 3)], self)
                elif (spawnSide == 1):
                    self.monsters[i] = Monster(i, possibleEnemyTypes[selectedEnemyType], [playerPos[0] - (self.screenSize[0] / 3 * 2), playerPos[1] + (i * TILE_SIZE * 3)], self)
                else:
                    self.monsters[i] = Monster(i, possibleEnemyTypes[selectedEnemyType], [playerPos[0] + random.randint(-self.screenSize[0] / 2, self.screenSize[0] / 2), playerPos[1] - (self.screenSize[0] / 3 * 2) - (i * TILE_SIZE)], self)

            self.monsters[i].health *= 1.25
            self.monsters[i].speed *= 1.15
            selectedEnemyType = (selectedEnemyType + 1) % len(possibleEnemyTypes)

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

        for y in range(int(max(0, self.middleY - (self.screenNbTilesY / 2))), int(min(len(self.tileLayoutBG), self.middleY + (self.screenNbTilesY / 2)))):
            for x in range(len(self.tileLayoutBG[y])):
                posX = (x * TILE_SIZE) + (self.screenSize[0] / 2) - (self.backgroundSize[0] / 2)
                posY = (y * TILE_SIZE) + (self.screenSize[1] / 2) - (self.backgroundSize[1] / 2) + self.offsetY
                screen.blit(self.tileImages[self.tileLayoutBG[y][x]], (posX, posY))

                if (self.tileLayoutFG[y][x] != -1):
                    if (self.tileLayoutFG[y][x] < OBSTACLES_LAST_ID): # Id is an obstacle
                        screen.blit(self.tileImages[self.tileLayoutFG[y][x]], (posX, posY))

                        if (self.tileLayoutFG[y][x] in DICT_HITBOX_SIZES): # The obstacle has a custom hitbox 
                            customHitbox = DICT_HITBOX_SIZES.get(self.tileLayoutFG[y][x])

                            self.obstacles.append(Obstacle(True, False, False, posX, posY, 
                                customHitbox[0], customHitbox[1], customHitbox[2], customHitbox[3]))

                            '''# Debug info - Uncomment to show hitboxes : 
                            pygame.draw.rect(screen, (255,0,0), pygame.Rect(
                                posX + customHitbox[2], posY + customHitbox[3],
                                customHitbox[0], customHitbox[1]), 2)'''
                            
                        else: # Use the default hitbox 
                            self.obstacles.append(Obstacle(True, False, False, posX, posY, 32, 32, 0, 0))

                            '''# Debug info - Uncomment to show hitboxes :  
                            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(posX, posY, 32, 32), 2)'''
                    
                    else:
                        tileId = y * self.screenNbTilesY + x
                        
                        if (self.tileLayoutFG[y][x] < ENTITIES_LAST_ID): # Id is an entity
                            if (tileId not in self.monsters and tileId not in self.deadMonsters): # It has not spawned or died
                                self.monsters[tileId] = Monster(tileId, (self.tileLayoutFG[y][x]), [posX, posY], self)

                        elif (tileId not in self.collectables): # Id is a collectable that has not spawned
                            self.collectables[tileId] = Collectable(tileId, (self.tileLayoutFG[y][x]), [posX, posY], self)