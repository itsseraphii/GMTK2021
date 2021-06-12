import pygame

TILE_SIZE = 16
TILESHEET_PATH = "./res/tiled/CosmicLilac_Tiles.png"

FLOOR_TILE_POS = [1, 1]
LEFT_WALL_TILE_POS = [0, 1]
RIGHT_WALL_TILE_POS = [3, 1]

class Background():
    def __init__(self):
        self.tileSheet = pygame.image.load(TILESHEET_PATH)

    def GetTile(self, posX, posY):
        rect = pygame.Rect(posX * TILE_SIZE, posY * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.tileSheet, (0, 0), rect)
        return image

    def DrawTile(screen, image, posX, posY):
        screen.blit(image, (posX, posY))

    def Draw(self, screen):
        for x in range(32):
            for y in range(32):
                if (x == 0):
                    tile = self.GetTile(LEFT_WALL_TILE_POS[0], LEFT_WALL_TILE_POS[1])
                elif (x == 31):
                    tile = self.GetTile(RIGHT_WALL_TILE_POS[0], RIGHT_WALL_TILE_POS[1])
                else:
                    tile = self.GetTile(FLOOR_TILE_POS[0], FLOOR_TILE_POS[1])

                screen.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))