import pygame

TILE_SIZE = 32
TILE_SHEET_WIDTH = 15
TILE_SHEET_HEIGHT = 9
TILESHEET_SIZE = (TILE_SHEET_WIDTH, TILE_SHEET_HEIGHT)
TILESHEET_PIXEL_SIZE = (TILE_SHEET_WIDTH * 16, TILE_SHEET_HEIGHT * 16)
TILESHEET_PATH = "./res/tiled/CosmicLilac_Tiles_greyscale.png"
CSV_PATH = "./res/tiled/testmap.csv"

class Background():
    def __init__(self):
        self.screenSize = pygame.display.get_window_size()
        self.tileSheet = pygame.image.load(TILESHEET_PATH)
        self.tileSheet = pygame.transform.scale(self.tileSheet, (TILESHEET_PIXEL_SIZE[0] * 2, TILESHEET_PIXEL_SIZE[1] * 2))
        self.LoadTileCSV()

        self.screenNbTilesY = int(self.screenSize[1] / TILE_SIZE) + 2
        self.startOffsetY = -self.backgroundSize[1] / 2 + self.screenSize[1]
        self.offsetY = self.startOffsetY

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

    def SetPlayer(self, player):
        self.player = player
        self.playerSize = player.GetSize()

    def IncreaseOffsetY(self, offsetY):
        self.offsetY += offsetY

    def GetOffsetY(self):
        return self.offsetY

    def Draw(self, screen):
        middleY = (self.backgroundSize[1] - (self.offsetY - self.startOffsetY) - self.screenSize[1]) / TILE_SIZE

        for y in range(int(max(0, middleY - (self.screenNbTilesY / 2))), int(min(len(self.tileLayout), middleY + (self.screenNbTilesY / 2)))):
            for x in range(len(self.tileLayout[y])):
                posX = (x * TILE_SIZE) + (self.screenSize[0] / 2) - (self.backgroundSize[0] / 2)
                posY = (y * TILE_SIZE) + (self.screenSize[1] / 2) - (self.backgroundSize[1] / 2) + self.offsetY
                screen.blit(self.tileImages[self.tileLayout[y][x]], (posX, posY))