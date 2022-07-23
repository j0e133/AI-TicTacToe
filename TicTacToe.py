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

turnSwap = {
    'X': 'O',
    'O': 'X'
}



class TicTacToe:
    def __init__(self):
        self.board = [0 for _ in range(9)]
        self.turn = 'X'
        self.turnNum = 0

    def __repr__(self) -> str:
        return f'TicTacToe game | Turn {self.turnNum}, {self.turn} to move'

    def move(self, tile: int) -> bool:
        if not self.board[tile]:
            self.board[tile] = self.turn
            self.turn = turnSwap[self.turn]
            self.turnNum += 1
            return True
        return False

    def checkWin(self) -> str | None:
        for i in range(8):
            tiles = [self.board[t] for t in WINS[i]]
            if tiles[0] and tiles[:-1] == tiles[1:]:
                return tiles[0]
        if all(self.board):
            return 'Tie'

    def reset(self) -> None:
        self.board = [0 for _ in range(9)]
        self.turn = 'X'
        self.turnNum = 0

