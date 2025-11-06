import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

#definir cores
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
AZUL_MARINHO = (0, 0, 128)

# Testando cores
PERU = (205,133,63)
SADDLE_BROWN = (139,69,19)
LIGHT_YELLOW = (255, 255, 224)

# Cores para destaque
GREEN_HIGHLIGHT = (144, 238, 144)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))