import pygame
from checkers.constants import WIDTH, HEIGHT
from checkers.board import Board


FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
board = Board()

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
        board.draw_squares(WIN)
        pygame.display.update()
    pygame.quit()

main()