from game import Game

class LevelController:
    def __init__(self, screen):
        game = Game()
        gameState = [0, 0, -2] # [-1: exit  0: restart level  1: next level, currentLevel, menuPage]

        while (gameState[0] != -1):
            gameState = game.Init(screen, gameState[0] + gameState[1], gameState[0] + gameState[2])

    def LoadGame(self):
        return [0, 3, 3]

    def SaveGame(self):
        pass