from .board import Board
from .constants import *
from .board import Board

import pygame

class Game:
    """High-level game controller that tracks turns and user interaction."""
    def __init__(self, win):
        """Store ``win`` surface and set the game to its initial state.

        Args:
            win (pygame.Surface): Surface that displays the game.

        Returns:
            None
        """
        self._init()
        self.win = win
        
    def update(self):
        """Redraw the board, show valid moves, and flip the Pygame buffer.

        Args:
            None

        Returns:
            None
        """
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
    
    def _init(self):
        """Reset the board, selected piece, and turn trackers.

        Args:
            None

        Returns:
            None
        """
        self.selected = None
        self.board = Board()
        self.turn = AZUL_MARINHO
        self.valid_moves = {}
        
    def winner(self):
        """Return the color that has already won, if any.

        Args:
            None

        Returns:
            tuple | None: Color tuple of the winner or ``None`` otherwise.
        """
        return self.board.winner()
    
    def reset(self):
        """Restart the entire game.

        Args:
            None

        Returns:
            None
        """
        self._init()
    
    def select(self, row, col):
        """Handle user selection logic and compute valid moves for that piece.

        Args:
            row (int): Row that was clicked.
            col (int): Column that was clicked.

        Returns:
            bool: ``True`` if the selection is valid.
        """
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
        """Move the currently selected piece to ``(row, col)`` when legal.

        Args:
            row (int): Destination row.
            col (int): Destination column.

        Returns:
            bool: ``True`` if the move was performed.
        """
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
        """Draw a small highlight for every coordinate contained in ``moves``.

        Args:
            moves (dict): Mapping of destinations to skipped pieces.

        Returns:
            None
        """
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, GREEN_HIGHLIGHT, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)
    
    def change_turn(self):
        """Switch the active player and clear cached moves.

        Args:
            None

        Returns:
            None
        """
        self.valid_moves = {}
        if self.turn == AZUL_MARINHO:
            self.turn = WHITE
        else:
            self.turn = AZUL_MARINHO
            
    def agent_movement(self, board):
        """Update the internal board with an agent-produced state and pass the turn.

        Args:
            board (Board): New board instance returned by the AI.

        Returns:
            None
        """
        self.board = board
        self.change_turn()
        
