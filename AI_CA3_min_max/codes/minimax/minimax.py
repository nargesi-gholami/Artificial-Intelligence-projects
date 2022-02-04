import copy
import pygame
from checkers.board import Board
from checkers.pieces import Piece

RED = (255,0,0)
WHITE = (255,255,255)
INFINITY_MAX = 1e4
INFINITY_MIN = -1e4


def minimax(board , depth, maxPlayer):
    if(depth < 0):
        return board.evaluate(), board

    moves = []
    color = WHITE if maxPlayer else RED
    v = INFINITY_MIN if maxPlayer else INFINITY_MAX
    
    finalBoard = copy.deepcopy(board)
    pieces = board.getAllPieces(color)
    for piece in pieces:
        moves_right, moves_left = board.getValidMoves(piece)
        moves = [moves_right, moves_left]
        for move in moves: 
            if not len(move):
                continue
            sampleBoard = copy.deepcopy(board)
            samplePiece = sampleBoard.getPiece(piece.row, piece.col)
            sampleBoard = simulateMove(samplePiece, move, sampleBoard, color, len(move))
            newV, newBoard = minimax (sampleBoard , depth-1, not maxPlayer)
            if (maxPlayer and v < newV) or (not maxPlayer and v > newV):
                finalBoard = copy.deepcopy(sampleBoard)
                v = newV
            
    return v, finalBoard  
    

def simulateMove(piece, move, board, color, skip):
    if(skip > 1):
        board.move(piece, move[-1][0], move[-1][1])
        i = 0
        while i < len(move):
            board.remove2(move[i][0], move[i][1], color)
            i += 2
    else:
        board.move(piece, move[0][0], move[0][1])
     
    return board
