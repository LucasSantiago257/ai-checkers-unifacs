from copy import deepcopy

from checkers.constants import AZUL_MARINHO, WHITE


def minimax(position, depth, max_player, game):
    """Run the minimax search on ``position`` until ``depth`` or terminal.

    Args:
        position (Board): Current board state to explore from.
        depth (int): Remaining search depth.
        max_player (bool): ``True`` if it is the AI (dark blue) turn.
        game (Game): Game instance, currently unused but kept for future hooks.

    Returns:
        tuple[int, Board]: Evaluation score and the associated board state.
    """
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position

    if max_player:
        max_eval = float("-inf")
        best_move = None
        for move in get_all_moves(position, AZUL_MARINHO, game):
            evaluation = minimax(move, depth - 1, False, game)[0]
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
        return max_eval, best_move

    min_eval = float("inf")
    best_move = None
    for move in get_all_moves(position, WHITE, game):
        evaluation = minimax(move, depth - 1, True, game)[0]
        if evaluation < min_eval:
            min_eval = evaluation
            best_move = move
    return min_eval, best_move


def simulate_move(piece, move, board, skipped):
    """Apply ``move`` to ``piece`` on ``board`` and remove any ``skipped`` pieces.

    Args:
        piece (Piece): Piece to move on the board.
        move (tuple[int, int]): Target row and column for the move.
        board (Board): Board to apply the move on (modified in place).
        skipped (list[Piece]): Captured pieces to remove, if any.

    Returns:
        Board: The board instance after the simulated move.
    """
    board.move(piece, move[0], move[1])
    if skipped:
        board.remove(skipped)
    return board


def get_all_moves(board, color, game):
    """Return every board state reachable by a single move from ``color``.

    Args:
        board (Board): Current board state to explore from.
        color (tuple[int, int, int]): RGB color that identifies the moving side.
        game (Game): Game instance, currently unused but kept for compatibility.

    Returns:
        list[Board]: All boards generated after every legal move.
    """
    moves = []
    for piece in board.get_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skipped in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, skipped)
            moves.append(new_board)
    return moves
