class Obstacle:
    def __init__(self, BLOCKS_BODIES, BLOCKS_BULLETS, KILLS, x, y, width, length, offX, offY):
        self.BLOCKS_BODIES = BLOCKS_BODIES
        self.BLOCKS_BULLETS = BLOCKS_BULLETS
        self.KILLS = KILLS
        self.X = x
        self.Y = y
        self.width = width
        self.length = length
        self.offX = offX
        self.offY = offY

    # TODO All those returns could be remove (just call obstacle.varName)
    
    def BlocksBodies(self):
        return self.BLOCKS_BODIES    

    def BlocksBullets(self):
        return self.BLOCKS_BULLETS    

    def Kills(self):
        return self.KILLS
            
    def GetX(self):
        return self.X

    def GetY(self):
        return self.Y
    
    def GetHitboxWidth(self):
        return self.width

    def GetHitboxLength(self):
        return self.length
    
    def GetHitBoxOffsetX(self):
        return self.offX

    def GetHitBoxOffsetY(self):
        return self.offY