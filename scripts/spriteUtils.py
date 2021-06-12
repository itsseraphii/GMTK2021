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
        frame = getSingleFrame(spriteSheet, tile_size, i)
        frameArray.append(frame)
        i += 1

    return frameArray

def getSingleFrame(sprite_sheet, tile_size, frame_number):
    # Create a new blank image
    frame = pygame.Surface([tile_size, tile_size]).convert()

    # Copy the sprite from the large sheet onto the smaller image
    frame.blit(sprite_sheet, (0, 0), (frame_number*tile_size, 0, tile_size, tile_size))

    # Assuming black works as the transparent color
    frame.set_colorkey((0, 0, 0))

    # Return the image
    return frame

