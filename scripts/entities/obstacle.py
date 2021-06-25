
HITBOX_SIZES = {
    28 : [16, 16, 7, 7],
    43 : [32, 28, 0, 0],
    44 : [32, 28, 0, 0],
    58 : [32, 28, 0, 0],
    59 : [32, 28, 0, 0],
    73 : [32, 16, 0, 7],
    74 : [16, 32, 7, 0]
}

class Obstacle:
    def __init__(self, blocksBodies, blocksBullets, posX, posY, hitbox):
        self.blocksBodies = blocksBodies
        self.blocksBullets = blocksBullets
        self.posX = posX
        self.posY = posY
        self.width = hitbox[0]
        self.height = hitbox[1]
        self.offsetX = hitbox[2]
        self.offsetY = hitbox[3]