import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from checkers.board import Board

class Game:

    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.validMoves = {}

    def winner(self):
        return self.board.winner()

    def changeTurn(self):#ok
        self.validMoves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def getBoard(self):#ok
        return self.board

    def aiMove(self, board):#ok
        self.board = board
        self.changeTurn()