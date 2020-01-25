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
zombie_image = load_image("zombie2.png", -1)
