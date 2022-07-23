import pygame
from TicTacToe import TicTacToe
from training import Trainer


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORKEY = (255, 0, 255)

TILE_TO_POS = [
    (469, 200),
    (614, 201),
    (746, 190),
    (474, 331),
    (625, 320),
    (744, 322),
    (470, 464),
    (614, 451),
    (742, 464)
]





SCREEN = pygame.display.set_mode((1280, 720))

BOARD = pygame.image.load('Sprites/board.png').convert(SCREEN)
BOARD.set_colorkey(COLORKEY)

X = pygame.image.load('Sprites/X.png').convert(SCREEN)
X.set_colorkey(COLORKEY)

O = pygame.image.load('Sprites/O.png').convert(SCREEN)
O.set_colorkey(COLORKEY)

STR_TO_IMG = {
    'X': X,
    'O': O
}

FONT = pygame.font.SysFont(None, 80, True)
FONT_SMALL = pygame.font.SysFont(None, 50, True)
FONT_TINY = pygame.font.SysFont(None, 22, True)



def draw(game: TicTacToe, trainer: Trainer):

    SCREEN.fill(WHITE)

    SCREEN.blit(BOARD, (0, 0))

    for i in range(9):
        tile = game.board[i]
        if tile:
            SCREEN.blit(STR_TO_IMG[tile], TILE_TO_POS[i])

    text = FONT.render(f'Generation {trainer.generation}', True, BLACK)
    rect = text.get_rect(center=(640, 40))
    SCREEN.blit(text, rect)
    
    text = FONT_SMALL.render(f'Game {trainer.gameNum}', True, BLACK)
    rect = text.get_rect(center=(640, 80))
    SCREEN.blit(text, rect)
    
    text = FONT_TINY.render(f'Avg score: {round(trainer.stats[0], 3)}', True, BLACK)
    rect = text.get_rect(topleft=(5, 5))
    SCREEN.blit(text, rect)

    text = FONT_TINY.render(f'Best score: {round(trainer.stats[1], 3)}', True, BLACK)
    rect = text.get_rect(topleft=(5, 25))
    SCREEN.blit(text, rect)

    text = FONT_TINY.render(f'Top 50% avg score: {round(trainer.stats[2], 3)}', True, BLACK)
    rect = text.get_rect(topleft=(5, 45))
    SCREEN.blit(text, rect)

    text = FONT_TINY.render(f'Top 10% avg score: {round(trainer.stats[3], 3)}', True, BLACK)
    rect = text.get_rect(topleft=(5, 65))
    SCREEN.blit(text, rect)

    pygame.display.flip()
