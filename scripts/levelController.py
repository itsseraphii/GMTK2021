import os
import json
from cryptography.fernet import Fernet
from game import Game
from utils.constants import SAVE_KEY, SAVE_PATH

class LevelController:
    def __init__(self, screen):
        game = Game()
        gameState = [0, 0, -2] # [-1: exit  0: restart level  1: next level, currentLevel, menuPage]
        self.save = self.LoadGame()

        while (gameState[0] != -1):
            gameState = game.Init(self, screen, gameState[0] + gameState[1], gameState[0] + gameState[2])

        if (self.SaveRequired(gameState)):
            self.SaveGame(gameState)

    def SaveRequired(self, gameState): # True if nothing is saved or if there has been progress
        return not self.save or gameState[1] > self.save[0] or gameState[2] > self.save[1]

    def LoadGame(self):
        try:
            with open(SAVE_PATH, "r") as file:
                saveData = file.read()

            saveData = Fernet(SAVE_KEY).decrypt(saveData.encode()).decode()
            saveData = json.loads(saveData)

            return [int(saveData["level"]), int(saveData["menu"])]

        except:
            return None

    def SaveGame(self, gameState):
        saveData = {
            "level": max(0, gameState[1]),
            "menu": max(0, gameState[2])
        }

        saveData = json.dumps(saveData)
        saveData = Fernet(SAVE_KEY).encrypt(saveData.encode()).decode()

        os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)

        with open(SAVE_PATH, "w") as file:
            file.write(saveData)