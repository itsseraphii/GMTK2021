from enum import Enum
from spriteUtils import getFrames
import random
import math
import pygame
import sys

try: # Path for files when app is built by PyInstaller
    BASE_PATH = sys._MEIPASS
except:
    BASE_PATH = "."

AMMO_PICKUP_SOUND = "ammo_pickup.ogg"
GUN_PICKUP_SOUND = "gun_pickup.wav"
DASH_SOUND = "dash.wav"

class CollectableType(Enum):
    AMMO = 125
    PISTOL = 129
    RIFLE = 121
    SNIPER = 119
    BIG_AMMO = 127
    GOAL = 132

class Collectable:
    def __init__(self, id, collectable_type, spawn_location, gameworld):
        self.gameworld = gameworld
        self.id = id
        self.posX = spawn_location[0]
        self.posY = spawn_location[1]
        self.collected = False

        if (CollectableType(collectable_type) == CollectableType.PISTOL):
            self.image_source = "pistol.png"
            self.size = [32, 15]
            self.type = CollectableType.PISTOL
            self.soundSource = GUN_PICKUP_SOUND
        elif (CollectableType(collectable_type) == CollectableType.RIFLE):
            self.image_source = "rifle.png"
            self.size = [32, 15]
            self.type = CollectableType.RIFLE
            self.soundSource = GUN_PICKUP_SOUND
        elif (CollectableType(collectable_type) == CollectableType.SNIPER):
            self.image_source = "sniper.png"
            self.size = [32, 15]
            self.type = CollectableType.SNIPER
            self.soundSource = GUN_PICKUP_SOUND
        elif (CollectableType(collectable_type) == CollectableType.BIG_AMMO):
            self.image_source = "ammo_big.png"
            self.size = [32, 32]
            self.type = CollectableType.BIG_AMMO
            self.soundSource = AMMO_PICKUP_SOUND
        elif (CollectableType(collectable_type) == CollectableType.GOAL):
            self.image_source = "goal.png"
            self.size = [32, 32]
            self.type = CollectableType.GOAL
            self.soundSource = DASH_SOUND
        else:
            self.image_source = "ammo.png"
            self.size = [32, 32]
            self.type = CollectableType.AMMO
            self.soundSource = AMMO_PICKUP_SOUND

        self.pickupSound = pygame.mixer.Sound(BASE_PATH + "/sounds/" + self.soundSource)

        self.image = pygame.image.load(BASE_PATH + "/res/" + self.image_source)

    def Pickup(self):
        self.collected = True
        self.pickupSound.play()

        if self.type == CollectableType.PISTOL:
            weapon = "Revolver"
            if weapon not in self.gameworld.player.weaponInventory:
                self.gameworld.player.ammo += 5
                self.gameworld.player.weaponInventory.append(weapon)
                self.gameworld.player.equippedWeaponIndex += 1
            else:
                self.gameworld.player.ammo += 8

        elif self.type == CollectableType.RIFLE:
            weapon = "Assault Rifle"
            if weapon not in self.gameworld.player.weaponInventory:
                self.gameworld.player.ammo += 10
                self.gameworld.player.weaponInventory.append(weapon)
                self.gameworld.player.equippedWeaponIndex += 1
            else:
                self.gameworld.player.ammo += 15

        elif self.type == CollectableType.SNIPER:
            weapon = "Sniper"
            if weapon not in self.gameworld.player.weaponInventory:
                self.gameworld.player.ammo += 2
                self.gameworld.player.weaponInventory.append(weapon)
                self.gameworld.player.equippedWeaponIndex += 1
            else:
                self.gameworld.player.ammo += 5

        elif self.type == CollectableType.BIG_AMMO:
            self.gameworld.player.ammo += 10

        elif self.type == CollectableType.GOAL:
            self.gameworld.player.game.TriggerGameOver(True)

        else :
            # Ammo pickup
            self.gameworld.player.ammo += 4

    def Draw(self, screen):
        if not self.collected :
            screen.blit(self.image, (self.posX, self.posY))


