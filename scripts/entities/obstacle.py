import pygame

class Obstacle:
    def __init__(self, BLOCKS_BODIES, BLOCKS_BULLETS, KILLS, x, y):
        self.BLOCKS_BODIES = BLOCKS_BODIES
        self.BLOCKS_BULLETS = BLOCKS_BULLETS
        self.KILLS = KILLS
        self.X = x
        self.Y = y
    
    def BlocksBodies(self):
        return self.BLOCKS_BODIES    

    def BlocksBullets(self):
        return self.BLOCKS_BULLETS    

    def Kills(self):
        return self.Kills
            
    def GetX(self):
        return self.X
                    
    def GetY(self):
        return self.Y