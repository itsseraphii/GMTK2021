from enum import IntEnum

class CollectableType(IntEnum):
    PISTOL = 195
    RIFLE = 196
    SNIPER = 197
    AMMO = 198
    BIG_AMMO = 199
    GOAL = 200

class Collectable:
    def __init__(self, id, collectable_type, spawn_location, gameworld):
        self.gameworld = gameworld
        self.id = id
        self.posX = spawn_location[0]
        self.posY = spawn_location[1]
        self.collected = False

        if (collectable_type not in list(CollectableType)):
            self.type = CollectableType.AMMO
        else:
            self.type = collectable_type

        if (self.type == CollectableType.PISTOL):
            imageName = "pistol"
            soundName = "gunPickup"
            self.size = [32, 15]
        elif (self.type == CollectableType.RIFLE):
            imageName = "rifle"
            soundName = "gunPickup"
            self.size = [32, 15]
        elif (self.type == CollectableType.SNIPER):
            imageName = "sniper"
            soundName = "gunPickup"
            self.size = [32, 15]
        elif (self.type == CollectableType.BIG_AMMO):
            imageName = "ammoBig"
            soundName = "ammoPickup"
            self.size = [32, 32]
        elif (self.type == CollectableType.GOAL):
            imageName = "goal"
            soundName = "levelComplete"
            self.size = [32, 32]
        else:
            imageName = "ammo"
            soundName = "ammoPickup"
            self.size = [32, 32]

        self.pickupSound = self.gameworld.collectableSounds[soundName]
        self.image = self.gameworld.collectableImages[imageName]

    def Pickup(self):
        self.collected = True
        self.pickupSound.play()

        if (self.type == CollectableType.PISTOL):
            self.gameworld.player.AddWeapon(5, 8, "Revolver")

        elif (self.type == CollectableType.RIFLE):
            self.gameworld.player.AddWeapon(10, 15, "Assault Rifle")

        elif (self.type == CollectableType.SNIPER):
            self.gameworld.player.AddWeapon(2, 5, "Sniper")

        elif (self.type == CollectableType.BIG_AMMO):
            self.gameworld.player.ammo += 10

        elif (self.type == CollectableType.GOAL):
            self.gameworld.player.game.TriggerGameOver(True)

        else: # Small ammo pickup
            self.gameworld.player.ammo += 4

    def Draw(self, screen):
        if not self.collected :
            screen.blit(self.image, (self.posX, self.posY))