import pygame
import sys
from enum import IntEnum

try: # Path for files when app is built by PyInstaller
    BASE_PATH = sys._MEIPASS
except:
    BASE_PATH = "."

# Sound files
AMMO_PICKUP_SOUND = BASE_PATH + "/sounds/" + "ammo_pickup.ogg"
GUN_PICKUP_SOUND = BASE_PATH + "/sounds/" + "gun_pickup.wav"
DASH_SOUND = BASE_PATH + "/sounds/" + "dash.wav"

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

        try:
            CollectableType(collectable_type)
        except:
            collectable_type = CollectableType.AMMO

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
            self.imageFile = "ammo_big.png"
            self.soundFile = AMMO_PICKUP_SOUND
            self.size = [32, 32]
        elif (self.type == CollectableType.GOAL):
            self.imageFile = "goal.png"
            self.soundFile = DASH_SOUND
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
            self.AddPlayerWeapon(5, 8, "Revolver")

        elif (self.type == CollectableType.RIFLE):
            self.AddPlayerWeapon(10, 15, "Assault Rifle")

        elif (self.type == CollectableType.SNIPER):
            self.AddPlayerWeapon(2, 5, "Sniper")

        elif (self.type == CollectableType.BIG_AMMO):
            self.gameworld.player.ammo += 10

        elif (self.type == CollectableType.GOAL):
            self.gameworld.player.game.TriggerGameOver(True)

        else: # Ammo pickup
            self.gameworld.player.ammo += 4

    def AddPlayerWeapon(self, ammo, duplicateAmmo, weaponName):
        if (weaponName not in self.gameworld.player.weaponInventory):
            self.gameworld.player.ammo += ammo
            self.gameworld.player.weaponInventory.append(weaponName)
            self.gameworld.player.equippedWeaponIndex = len(self.gameworld.player.weaponInventory) - 1
        else:
            self.gameworld.player.ammo += duplicateAmmo

    def Draw(self, screen):
        if not self.collected :
            screen.blit(self.image, (self.posX, self.posY))