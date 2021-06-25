import pygame
import sys
from enum import IntEnum

try: # Path for files when app is built by PyInstaller
    BASE_PATH = sys._MEIPASS
except:
    BASE_PATH = "."

# Sound files
AMMO_PICKUP_SOUND = BASE_PATH + "/sounds/" + "ammoPickup.mp3"
GUN_PICKUP_SOUND = BASE_PATH + "/sounds/" + "gunPickup.mp3"
LEVEL_COMPLETE_SOUND = BASE_PATH + "/sounds/" + "levelComplete.mp3"

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
            self.imageFile = "pistol.png"
            self.soundFile = GUN_PICKUP_SOUND
            self.size = [32, 15]
        elif (self.type == CollectableType.RIFLE):
            self.imageFile = "rifle.png"
            self.soundFile = GUN_PICKUP_SOUND
            self.size = [32, 15]
        elif (self.type == CollectableType.SNIPER):
            self.imageFile = "sniper.png"
            self.soundFile = GUN_PICKUP_SOUND
            self.size = [32, 15]
        elif (self.type == CollectableType.BIG_AMMO):
            self.imageFile = "ammoBig.png"
            self.soundFile = AMMO_PICKUP_SOUND
            self.size = [32, 32]
        elif (self.type == CollectableType.GOAL):
            self.imageFile = "goal.png"
            self.soundFile = LEVEL_COMPLETE_SOUND
            self.size = [32, 32]
        else:
            self.imageFile = "ammo.png"
            self.soundFile = AMMO_PICKUP_SOUND
            self.size = [32, 32]

        self.pickupSound = pygame.mixer.Sound(self.soundFile)
        self.image = pygame.image.load(BASE_PATH + "/res/" + self.imageFile)

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