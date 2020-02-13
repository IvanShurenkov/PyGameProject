import pygame
pygame.init()

size = width, height = 1332, 703
screen = pygame.display.set_mode(size)
board_size_x, board_size_y = 33, 19
menu_size_x, menu_size_y = 3, 19
start_field = [[0] * board_size_x for _ in range(board_size_y)]
menu = [[0] * menu_size_x for _ in range(menu_size_y)]
ripe_time = 120

start_field[18][26] = 1
start_field[0][0] = 2
start_field[0][1] = 3
start_field[1][0] = 4
start_field[1][1] = 5
laboratory_array = []
menu_array = []
objects_array = [0 for _ in range(25)]
poison_r = [[[1, 1], [22, 1], [23, 1]], [[20, 1], [21, 1]], [[24, 60]], [[24, 30]], [[24, 65]], [[24, 40]], [[24, 10]],
            [[24, 30]], [], [], [], [], [], [], [], [], [], [[14, 1], [16, 1]], [[16, 1], [13, 1]],
            [[11, 1], [9, 1], [8, 1]], [[12, 1], [15, 1]], [[12, 1], [17, 1]], [[10, 1], [19, 1]], [[10, 1], [18, 1]],
            []]
