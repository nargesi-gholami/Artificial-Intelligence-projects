from typing import Tuple
import pygame

from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .pieces import Piece

class Board:


    	
    def __init__(self):
        self.board = []
        self.redLeft = self.whiteLeft = 16
        self.redKings = self.whiteKings = 0
        self.createBoard()
    
    def drawSquares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        return self.whiteLeft - self.redLeft + (self.whiteKings * 0.5 - self.redKings * 0.5)

    def getAllPieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        self.board[piece.row][piece.col] = 0
        piece.move(row, col)
        if row == ROWS - 1 or row == 0:
            piece.makeKing()
            if piece.color == WHITE:
                self.whiteKings += 1
            else:
                self.redKings += 1 

    def getPiece(self, row, col):#ok
        return self.board[row][col]

    def createBoard(self):#ok
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        
    def draw(self, win):#ok
        self.drawSquares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
    
    def remove2(self, x, y, turn):
        self.board[x][y] = 0
        if turn == RED:
            self.whiteLeft -= 1
        else:
            self.redLeft -= 1
    
    def winner(self):
        if self.redLeft <= 0:
            return WHITE
        elif self.whiteLeft <= 0:
            return RED
        
        return None 
    
    def getValidMoves(self, piece):
        
        step = -1 if piece.color == RED else 1  #red --> step = -1 
        if piece.king:
            moves_left = (self._traverseLeft(piece.row+1, piece.row+3, 1, piece.color, piece.col-1, skipped=[]))
            moves_right = (self._traverseRight(piece.row+1, piece.row+3, 1, piece.color, piece.col+1, skipped=[]))
            moves_left2 = (self._traverseLeft(piece.row-1,  piece.row-3, -1, piece.color, piece.col-1, skipped=[]))
            moves_right2 = (self._traverseRight(piece.row-1,  piece.row-3, -1, piece.color, piece.col+1, skipped=[]))
            if moves_left2:
                for i in range(len(moves_left2)):
                    moves_left.append(moves_left2[i])
            if moves_right2:
                for i in range(len(moves_right2)):
                    moves_right.append(moves_right2[i])
            

        elif piece.color == RED:
            moves_left = self._traverseLeft(piece.row-1 ,  piece.row-3, step, RED, piece.col-1, skipped=[])
            moves_right = self._traverseRight(piece.row-1 , piece.row-3, step, RED, piece.col+1, skipped=[])

        elif piece.color == WHITE:
            moves_left = (self._traverseLeft(piece.row+1 , piece.row+3, step, WHITE, piece.col-1, skipped=[]))
            moves_right = (self._traverseRight(piece.row+1 ,piece.row+3, step, WHITE, piece.col+1, skipped=[]))
         
        return moves_right, moves_left


    def _traverseLeft(self, start, stop, step, color, left, skipped=[]):
        moves = []
        seen = []
        for r in range(start, stop, step):
            if left < 0 or r < 0 or r >= ROWS:
                break   
            current = self.board[r][left]
            if current == 0:
                if skipped and not seen:
                    break
                elif skipped:
                    for i in range(len(skipped)):
                        moves.append(skipped[i])
                    moves.append(seen[0])
                    moves.append((r,left))
                else:
                    if seen:
                        moves.append(seen[0])
                    moves.append((r, left))

                if seen:
                    if step == -1:
                        row = r-3
                    else:
                        row = r+3
                        
                    newMoves1 = (self._traverseLeft(r+step, row, step, color, left-1, skipped=moves))
                    newMoves2 = (self._traverseRight(r+step, row, step, color, left+1, skipped=moves))
                    if newMoves1:
                        moves = newMoves1
                    elif newMoves2:
                        moves = newMoves2
                break
            elif current.color == color:
                break
            else:#another color
                if seen:
                    break
                else:
                    seen.append((r, left))
                

            left -= 1
        return moves

    def _traverseRight(self, start, stop, step, color, right, skipped=[]):
        moves = []
        seen = []
        for r in range(start, stop, step):
            if right >= COLS or r < 0 or r >= ROWS:
                break
            current = self.board[r][right]
            if current == 0:
                if skipped and not seen:
                    break
                elif skipped:
                    for i in range(len(skipped)):
                        moves.append(skipped[i])
                    moves.append(seen[0])
                    moves.append((r, right))
                else:
                    if seen:
                        moves.append(seen[0])
                    moves.append((r, right))

                if seen:
                    if step == -1:
                        row = r-3
                    else:
                        row = r+3
                    newMoves1 = (self._traverseLeft(r+step, row, step, color, right-1, skipped=moves))
                    newMoves2 = (self._traverseRight(r+step, row, step, color, right+1, skipped=moves))

                    if newMoves1:
                        moves = newMoves1
                    elif newMoves2:
                        moves = newMoves2
                break

            elif current.color == color:
                break
            else:#another color
                if seen:
                    break
                else:
                    seen.append((r, right))
                

            right += 1
        return moves