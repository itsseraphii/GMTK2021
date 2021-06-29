import os
from game import Game
from utils.constants import SAVE_PATH

class LevelController:
    def __init__(self, screen):
        game = Game()
        gameState = [0, 0, -2] # [-1: exit  0: restart level  1: next level, currentLevel, menuPage]
        self.save = self.LoadGame()

        while (gameState[0] != -1):
            gameState = game.Init(self, screen, gameState[0] + gameState[1], gameState[0] + gameState[2])

        self.SaveGame(gameState)

    def LoadGame(self):
        pass

    def SaveGame(self, gameState):
        filename = SAVE_PATH + "/save.dat"
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "w") as file:
            file.write(gameState[1] + "\n" + gameState[2])