import pygame
from constants import screen, board_size_x, board_size_y, size, start_field, menu_size_x, menu_size_y, menu_array
from images import grass_image, tree_image, stone_image1, stone_image2, shovel_image, \
                   zombie_down, zombie_left, zombie_right, zombie_up, bed_image, cell_image, laboratory_image
from groups import all_grass, zombies, all_cell
from algorithm import bfs
import time


class FieldImage(pygame.sprite.Sprite):
    def __init__(self, x, y, image, group):
        super().__init__(group)
        if image == 1:
            self.image = tree_image
        elif image == 2:
            self.image = stone_image1
        elif image == 3:
            self.image = stone_image2
        elif image == 4:
            self.image = bed_image
        elif image == 5:
            self.image = laboratory_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class MenuImage(pygame.sprite.Sprite):
    def __init__(self, x, y, image, group):
        super().__init__(group)
        if image[0] == 1:
            self.image = shovel_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class CellMenu(pygame.sprite.Sprite):
    def __init__(self, x, y, group=all_cell):
        super().__init__(group)
        self.image = cell_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, group, move, moment):  # move = [y, x]
        super().__init__(group)
        if move == [1, 0]:
            self.image = zombie_right[moment]
        elif move == [-1, 0]:
            self.image = zombie_left[moment]
        elif move == [0, -1]:
            self.image = zombie_up[moment]
        else:
            self.image = zombie_down[moment]
        self.turn = 0
        self.move = 0
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
        self.flag = True
        self.x = -1
        self.y = -1
        self.effect, self.id = -1, -1
        self.menu = menu_array

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            # print(cell)
            if cell[4]:
                return self.on_click(cell)
            else:
                return self.action(cell)
        else:
            # print(None)
            return []

    def action(self, cell_coords):
        pos_x, pos_y, w, h, flag = cell_coords
        if self.effect == -1:
            if len(self.menu) > h * menu_size_x + w:
                self.effect = self.menu[h * menu_size_x + w][0]
                self.id = h * menu_size_x + w
        else:
            self.effect = -1
        return []

    def get_cell(self, mouse_pos):
        pos_x = self.left
        pos_y = self.top
        for i in range(self.height):
            for j in range(self.width):
                if pos_x <= mouse_pos[0] <= pos_x + self.cell_size and pos_y <= mouse_pos[1] <= pos_y + self.cell_size:
                    return pos_x, pos_y, j, i, 1
                pos_x += self.cell_size
            pos_x = self.left
            pos_y += self.cell_size
        pos_x = self.left
        pos_y = self.top
        for i in range(menu_size_y):
            for j in range(menu_size_x):
                if pos_x <= mouse_pos[0] - self.cell_size * self.width <= pos_x + self.cell_size\
                   and pos_y <= mouse_pos[1] <= pos_y + self.cell_size:
                    return pos_x, pos_y, j, i, 0
                pos_x += self.cell_size
            pos_x = self.left
            pos_y += self.cell_size

    def on_click(self, cell_coords):
        pos_x, pos_y, w, h, flag = cell_coords
        if self.flag:
            if self.effect != -1:
                if self.effect == 1 and start_field[h][w] == 0 and self.menu[self.id][1] > 0:
                    start_field[h][w] = 4
                    group = pygame.sprite.Group()
                    FieldImage(w * board.cell_size, h * board.cell_size, start_field[h][w], group)
                    group.draw(screen)
                    self.menu[self.id][1] -= 1

                    x = self.id % menu_size_x
                    y = int(self.id / menu_size_y)

                    group_menu = pygame.sprite.Group()
                    CellMenu(board.cell_size * (board_size_x + x), y * board.cell_size, group_menu)
                    group_menu.draw(screen)

                    group = pygame.sprite.Group()
                    MenuImage(board.cell_size * (board_size_x + x), y * board.cell_size, self.menu[self.id],
                              group)
                    group.draw(screen)
                    font = pygame.font.SysFont('arial', 11)
                    text = font.render(str(self.menu[self.id][1]), 1, (0, 0, 0))
                    screen.blit(text, (board.cell_size * (board_size_x + x) + 28 - 3 * len(str(self.menu[self.id][1])),
                                y * board.cell_size + 23))
                    if self.menu[self.id][1] == 0:
                        self.effect = -1
                        self.id = -1
            else:
                self.flag = not (start_field[h][w] == 10)
                self.x = w
                self.y = h
            return []
        else:
            self.effect = -1
            self.flag = True
            if start_field[h][w] != 0:
                return []
            return bfs(self.x, self.y, w, h)

    def build(self):
        for i in range(board_size_x):
            for j in range(board_size_y):
                Grass(i * board.cell_size, j * board.cell_size)

        all_grass.draw(screen)

        for i in range(board_size_y):
            for j in range(board_size_x):
                if start_field[i][j] != 0:
                    group = pygame.sprite.Group()
                    FieldImage(j * board.cell_size, i * board.cell_size, start_field[i][j], group)
                    group.draw(screen)

        for i in zombies:
            zombie = pygame.sprite.Group()
            Zombie(i[0] * board.cell_size, i[1] * board.cell_size, zombie, [0, 0], 0)
            zombie.draw(screen)
            start_field[i[1]][i[0]] = 10

    def build_menu(self, menu_arr=[]):
        self.menu = menu_arr
        for i in range(menu_size_x):
            for j in range(menu_size_y):
                CellMenu(board.cell_size * (board_size_x + i), j * board.cell_size)
        all_cell.draw(screen)

        for i in range(len(menu_arr)):
            group = pygame.sprite.Group()
            x = i % menu_size_x
            y = int(i / menu_size_y)
            MenuImage(board.cell_size * (board_size_x + x), y * board.cell_size, menu_arr[i], group)
            group.draw(screen)
            font = pygame.font.SysFont('arial', 11)
            text = font.render(str(menu_arr[i][1]), 1, (0, 0, 0))
            screen.blit(text, (board.cell_size * (board_size_x + x) + 28 - 3 * len(str(menu_arr[i][1])),
                               y * board.cell_size + 23))


board = Board(board_size_x, board_size_y)

board.build()
board.build_menu(menu_array)

running = True

x, y = 26, 18

arr = []
id = 1
t = time.time()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            arr = board.get_click(event.pos)
            # print(arr)
    t1 = time.time()
    if len(arr) != 0 and t1 - t > 0.5:
        grass = pygame.sprite.Group()
        Grass(arr[id - 1][1] * board.cell_size, arr[id - 1][0] * board.cell_size, grass)
        start_field[arr[id - 1][0]][arr[id - 1][1]] = 0
        grass.draw(screen)
        for i in range(4):
            grass = pygame.sprite.Group()
            Grass(arr[id][1] * board.cell_size, arr[id][0] * board.cell_size, grass)
            grass.draw(screen)

            zombie = pygame.sprite.Group()
            Zombie(arr[id][1] * board.cell_size, arr[id][0] * board.cell_size, zombie, [arr[id][1] - arr[id - 1][1],
                   arr[id][0] - arr[id - 1][0]], i)
            zombie.draw(screen)
            start_field[arr[id][0]][arr[id][1]] = 10

        id += 1
        t = time.time()
        if id == len(arr):
            id = 1
            arr = []
    pygame.display.flip()
