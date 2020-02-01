import pygame
pygame.init()

size = width, height = 1332, 703
screen = pygame.display.set_mode(size)
board_size_x, board_size_y = 33, 19
menu_size_x, menu_size_y = 3, 19
start_field = [[0] * board_size_x for _ in range(board_size_y)]
menu = [[0] * menu_size_x for _ in range(menu_size_y)]
start_field[18][26] = 1
start_field[0][0] = 2
start_field[0][1] = 3
start_field[1][0] = 4
start_field[1][1] = 5
menu_array = [[1, 5]]
