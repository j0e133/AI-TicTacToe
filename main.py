import pygame, sys
pygame.init()
from TicTacToe import TicTacToe
from training import Trainer, AIopponent
from neuralNetwork import neuralNetwork
from draw import draw, BOARD
from opponents import *


screen = pygame.display.get_surface()
clock = pygame.time.Clock()


trainer = Trainer()
trainer.newGame()


COL_TO_TILE = {
    (236, 28,  36):  0,
    (255, 127, 39):  1,
    (255, 242, 0):   2,
    (5,   117, 36):  3,
    (14,  209, 69):  4,
    (140, 255, 251): 5,
    (0,   168, 243): 6,
    (63,  72,  204): 7,
    (162, 63,  204): 8
}



def EPICMOVE(game: TicTacToe) -> None:
    op = EPIC()
    op.setLetter(game.turn)
    op.move(game)



def close():
    trainer.prevBest.brain.save()
    pygame.quit()
    sys.exit()



def normInput():
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                close()
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_d:
                        draw(trainer.game, trainer)
                    case pygame.K_SPACE:
                        global stop, inputFunc
                        stop = True
                        game.reset()
                        inputFunc = playInput



def playInput():
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                close()
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_r:
                        game.reset()
                        draw(game, trainer)
                    case pygame.K_d:
                        draw(game, trainer)
                    case pygame.K_m:
                        trainer.prevBest.move(game)
                        draw(game, trainer)
                    case pygame.K_f:
                        draw(game, trainer)
                    case pygame.K_SPACE:
                        global stop, inputFunc
                        stop = False
                        inputFunc = normInput
            case pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    color = tuple(BOARD.get_at(event.pos))[:-1]
                    if color in COL_TO_TILE:
                        tile = COL_TO_TILE[color]
                        if game.move(tile):

                            trainer.prevBest.move(game)

                            draw(game, trainer)
                            tile = None



game = TicTacToe()
# stop = True
# inputFunc = playInput
stop = False
inputFunc = normInput

frame = 1

draw(trainer.game, trainer)

while True:
    inputFunc()

    if not stop:
        trainer.update()
        if frame % 10 == 0:
            draw(trainer.game, trainer)

        frame += 1
