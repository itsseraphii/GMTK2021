import pygame

TILE_SIZE = 32
TILESHEET_SIZE = (13, 8)
TILESHEET_PATH = "./res/tiled/CosmicLilac_Tiles_greyscale.png"
CSV_PATH = "./res/tiled/testmap..csv"

class Background():
    def __init__(self):
        self.tileSheet = pygame.transform.scale(pygame.image.load(TILESHEET_PATH), (416, 256))
        self.LoadTileCSV()

    def GetTile(self, posX, posY):
        rect = pygame.Rect(posX * TILE_SIZE, posY * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.tileSheet, (0, 0), rect)
        return image

    def LoadTileCSV(self):
        self.tileLayout = []
        self.tileImages = {}
        csvFile = open(CSV_PATH, 'r')

        for line in csvFile:
            currentRow = []
            
            for tileNum in line.split(','):
                intTileNum = int(tileNum)
                currentRow.append(intTileNum)

                if (intTileNum not in self.tileImages):
                    tilePosY = int(intTileNum / TILESHEET_SIZE[0])
                    tilePosX = intTileNum - (tilePosY * TILESHEET_SIZE[0])
                    self.tileImages.update({intTileNum: self.GetTile(tilePosX, tilePosY)})

            self.tileLayout.append(currentRow)

    def Draw(self, screen):
        for y in range(len(self.tileLayout)):
            for x in range(len(self.tileLayout[y])):
                screen.blit(self.tileImages[self.tileLayout[y][x]], (x * TILE_SIZE, y * TILE_SIZE))