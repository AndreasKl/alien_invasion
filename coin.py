from settings import Settings
import pygame
import random

from pygame.sprite import Sprite, AbstractGroup


class Coin(Sprite):

    coin_points =  list(range(1, 7))

    def __init__(self, ai_game, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.screen = ai_game.screen
        self.settings: Settings = ai_game.settings

        self.point = random.choice(self.coin_points)
        image = "images/coin_{}.png".format(self.point)
        print(image)

        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.width
        self.fleet_direction = self.settings.fleet_direction
        self.x = float(self.rect.x)

    def change_direction(self):
        self.fleet_direction *= -1

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        return False

    def update(self, *args, **kwargs) -> None:
        self.x += self.settings.alien_speed * self.fleet_direction
        self.rect.x = self.x
        return super().update(*args, **kwargs)

    def get_points(self) -> int:
        return self.point
