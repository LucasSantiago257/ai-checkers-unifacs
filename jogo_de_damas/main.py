# Agradecimento ao TechWithTim que serviu como base para a criação desse projeto
# Demais créditos estão no README.md

import pygame
from checkers.constants import * 
from checkers.board import Board
from checkers.game import Game


FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
game = Game(WIN)

def get_row_and_column_from_mpos(pos):
        x, y = pos
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        return row, col


pygame.display.set_caption('Jogo de Damas')

def main():
    run = True
    clock = pygame.time.Clock()
    board = Board()

    while run:
        clock.tick(FPS)

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