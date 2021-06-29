import pygame
from utils.constants import DATA_PATH

# Returns an array of all frames from a file
def GetFramesFromFile(filename, frameSize):
    try:
        spriteSheet = pygame.image.load(DATA_PATH + "/res/" + filename).convert()
    except:
        print("Error while fetching " + filename)

    return GetFramesFromImage(spriteSheet, frameSize)

# Returns an array of all frames from an image
def GetFramesFromImage(spriteSheet, frameSize):
    frameCount = spriteSheet.get_rect().size[0] / frameSize[0]

    i = 0
    frameArray = []

    while i < frameCount:
        frame = GetSingleFrame(spriteSheet, frameSize, i)
        frameArray.append(frame)
        i += 1

    return frameArray

def GetSingleFrame(spriteSheet, frameSize, frameNumber):
    # Create a new blank image
    frame = pygame.Surface(frameSize).convert()

    # Copy the sprite from the large sheet onto the smaller image
    frame.blit(spriteSheet, (0, 0), (frameNumber * frameSize[0], 0, frameSize[0], frameSize[1]))

    # Assuming black is the transparent color
    frame.set_colorkey((0, 0, 0))

    # Return the image
    return frame