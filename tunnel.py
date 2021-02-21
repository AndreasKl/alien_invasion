import pygame as pg
from pygame.sprite import Sprite


class Tunnel(Sprite):
    def __init__(self) -> None:
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load("images/tunnel.png")
        self.rect = self.image.get_rect()
        self.rect.center = (1150, 700)

    def update(self):
        pass
