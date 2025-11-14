from copy import deepcopy
import pygame
from jogo_de_damas.checkers.constants import *
from jogo_de_damas.checkers.game import Game

def minimax(position, depth, max_player, game):
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    
    if max_player:
        max_eval = float('-inf')
    
    