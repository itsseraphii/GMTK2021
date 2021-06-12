import pygame

# Returns an array of all frames of 
def loadFrames(filename, tile_size):
    spriteSheet = pygame.image.load("./res/" + filename)
    print(spriteSheet.get_rect().size)
