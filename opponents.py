from random import shuffle, choice, choices
from TicTacToe import TicTacToe



ALL_MOVES = [0, 1, 2, 3, 4, 5, 6, 7, 8]
CORNERS =   [0, 2, 6, 8]
CORNERS_SET = set(CORNERS)
MIDDLES =   [1, 3, 5, 7]
CENTER =    [4]

WINS = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6)
)

ROWS = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
)

COLS = (
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
)

DIAG = {
    (0, 4, 8),
    (2, 4, 6)
}

SWAP = {
    'X': 'O',
    'O': 'X'
}


class opponent:
    def __init__(self):
        self.letter = 'X'
        self.opponent = 'O'
        self.score = 0
        self.badCount = 0

    def setLetter(self, letter: str) -> None:
        self.letter = letter
        self.opponent = SWAP[letter]

    def move(self, game: TicTacToe) -> None:
        return



class EPIC(opponent):
    def __init__(self):
        super().__init__()
    
    def __repr__(self) -> str:
        return f'EPIC opponent'

    def move(self, game: TicTacToe) -> None:
        moves = []
        stopLose = []

        for positions in WINS:
            row = [game.board[p] for p in positions]
            match row:
                case [self.letter, self.letter, 0]:
                    game.move(positions[2])
                    return
                case [self.letter, 0, self.letter]:
                    game.move(positions[1])
                    return
                case [0, self.letter, self.letter]:
                    game.move(positions[0])
                    return
                case [self.opponent, self.opponent, 0]:
                    stopLose.append(positions[2])
                case [self.opponent, 0, self.opponent]:
                    stopLose.append(positions[1])
                case [0, self.opponent, self.opponent]:
                    stopLose.append(positions[0])
                case [self.letter, 0, 0]:
                    moves.extend([positions[1], positions[2]])
                case [0, self.letter, 0]:
                    moves.extend([positions[0], positions[2]])
                case [0, 0, self.letter]:
                    moves.extend([positions[0], positions[1]])
                case [self.opponent, 0, 0]:
                    moves.extend([positions[1], positions[2]])
                case [0, self.opponent, 0]:
                    moves.extend([positions[0], positions[2]])
                case [0, 0, self.opponent]:
                    moves.extend([positions[0], positions[1]])

        if len(stopLose):
            game.move(stopLose[0])
        elif len(moves):
            moveCounts = {m: moves.count(m) for m in set(moves)}
            bestCount = max(moveCounts.values())
            bestMoves = tuple(m for m, c in moveCounts.items() if c == bestCount)

            intersect = CORNERS_SET.intersection(bestMoves)
            if 4 in bestMoves:
                game.move(4)
            elif intersect:
                game.move(choice(tuple(intersect)))
            else:
                game.move(choice(bestMoves))
        else:
            shuffle(MIDDLES)
            shuffle(CORNERS)
            for m in CENTER + CORNERS + MIDDLES:
                if game.move(m):
                    break
