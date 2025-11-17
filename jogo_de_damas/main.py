# Agradecimento ao TechWithTim que serviu como base para a criação desse projeto
# Demais créditos estão no README.md

# Esse arquivo lida principalmente com a inicialização do Pygame, o loop principal do jogo e a captura de eventos do usuário.

import pygame
from checkers.constants import * 
from checkers.board import Board
from checkers.game import Game
from minimax.agent import minimax


FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
game = Game(WIN)
AI_COLOR = AZUL_MARINHO
AI_MAX_PLAYER = AI_COLOR == AZUL_MARINHO
AI_DEPTH = 3

def get_row_and_column_from_mpos(pos):
        """Return the board coordinates that correspond to the mouse position.

        Args:
            pos (tuple[int, int]): Mouse coordinates in pixels.

        Returns:
            tuple[int, int]: Row and column indexes.
        """
        x, y = pos
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        return row, col


pygame.display.set_caption('Jogo de Damas')

def main():
    """Initialize pygame and run the event loop until the window is closed.

    Args:
        None

    Returns:
        None
    """
    run = True
    clock = pygame.time.Clock()
    board = Board()
    game = Game(WIN)

    while run:
        clock.tick(FPS)
        if game.turn == AI_COLOR and game.winner() is None:
            _, new_board = minimax(game.board, AI_DEPTH, AI_MAX_PLAYER, game)
            game.agent_movement(new_board)
        
        if game.winner() != None:
            print(f"{game.winner()} venceu!")
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_and_column_from_mpos(pos)
                game.select(row, col)
                
        game.update()
    pygame.quit()

main()
