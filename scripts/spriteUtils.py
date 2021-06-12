import pygame

# Returns an array of all frames from requested file
def getFrames(filename, tile_size):
    try:
        spriteSheet = pygame.image.load("./res/" + filename).convert()
    except pygame.error as e:
        print("error while fetching " + filename)

    nbOfFrames = spriteSheet.get_rect().size[0]/tile_size

    i = 0
    frameArray = []
    while i < nbOfFrames:
        spriteXOffset = i * tile_size

        rect = pygame.Rect(spriteXOffset * tile_size, 0, tile_size, tile_size)
        frame = pygame.Surface(rect.size).convert()
        frame.blit(spriteSheet, (0,0), rect)
        frameArray.append(frame)
        i += 1

    return frameArray

