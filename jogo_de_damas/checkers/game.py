from .board import Board
from .constants import *
from .board import Board

import pygame

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
        
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
    
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = AZUL_MARINHO
        self.valid_moves = {}
        
    def winner(self):
        return self.board.winner()
    
    def reset(self):
        self._init()
    
    def select(self, row, col):
        if self.selected:
            result = self.move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        return False

    def move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False
        return True
    
    def draw_valid_moves(self, moves):
        """ Pinta os movimentos válidos de verde no tabuleiro.

        Args:
            moves(dict): dicionário com os movimentos válidos do jogador atual.
        """
        
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, GREEN_HIGHLIGHT, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)
    
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == AZUL_MARINHO:
            self.turn = WHITE
        else:
            self.turn = AZUL_MARINHO
            
    def agent_movement(self, board):
        """ Diferente de nós, o Agente não vai interagir diretamente com a API do PyGame. Para cada movimento do agente, criaremos outro tabuleiro.

        Args:
            board (Board): O Tabuleiro atual do jogo.
        """
        self.board = board
        self.change_turn()
        