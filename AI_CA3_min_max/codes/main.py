import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minimax.minimax import minimax

FPS = 60

WHITE_DEPTH = 3
RED_DEPTH = 2

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def getRowColFromMouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

if __name__ == '__main__':
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    t = 0
    while run:
        t += 1
        clock.tick(FPS)
        if game.winner() != None:
            print(game.winner())
            run = False

        if game.turn == WHITE:#maximize score
            value, newBoard = minimax(game.getBoard(), WHITE_DEPTH, True)
            game.aiMove(newBoard)

        elif game.turn == RED:#minimize score
            value, newBoard = minimax(game.getBoard(), RED_DEPTH, False)
            game.aiMove(newBoard)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        game.update()
        clock.tick(1.5)  
    
    pygame.quit()