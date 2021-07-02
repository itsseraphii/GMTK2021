from weaponController import WeaponTypes
from enum import IntEnum

DEFAULT_SIZE = [32, 32]

class CollectableTypes(IntEnum):
    PISTOL = 195
    RIFLE = 196
    SNIPER = 197
    AMMO = 198
    BIG_AMMO = 199
    GOAL = 200

class Collectable:
    def __init__(self, id, collectableType, spawnLocation, gameworld):
        self.gameworld = gameworld
        self.id = id
        self.posX = spawnLocation[0]
        self.posY = spawnLocation[1]
        self.collected = False

        if (collectableType in list(CollectableTypes)):
            self.type = collectableType
        else:
            self.type = CollectableTypes.AMMO

        if (self.type == CollectableTypes.PISTOL):
            imageName = "revolver"
            soundName = "gunPickup"
            self.size = [32, 15]

        elif (self.type == CollectableTypes.RIFLE):
            imageName = "rifle"
            soundName = "gunPickup"
            self.size = [32, 15]

        elif (self.type == CollectableTypes.SNIPER):
            imageName = "sniper"
            soundName = "gunPickup"
            self.size = [32, 15]

        elif (self.type == CollectableTypes.BIG_AMMO):
            imageName = "ammoBig"
            soundName = "ammoPickup"
            self.size = DEFAULT_SIZE

        elif (self.type == CollectableTypes.GOAL):
            imageName = "goal"
            soundName = "levelComplete"
            self.size = DEFAULT_SIZE

        else:
            imageName = "ammo"
            soundName = "ammoPickup"
            self.size = DEFAULT_SIZE

        self.pickupSound = self.gameworld.collectableSounds[soundName]
        self.image = self.gameworld.collectableImages[imageName]

    def Pickup(self):
        self.collected = True
        self.pickupSound.play()

        if (self.type == CollectableTypes.PISTOL):
            self.gameworld.player.AddWeapon(5, 8, WeaponTypes.REVOLVER)

        elif (self.type == CollectableTypes.RIFLE):
            self.gameworld.player.AddWeapon(10, 15, WeaponTypes.RIFLE)

        elif (self.type == CollectableTypes.SNIPER):
            self.gameworld.player.AddWeapon(2, 5, WeaponTypes.SNIPER)

        elif (self.type == CollectableTypes.BIG_AMMO):
            self.gameworld.player.ammo += 10

        elif (self.type == CollectableTypes.GOAL):
            self.gameworld.player.game.TriggerGameOver(True)

        else: # Small ammo pickup
            self.gameworld.player.ammo += 4

    def Draw(self, screen):
        if not self.collected :
            screen.blit(self.image, (self.posX, self.posY))

            '''# Debug info - Uncomment to show hitboxes : 
            import pygame
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.posX, self.posY, self.size[0], self.size[1]), 2)'''