import os, pygame


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
