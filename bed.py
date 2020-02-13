import pygame
from images import load_image
from constants import ripe_time
from images import plants


class Bed(pygame.sprite.Sprite):
    def __init__(self, name, coord, group):
        super().__init__(group)
        self.x, self.y = coord
        self.clock = pygame.time.Clock()
        self.time = 0
        self.image = load_image("bed.jpg")
        self.name = name
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coord[0], coord[1]

    def update(self):
        if self.time < 0:
            self.image = plants[self.name]
            return
        self.time += self.clock.tick()
        if self.time >= ripe_time:
            self.time = -1
