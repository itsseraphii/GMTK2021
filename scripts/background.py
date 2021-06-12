import pygame

TILE_SIZE = 32
TILESHEET_SIZE = (13, 8)
TILESHEET_PIXEL_SIZE = (208, 128)
TILESHEET_PATH = "./res/tiled/CosmicLilac_Tiles.png"
CSV_PATH = "./res/tiled/testmap..csv"

class Background():
    def __init__(self):
        self.offset = 0
        self.screenSize = pygame.display.get_window_size()
        self.tileSheet = pygame.image.load(TILESHEET_PATH)
        self.tileSheet = pygame.transform.scale(self.tileSheet, (TILESHEET_PIXEL_SIZE[0] * 2, TILESHEET_PIXEL_SIZE[1] * 2))
        self.LoadTileCSV()

    def GetTileImage(self, posX, posY):
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

                # Load tile image in memory if it's not already loaded
                if (intTileNum not in self.tileImages):
                    tilePosY = int(intTileNum / TILESHEET_SIZE[0])
                    tilePosX = intTileNum - (tilePosY * TILESHEET_SIZE[0])
                    self.tileImages.update({intTileNum: self.GetTileImage(tilePosX, tilePosY)})

            self.tileLayout.append(currentRow)

        self.backgroundSize = (len(self.tileLayout[0]) * TILE_SIZE, len(self.tileLayout) * TILE_SIZE)

    def SetPlayerSize(self, size):
        self.playerSize = size

    def IncreaseOffsetY(self, offset):
        self.offset += offset

    def GetOffsetY(self):
        return self.offset

    def InWidthBounds(self, posX):
        return posX > (self.screenSize[0] / 2) - (self.backgroundSize[0] / 2) and posX < (self.screenSize[0] / 2) + (self.backgroundSize[0] / 2) - self.playerSize[0]

    def Draw(self, screen):
        for y in range(len(self.tileLayout)):
            for x in range(len(self.tileLayout[y])):
                posX = (x * TILE_SIZE) + (self.screenSize[0] / 2) - (self.backgroundSize[0] / 2)
                posY = (y * TILE_SIZE) + (self.screenSize[1] / 2) - (self.backgroundSize[1] / 2) + self.offset
                screen.blit(self.tileImages[self.tileLayout[y][x]], (posX, posY))