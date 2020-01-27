import pygame
from constants import screen, board_size_x, board_size_y, size, start_field
from images import grass_image, tree_image, load_image, stone_image1, stone_image2, zombie_image
from groups import all_grass, all_trees, all_stone, zombies
from queue import Queue
import time


class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y, group=all_trees):
        super().__init__(group)
        self.image = tree_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.image = zombie_image
        self.turn = 0
        self.move = 0
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Stone(pygame.sprite.Sprite):
    def __init__(self, x, y, flag, group=all_stone):
        super().__init__(group)
        if flag:
            self.image = stone_image1
        else:
            self.image = stone_image2
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

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            print(cell[2], cell[3])
            return self.on_click(cell)
        else:
            print(None)
            return []

    def get_cell(self, mouse_pos):
        pos_x = self.left
        pos_y = self.top
        for i in range(self.height):
            for j in range(self.width):
                if pos_x <= mouse_pos[0] <= pos_x + self.cell_size and pos_y <= mouse_pos[1] <= pos_y + self.cell_size:
                    return pos_x, pos_y, j, i
                pos_x += self.cell_size
            pos_x = self.left
            pos_y += self.cell_size

    def on_click(self, cell_coords):
        pos_x, pos_y, w, h = cell_coords
        if self.flag:
            self.flag = not (start_field[h][w] == 10)
            self.x = w
            self.y = h
            return []
        else:
            self.flag = True
            if start_field[h][w] != 0:
                return []
            return bfs(self.x, self.y, w, h)


def check(x, y):
    t = (0 <= x < board_size_x and 0 <= y < board_size_y)
    return t


def bfs(start_x, start_y, end_x, end_y):
    q = Queue()
    q.put([start_y, start_x])
    step = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    used = [[False] * board_size_x for _ in range(board_size_y)]
    parent = [[[-1, -1]] * board_size_x for _ in range(board_size_y)]
    while not q.empty():
        a = q.get()
        if a == [end_y, end_x]:
            break
        for i in step:
            if check(a[1] + i[1], a[0] + i[0]) and start_field[a[0] + i[0]][a[1] + i[1]] == 0 \
                    and not used[a[0] + i[0]][a[1] + i[1]]:
                used[a[0] + i[0]][a[1] + i[1]] = True
                parent[a[0] + i[0]][a[1] + i[1]] = a
                q.put([a[0] + i[0], a[1] + i[1]])
    ans = [[end_y, end_x]]
    while parent[end_y][end_x] != [-1, -1]:
        ans.append(parent[end_y][end_x])
        x = parent[end_y][end_x][1]
        end_y = parent[end_y][end_x][0]
        end_x = x
    ans = list(reversed(ans))
    return ans


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
        elif start_field[i][j] == 2 or start_field[i][j] == 3:
            stone = pygame.sprite.Group()
            Stone(j * board.cell_size, i * board.cell_size, start_field[i][j] % 2, stone)
            stone.draw(screen)

for i in zombies:
    zombie = pygame.sprite.Group()
    Zombie(i[0] * board.cell_size, i[1] * board.cell_size, zombie)
    zombie.draw(screen)
    start_field[i[1]][i[0]] = 10

running = True

x, y = 26, 18

arr = []
id = 0
t = time.time()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            arr = board.get_click(event.pos)
            print(arr)
    t1 = time.time()
    if len(arr) != 0 and t1 - t > 0.5:

        zombie = pygame.sprite.Group()
        Zombie(arr[id][1] * board.cell_size, arr[id][0] * board.cell_size, zombie)
        zombie.draw(screen)
        start_field[arr[id][0]][arr[id][1]] = 10
        id += 1
        t = time.time()
        if id == len(arr):
            id = 0
            arr = []
    pygame.display.flip()
