import pygame
from .constants import BLACK, ROWS, COLS, PERU, SQUARE_SIZE, AZUL_MARINHO, WHITE
from .piece import Piece

# Esse arquivo lida com a lógica do tabuleiro de damas, incluindo a criação do tabuleiro, movimentação das peças, remoção de peças capturadas e verificação de movimentos válidos.

class Board:
    """Represents the checkers board along with all move-generation logic."""

    def __init__(self):
        """Create an empty board matrix and populate it with the initial layout.

        Args:
            None

        Returns:
            None
        """
        self.board = []
        self.darkblue_left = self.white_left = 12
        self.darkblue_kings = self.white_kings = 0
        self.create_board()
    
    def get_piece(self, row, col):
        """Return the piece that sits on ``(row, col)``.

        Args:
            row (int): Matrix row.
            col (int): Matrix column.

        Returns:
            Piece | int: Piece instance or 0 if the square is empty.
        """
        return self.board[row][col]

    def draw_squares(self, win):
        """Draw the alternating background squares onto ``win``.

        Args:
            win (pygame.Surface): Surface that receives the board background.

        Returns:
            None
        """
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, PERU, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    def move(self, piece, row, col):
        """Move ``piece`` to ``(row, col)`` and crown it if it reaches the far rank.

        Args:
            piece (Piece): Piece being moved.
            row (int): Target row.
            col (int): Target column.

        Returns:
            None
        """
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if (row == ROWS - 1 or row == 0) and piece.king is False:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.darkblue_kings += 1

    def create_board(self):
        """Populate the board with alternating empty squares and the starting pieces.

        Args:
            None

        Returns:
            None
        """
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(AZUL_MARINHO, row, col))
                    elif row > 4:
                        self.board[row].append(Piece(WHITE, row, col))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
    
    def draw(self, win):
        """Render the full board and all pieces onto ``win``.

        Args:
            win (pygame.Surface): Surface that receives the rendered board.

        Returns:
            None
        """
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        """Remove ``pieces`` after a capture and update piece counters.

        Args:
            pieces (list[Piece]): Captured pieces to remove.

        Returns:
            None
        """
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == AZUL_MARINHO:
                    self.darkblue_left -= 1
                else:
                    self.white_left -= 1
    
    def evaluate_board(self):
        """Return a heuristic score from the dark blue point of view.

        Args:
            None

        Returns:
            int: Positive values favor dark blue, negative favor white.
        """
        score = 0
        
        score += (self.darkblue_left - self.white_left) * 10
        
        score += (self.darkblue_kings - self.white_kings) * 15
        
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    position_value = 0
                    
                    # Peças no centro valem mais
                    if 2 <= row <= 5 and 2 <= col <= 5:
                        position_value += 3
                    
                    # Peças avançadas valem mais
                    if piece.color == AZUL_MARINHO:
                        position_value += row 
                    else:
                        position_value += (ROWS - 1 - row)  # 

                    if col == 0 or col == COLS - 1:
                        position_value -= 2
                    

                    if self._is_protected(piece, row, col):
                        position_value += 2
                    
                    if piece.color == AZUL_MARINHO:
                        score += position_value
                    else:
                        score -= position_value
            return score
    
    def _is_protected(self, piece, row, col):
        """Return ``True`` if ``piece`` has a friendly neighbor diagonally adjacent.

        Args:
            piece (Piece): Piece being evaluated.
            row (int): Piece row.
            col (int): Piece column.

        Returns:
            bool: ``True`` if a friendly neighbor exists.
        """
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                neighbor = self.board[r][c]
                if neighbor != 0 and neighbor.color == piece.color:
                    return True
        return False
    
    def get_pieces(self, color):
        """Return a list with all pieces of ``color`` still on the board.

        Args:
            color (tuple): RGB tuple that represents the owner color.

        Returns:
            list[Piece]: All pieces that match the color.
        """
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color: # A representação interna do quadrado vazio é 0
                    # por isso fazemos essa verificação
                    pieces.append(piece)
        return pieces
    
    
                    
    def winner(self):
        """Return the winning color if one side has no pieces left.

        Args:
            None

        Returns:
            tuple | None: Color of the winner or ``None`` if game continues.
        """
        if self.darkblue_left <= 0:
            print("Brancas Vencem")
            return WHITE
        elif self.white_left <= 0:
            print("Azul Marinho Vence")
            return AZUL_MARINHO
        return None

    def get_valid_moves(self, piece, check_captures=True):
        """Return every legal target square for ``piece`` and any captured pieces.

        Args:
            piece (Piece): Piece to evaluate.
            check_captures (bool, optional): Whether to enforce the capture priority.

        Returns:
            dict[tuple, list]: Mapping of (row, col) to a list of captured pieces.
        """
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.king:
            moves.update(self.king_traverse_left(row -1, -1, -1, piece.color, left))
            moves.update(self.king_traverse_right(row -1, -1, -1, piece.color, right))
            moves.update(self.king_traverse_left(row +1, ROWS, 1, piece.color, left))
            moves.update(self.king_traverse_right(row +1, ROWS, 1, piece.color, right))
        if piece.color == WHITE:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == AZUL_MARINHO:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
        
        if check_captures:
            possible_captures = self.check_possible_capture(piece.color)    
            if possible_captures:
                moves = {move: skipped for move, skipped in moves.items() if skipped}
        
        return moves
        
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        """Traverse diagonally left to find simple moves or multi-jump continuations.

        Args:
            start (int): Starting row.
            stop (int): Stopping row boundary (exclusive).
            step (int): Row increment direction.
            color (tuple): Color of the moving piece.
            left (int): Starting column.
            skipped (list, optional): Pieces captured so far in the path.

        Returns:
            dict[tuple, list]: Candidate moves and their captured pieces.
        """
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
                    
            left -= 1
        return moves
                
    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        """Traverse diagonally right to find simple moves or multi-jump continuations.

        Args:
            start (int): Starting row.
            stop (int): Stopping row boundary (exclusive).
            step (int): Row increment direction.
            color (tuple): Color of the moving piece.
            right (int): Starting column.
            skipped (list, optional): Pieces captured so far in the path.

        Returns:
            dict[tuple, list]: Candidate moves and their captured pieces.
        """
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
                    
            right += 1
        return moves
    
    def king_traverse_left(self, start, stop, step, color, left, skipped=[]):
        """Traverse along the left diagonal for king pieces, allowing long moves.

        Args:
            start (int): Starting row.
            stop (int): Stopping row boundary.
            step (int): Row increment direction.
            color (tuple): Color of the king piece.
            left (int): Starting column.
            skipped (list, optional): Pieces captured so far in the path.

        Returns:
            dict[tuple, list]: Candidate moves and their captured pieces.
        """
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = -1
                    else:
                        row = ROWS
                    moves.update(self.king_traverse_left(r+step, row, step, color, left-1, skipped=last))
                    moves.update(self.king_traverse_right(r+step, row, step, color, left+1, skipped=last))
                    break
            elif current.color == color:
                break
            else:
                last = [current]
            
            left -= 1
        return moves
    
    def king_traverse_right(self, start, stop, step, color, right, skipped=[]):
        """Traverse along the right diagonal for king pieces, allowing long moves.

        Args:
            start (int): Starting row.
            stop (int): Stopping row boundary.
            step (int): Row increment direction.
            color (tuple): Color of the king piece.
            right (int): Starting column.
            skipped (list, optional): Pieces captured so far in the path.

        Returns:
            dict[tuple, list]: Candidate moves and their captured pieces.
        """
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = -1
                    else:
                        row = ROWS
                    moves.update(self.king_traverse_left(r+step, row, step, color, right-1, skipped=last))
                    moves.update(self.king_traverse_right(r+step, row, step, color, right+1, skipped=last))
                    break
            elif current.color == color:
                break
            else:
                last = [current]
            
            right += 1
        return moves
    
    def check_possible_capture(self, color):
        """Return ``True`` if any piece of ``color`` can capture an opponent.

        Args:
            color (tuple): Color to check.

        Returns:
            bool: ``True`` if there is at least one capture available.
        """
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    valid_moves = self.get_valid_moves(piece, check_captures=False)
                    for move, skipped in valid_moves.items():
                        if skipped:
                            return True
        return False
