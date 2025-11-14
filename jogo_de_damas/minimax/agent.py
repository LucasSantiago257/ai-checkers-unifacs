from copy import deepcopy
import pygame
from jogo_de_damas.checkers.constants import *
from jogo_de_damas.checkers.game import Game

def minimax(position, depth, max_player, game):
    """Recursive minimax helper that returns the best score and board state.

    Args:
        position (Board): Current board state to evaluate.
        depth (int): Remaining search depth.
        max_player (bool): Whether the current layer maximizes or minimizes.
        game (Game): Game controller, used when copying boards.

    Returns:
        tuple[int, Board]: Computed evaluation score and resulting board.
    """
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    
    if max_player:
        max_eval = float('-inf')
    elif not max_player:
        min_eval = float('inf')
    
    
