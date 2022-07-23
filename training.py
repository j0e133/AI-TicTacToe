import pygame
from random import shuffle, random, choice
from neuralNetwork import neuralNetwork, RELU, sigmoid
from TicTacToe import TicTacToe
from opponents import EPIC, opponent



layers = [10,   11,   12,   11,   10,   9]
aFuncs = [RELU, RELU, RELU, RELU, RELU, sigmoid]

INPUT_MAP = {
    'X': {
        'X': 0,
         0:  0.5,
        'O': 1
        },
    'O': {
        'O': 0,
         0:  0.5,
        'X': 1
        }
}

SWAP_LETTER = {
    'X': 'O',
    'O': 'X'
}

WIN = {
    5: 7,
    6: 7,
    7: 6,
    8: 6,
    9: 5
}

LOSE = {
    5: 1,
    6: 1,
    7: 2,
    8: 2,
    9: 3
}

AI_COUNT = 500

AI_50 = int(AI_COUNT * 0.5)
AI_10 = int(AI_COUNT * 0.1)
AI_KEPT = int(AI_COUNT * 0.3)
AI_NEW = AI_COUNT - AI_KEPT * 2



def boardToInputs(board: list[str, int], letter: str) -> list[int]:
    return [INPUT_MAP[letter][tile] for tile in board]



class sort:
    def __init__(self, value: float, tile: int):
        self.value = value
        self.tile = tile



class AIopponent:
    def __init__(self):
        self.brain = neuralNetwork(layers)
        self.letter = 'X'
        self.score = 0
        self.badCount = 0

    def __repr__(self) -> str:
        return f'AI opponent | Score {self.score}'
        # return f'AI opponent | Letter {self.letter}'

    def move(self, game: TicTacToe) -> None:
        ins = boardToInputs(game.board, self.letter) + [random()]
        self.brain.setInputs(ins)
        outs = [sort(out, i) for i, out in enumerate(self.brain.run())]

        for out in sorted(outs, key=lambda o: o.value):
            if game.move(out.tile):
                return
            else:
                self.badCount += 1
    
    def setLetter(self, letter: str) -> None:
        self.letter = letter

    def child(self):
        new = AIopponent()
        new.brain = self.brain.child()
        return new



class population:
    def __init__(self):
        good = AIopponent()
        good.brain = neuralNetwork.load('saves/gen1111.json')
        self.toPlay = [AIopponent() for _ in range(AI_COUNT - 1)] + [good]
        self.played: list[AIopponent] = []
        self.all = self.toPlay.copy()

    def __repr__(self) -> str:
        return f'Population | {len(self.toPlay)} left to play | {len(self.played)} already played'

    def getOpponent(self) -> AIopponent:
        if len(self.toPlay):
            opponent = self.toPlay.pop()
            self.played.append(opponent)
            return opponent

    def newGeneration(self) -> float | AIopponent:
        sortedAI = sorted(self.played, key=lambda member: member.score - member.badCount * 0.25)

        bestAI = sortedAI[-1]

        bestScore = bestAI.score
        avgScore = sum(AI.score for AI in self.played) / AI_COUNT
        t50AvgScore = sum(AI.score for AI in sortedAI[-AI_50:]) / AI_50
        t10AvgScore = sum(AI.score for AI in sortedAI[-AI_10:]) / AI_10

        bestBads = min(AI.badCount for AI in self.played)
        avgBads = sum(AI.badCount for AI in self.played) / AI_COUNT
        t50Bads = sum(AI.badCount for AI in sortedAI[-AI_50:]) / AI_50
        t10Bads = sum(AI.badCount for AI in sortedAI[-AI_10:]) / AI_10

        best = sortedAI[-AI_KEPT:]
        for ai in best:
            ai.score = 0
            ai.badCount = 0
        self.toPlay = best
        self.toPlay.extend(b.child() for b in best.copy())
        self.toPlay.extend(AIopponent() for _ in range(AI_NEW))
        shuffle(self.toPlay)
        self.played = []
        self.all = self.toPlay.copy()

        return [avgScore, bestScore, t50AvgScore, t10AvgScore, bestBads, avgBads, t50Bads, t10Bads], bestAI



class Trainer:
    def __init__(self):
        self.population = population()
        self.gameNum = 0
        self.generation = 1
        self.stats = [0, 0, 0, 0, 0, 0, 0, 0]
        self.prevBest: AIopponent = AIopponent()
        self.opponent: opponent = EPIC()
        self.gamesPlayed = 0

    def __repr__(self) -> str:
        return f'Trainer | Game {self.gameNum} | Generation {self.generation}'

    def update(self) -> None:
        winner = self.game.checkWin()

        if winner is None:
            # self.ai.move(self.game)
            self.toMove.move(self.game)
            self.toMove = self.moveSwap[self.toMove]
        else:
            self.gamesPlayed += 1
            if winner == 'Tie':
                self.ai.score += 4
            elif winner == self.ai.letter:
                self.ai.score += WIN[self.game.turnNum]
            else:
                self.ai.score += LOSE[self.game.turnNum]

            if self.gamesPlayed == 10:
                self.gamesPlayed = 1
                self.newGame()
            else:
                self.toMove = self.ai if (self.gamesPlayed % 2) == 0 else self.opponent
                self.ai.letter = SWAP_LETTER[self.ai.letter]
                self.opponent.letter = SWAP_LETTER[self.opponent.letter]
                self.game.reset()

    def newGame(self):
        if len(self.population.toPlay) == 0:
            self.stats, self.prevBest = self.population.newGeneration()
            self.generation += 1
            self.gameNum = 0

        self.ai = self.population.getOpponent()
        self.ai.setLetter('X')

        self.opponent = choice(self.population.all)
        self.opponent.setLetter('O')

        self.toMove = self.ai
        self.moveSwap = {
            self.ai: self.opponent,
            self.opponent: self.ai
        }

        self.game = TicTacToe()
        self.gameNum += 1
