import random

import pygame as pg
from pygame.sprite import Sprite

IMAGES = [f"images/tunnel_{i}.png" for i in range(1, 6)]


class Tunnel(Sprite):
    def __init__(self) -> None:
        pg.sprite.Sprite.__init__(self)
        image = IMAGES[random.randint(0, 4)]
        self.image = pg.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = (1140, 690)

    def update(self):
        pass
