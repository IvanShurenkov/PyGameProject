import pygame
from constants import start_field, menu_size_y, menu_size_x, board_size_x, board_size_y, screen, objects_array,\
    poison_r, menu_array
from groups import all_beds
from images import FieldImage, CellMenu, MenuImage, shovel_image, poison, plants
from bed import Bed
pygame.init()


class Shovel:
    def __init__(self):
        self.image = shovel_image
        self.id = -1

    def use(self, w, h, board, menu):
        if start_field[w][h] == 0 and menu[board.id][1] > 0:
            start_field[w][h] = 4
            group = pygame.sprite.Group()
            FieldImage(h * board.cell_size, w * board.cell_size, start_field[w][h], group)
            group.draw(screen)
            menu[board.id][1] -= 1

            x = board.id % menu_size_x
            y = int(board.id / menu_size_y)

            group_menu = pygame.sprite.Group()
            CellMenu(board.cell_size * (board_size_x + x), y * board.cell_size, group_menu)
            group_menu.draw(screen)

            group = pygame.sprite.Group()
            MenuImage(board.cell_size * (board_size_x + x), y * board.cell_size, self.image,
                      group)
            group.draw(screen)
            font = pygame.font.SysFont('arial', 11)
            text = font.render(str(menu[board.id][1]), 1, (0, 0, 0))
            screen.blit(text, (board.cell_size * (board_size_x + x) + 28 - 3 * len(str(menu[board.id][1])),
                        y * board.cell_size + 23))
            return menu

    def show(self, w, h, cnt=0):
        group = pygame.sprite.Group()
        MenuImage(w, h, self.image, group)
        group.draw(screen)
        font = pygame.font.SysFont('arial', 11)
        text = font.render(str(cnt), 1, (0, 0, 0))
        screen.blit(text, (w + 28 - 3 * len(str(cnt)), h + 23))


class Poison:
    def __init__(self, id):
        self.image = poison[id]
        self.id = id

    def use(self, w, h, board, menu):
        flag = True
        for i in poison_r[self.id]:
            if objects_array[i[0]] < i[1]:
                flag = False
        if flag:
            for i in poison_r[self.id]:
                objects_array[i[0]] -= i[1]
            objects_array[self.id] += 1
            flag = False
            for i in range(len(menu)):
                if menu[i][0].id == self.id:
                    flag = True
                    break
            if not flag:
                menu.append([self, 1])
        return menu

    def show(self, w, h, cnt=-1):
        if cnt == -1:
            cnt = objects_array[self.id]
        group = pygame.sprite.Group()
        MenuImage(w, h, self.image, group)
        group.draw(screen)
        font = pygame.font.SysFont('arial', 11)
        text = font.render(str(cnt), 1, (120, 120, 120))
        screen.blit(text, (w + 28 - 3 * len(str(cnt)), h + 23))


class Mak:
    def __init__(self):
        self.image = plants['mak']

    def use(self, w, h, board, menu):
        if start_field[w][h] == 4 and menu[board.id][1] > 0:
            Bed('mak', (w, h), all_beds)

    def show(self, w, h, cnt=0):
        group = pygame.sprite.Group()
        MenuImage(w, h, self.image, group)
        group.draw(screen)
        font = pygame.font.SysFont('arial', 11)
        text = font.render(str(cnt), 1, (0, 0, 0))
        screen.blit(text, (w + 28 - 3 * len(str(cnt)), h + 23))
