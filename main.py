import pygame
from constants import screen, board_size_x, board_size_y, size, start_field
from images import grass_image, tree_image, load_image
from groups import all_grass
import time


class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.image = tree_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Grass(pygame.sprite.Sprite):
    def __init__(self, x, y, group=all_grass):
        super().__init__(group)
        self.image = grass_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = start_field
        self.left = 0
        self.top = 0
        self.cell_size = 37
        self.counter = 0


board = Board(board_size_x, board_size_y)

for i in range(board_size_x):
    for j in range(board_size_y):
        Grass(i * board.cell_size, j * board.cell_size)

all_grass.draw(screen)

for i in range(board_size_y):
    for j in range(board_size_x):
        if start_field[i][j] == 1:
            tree = pygame.sprite.Group()
            Tree(j * board.cell_size, i * board.cell_size, tree)
            tree.draw(screen)
running = True

x, y = 26, 18

# t = time.time()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    '''t1 = time.time()
    if t1 - t >= 1:
        tree = pygame.sprite.Group()
        grass = pygame.sprite.Group()
        Grass(x * board.cell_size, y * board.cell_size, grass)
        grass.draw(screen)
        x -= 1
        y -= 1
        Tree(x * board.cell_size, y * board.cell_size, tree)
        tree.draw(screen)
        t = t1'''
    pygame.display.flip()
