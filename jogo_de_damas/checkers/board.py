import pygame
from .constants import BLACK, ROWS, COLS, PERU, SQUARE_SIZE, AZUL_MARINHO, WHITE
from .piece import Piece

# Esse arquivo lida com a lógica do tabuleiro de damas, incluindo a criação do tabuleiro, movimentação das peças, remoção de peças capturadas e verificação de movimentos válidos.

class Board:
    def __init__(self):
        self.board = []
        self.darkblue_left = self.white_left = 12
        self.darkblue_kings = self.white_kings = 0
        self.create_board()
    
    def get_piece(self, row, col):
        return self.board[row][col]

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, PERU, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if (row == ROWS - 1 or row == 0) and piece.king is False:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.darkblue_kings += 1

    def create_board(self):
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
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == AZUL_MARINHO:
                    self.darkblue_left -= 1
                else:
                    self.white_left -= 1
    
    def evaluate_board(self):
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
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                neighbor = self.board[r][c]
                if neighbor != 0 and neighbor.color == piece.color:
                    return True
        return False
    
    
                    
    def winner(self):
        if self.darkblue_left <= 0:
            print("Brancas Vencem")
            return WHITE
        elif self.white_left <= 0:
            print("Azul Marinho Vence")
            return AZUL_MARINHO
        return None

    def get_valid_moves(self, piece, check_captures=True):
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
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    valid_moves = self.get_valid_moves(piece, check_captures=False)
                    for move, skipped in valid_moves.items():
                        if skipped:
                            return True
        return False