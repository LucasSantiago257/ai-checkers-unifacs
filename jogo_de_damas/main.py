import pygame
from checkers.constants import *
from checkers.board import Board


FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
board = Board()

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
                piece = board.get_piece(row, col)
        board.draw(WIN)
        pygame.display.update()
    pygame.quit()

main()