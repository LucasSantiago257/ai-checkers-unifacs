from .constants import *
import pygame


class Piece:
    """Represents an individual checker piece and its rendering helpers."""
    PADDING = 10
    OUTLINE = 2


    def __init__(self, color, row, col):
        """Initialize a piece at ``(row, col)`` with the given ``color``.

        Args:
            color (tuple): RGB tuple for the player.
            row (int): Initial row position.
            col (int): Initial column position.

        Returns:
            None
        """
        self.color = color
        self.row = row
        self.col = col
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        """Update the screen coordinates according to the current row and column.

        Args:
            None

        Returns:
            None
        """
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        """Promote the piece to king status.

        Args:
            None

        Returns:
            None
        """
        self.king = True
    
    def draw(self, win):
        """Draw the piece on ``win`` including outline and crown if needed.

        Args:
            win (pygame.Surface): Surface onto which the piece is drawn.

        Returns:
            None
        """
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, LIGHT_YELLOW, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def move(self, row, col):
        """Update the grid position of the piece and recalculate pixel coordinates.

        Args:
            row (int): New row.
            col (int): New column.

        Returns:
            None
        """
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        """Return the string representation of the piece color tuple.

        Args:
            None

        Returns:
            str: String version of the color tuple.
        """
        return str(self.color)
