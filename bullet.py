import pygame
from pygame.sprite import Sprite, AbstractGroup


class Bullet(Sprite):
    def __init__(self, ai_game, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = ai_game.settings.bullet_color
        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height
        )
        self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

        pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/laser.ogg'))

    def update(self, *args, **kwargs) -> None:
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)