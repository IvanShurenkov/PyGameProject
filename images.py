import os
import pygame
from groups import all_cell, all_grass
from constants import screen
pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


grass_image = load_image("grass.jpg")
tree_image = load_image("tree.jpg", -1)
stone_image1 = load_image("stone_1.png", -1)
stone_image2 = load_image("stone_2.png", -1)
zombie_down = [load_image("zombie_down_0.png", -1), load_image("zombie_down_1.png", -1),
               load_image("zombie_down_2.png", -1), load_image("zombie_down_3.png", -1)]
zombie_left = [load_image("zombie_left_0.png", -1), load_image("zombie_left_1.png", -1),
               load_image("zombie_left_2.png", -1), load_image("zombie_left_3.png", -1)]
zombie_right = [load_image("zombie_right_0.png", -1), load_image("zombie_right_1.png", -1),
                load_image("zombie_right_2.png", -1), load_image("zombie_right_3.png", -1)]
zombie_up = [load_image("zombie_up_0.png", -1), load_image("zombie_up_1.png", -1),
             load_image("zombie_up_2.png", -1), load_image("zombie_up_3.png", -1)]
bed_image = load_image("bed.jpg")
cell_image = load_image("cell.png")
laboratory_image = load_image("laboratory.png", -1)
shovel_image = load_image("shovel.png", -1)
poison = {1: load_image("lhl.png", -1), 23: load_image("ulb.png", -1), 17: load_image("chocolate.png", -1),
          18: load_image("optimism.png"), 19: load_image("totalitarianism.png", -1), 20: load_image("necrophilia.png"),
          21: load_image("resusc.jpg"), 24: load_image("money.png", -1), 8: load_image("rock.png", -1),
          9: load_image("wood.png", -1)}
plants = {'mak': load_image('mak.png', -1), 'klever': load_image('klever.png', -1),
          'mouses': load_image('mouses.png', -1),
          'plodi': load_image('plodi.jpg')}


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
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class CellMenu(pygame.sprite.Sprite):
    def __init__(self, x, y, group=all_cell):
        super().__init__(group)
        self.image = cell_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Grass(pygame.sprite.Sprite):
    def __init__(self, x, y, group=all_grass):
        super().__init__(group)
        self.image = grass_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
