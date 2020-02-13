import pygame
from images import Grass, FieldImage, MenuImage, CellMenu, load_image
from groups import zombies, all_grass, all_cell
from algorithm import bfs, check
from constants import screen, board_size_x, board_size_y, size, start_field, menu_size_x, menu_size_y, \
                      laboratory_array, objects_array, menu_array
from tools import Shovel, Poison
pygame.init()


class Back:
    def __init__(self):
        self.image = load_image("arrow1.png", -1)

    def use(self, w, h, board, menu):
        board.build_menu(menu_array)

    def show(self, w, h, cnt=0):
        group = pygame.sprite.Group()
        MenuImage(w, h, self.image, group)
        group.draw(screen)


class Zombie(pygame.sprite.Sprite):
    def __init__(self, coord, group):  # move = [y, x]
        super().__init__(group)
        self.clock = pygame.time.Clock()
        self.time = 0
        self.index = -1
        self.path = []
        self.time_buffer = 0
        self.speed = 0.01
        self.sprite_speed = 0.1
        self.directions = {(0, 1): 'down', (0, -1): 'up', (1, 0): 'right', (-1, 0): 'left'}
        self.image = load_image("zombie_down_0.png", -1)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coord[0], coord[1]
        self.directions1 = [[0, 0], [0, 1], [0, -1], [1, 0], [-1, 0]]

    def change_path(self, path):
        self.path = path
        self.time_buffer = 0
        self.time = 0
        self.index = 0
        self.clock.tick()

    def move(self):
        if self.index + 1 == len(self.path):
            return

        last_time = self.clock.tick() / 1000
        self.time_buffer += last_time
        direction = [self.path[self.index + 1][0] - self.path[self.index][0],
                     self.path[self.index + 1][1] - self.path[self.index][1]]
        for i in range(2):
            if direction[i]:
                direction[i] //= abs(direction[i])
        self.rect.x += direction[0] * round(self.time_buffer // self.speed)
        self.rect.y += direction[1] * round(self.time_buffer // self.speed)
        self.time_buffer %= self.speed
        self.time += last_time

        zombie_cell = (self.rect.x // board.cell_size, self.rect.y // board.cell_size)
        zombie_cell_x, zombie_cell_y = zombie_cell
        grass_to_draw = pygame.sprite.Group()
        for direct in self.directions1:
            x, y = zombie_cell_x + direct[0], zombie_cell_y + direct[1]
            if check(x, y) and start_field[y][x] == 0:
                Grass(x * board.cell_size, y * board.cell_size, grass_to_draw)
        grass_to_draw.draw(screen)

        b = int(self.time % (self.sprite_speed * (2 / self.sprite_speed)) // 0.5)
        direction_tuple = (direction[0], direction[1])
        a = self.directions[direction_tuple]
        self.image = load_image("zombie_" + a + "_" + str(b) + ".png", -1)
        zombies.draw(screen)

        if [zombie_cell_x, zombie_cell_y] == self.path[self.index + 1]:
            self.index += 1


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
        self.effect, self.id = None, -1
        self.menu = menu_array

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            # print(cell)
            if cell[2]:
                return self.on_click(cell)
            else:
                return self.action(cell)
        else:
            return []

    def action(self, cell_coords):
        global menu_array
        w, h, flag = cell_coords
        if self.effect is None and len(self.menu) > h * menu_size_x + w:
            if isinstance(self.menu[h * menu_size_x + w][0], Poison) or \
               isinstance(self.menu[h * menu_size_x + w][0], Back):
                menu_array = self.menu[w * menu_size_x + h][0].use(0, 0, board, menu_array)
            else:
                self.effect = self.menu[w * menu_size_x + h][0]
                self.id = w * menu_size_x + h
        else:
            self.effect = None
        return []

    def get_cell(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        flag = 1
        if mouse_x > board.cell_size * self.width:
            mouse_x -= board.cell_size * self.width
            flag = 0
        return mouse_y // board.cell_size, mouse_x // board.cell_size, flag

    def on_click(self, cell_coords):
        w, h, flag = cell_coords
        if self.effect is not None:
            self.menu = self.effect.use(w, h, self, self.menu)
        else:
            self.effect = None
            if self.board[w][h] == 5:
                self.build_menu(laboratory_array)
            else:
                start_cell = board.get_cell((zombie.rect.x, zombie.rect.y))
                finish_cell = board.get_cell(event.pos)
                path = bfs(start_cell, finish_cell)
                zombie.change_path(path)

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
            Zombie([i[0] * board.cell_size, i[1] * board.cell_size], zombies)
            zombie.draw(screen)
            start_field[i[1]][i[0]] = 10

    def build_menu(self, menu_arr=[]):
        self.menu = menu_arr
        for i in range(menu_size_x):
            for j in range(menu_size_y):
                CellMenu(board.cell_size * (board_size_x + i), j * board.cell_size)
        all_cell.draw(screen)

        for i in range(len(menu_arr)):
            x = i % menu_size_x
            y = int(i / menu_size_x)
            menu_arr[i][0].show(board.cell_size * (board_size_x + x), y * board.cell_size, menu_arr[i][1])


menu_array = [[Shovel(), 5], [Poison(1), -1], [Poison(23), -1], [Poison(17), -1], [Poison(18), -1], [Poison(19), -1],
              [Poison(20), -1], [Poison(21), -1], [Poison(24), -1], [Poison(8), -1], [Poison(9), -1]]
laboratory_array = [[Back(), 1], [Poison(1), 99], [Poison(23), 99], [Poison(17), 99], [Poison(18), 99], [Poison(19), 99],
                    [Poison(20), 99], [Poison(21), 99], [Poison(8), 99], [Poison(9), 99]]
for i in range(len(objects_array)):
    objects_array[i] = 1

board = Board(board_size_x, board_size_y)

board.build()
board.build_menu(menu_array)

running = True

x, y = 26, 18
zombie = Zombie([111, 74], zombies)
zombies.draw(screen)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    zombie.move()
    pygame.display.flip()

