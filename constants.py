import pygame

size = width, height = 1332, 703
screen = pygame.display.set_mode(size)
board_size_x, board_size_y = 36, 19
start_field = [[0] * board_size_x for _ in range(board_size_y)]
start_field[18][26] = 1
start_field[0][0] = 2
start_field[0][1] = 3
