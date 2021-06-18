class Obstacle:
    def __init__(self, BLOCKS_BODIES, BLOCKS_BULLETS, KILLS, posX, posY, width, length, offsetX, offsetY):
        self.BLOCKS_BODIES = BLOCKS_BODIES
        self.BLOCKS_BULLETS = BLOCKS_BULLETS
        self.KILLS = KILLS
        self.posX = posX
        self.posY = posY
        self.width = width
        self.length = length
        self.offsetX = offsetX
        self.offsetY = offsetY

    # TODO All those returns could be remove (just call obstacle.varName)
    
    def BlocksBodies(self):
        return self.BLOCKS_BODIES    

    def BlocksBullets(self):
        return self.BLOCKS_BULLETS    

    def Kills(self):
        return self.KILLS
    
    def GetX(self):
        return self.posX

    def GetY(self):
        return self.posY
    
    def GetHitboxWidth(self):
        return self.width

    def GetHitboxLength(self):
        return self.length
    
    def GetHitBoxOffsetX(self):
        return self.offsetX

    def GetHitBoxOffsetY(self):
        return self.offsetY