import pygame


class HUDisplay:

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.stats = ai_game.stats
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.width, self.height = 200, 50
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 28)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.topright = self.screen_rect.topright
        self.previous_point = self.stats.get_points()
        self._prep_msg(str(self.previous_point))

    def _prep_msg(self, msg: str):
        self.level_text_surface = self.font.render(msg, True, self.text_color)
        self.level_text_surface.set_alpha(187)
        self.level_text_surface_rect = self.level_text_surface.get_rect()
        self.level_text_surface_rect.center = self.rect.center

    def draw(self):
        if self.previous_point != self.stats.get_points():
            self.previous_point = self.stats.get_points()
            self._prep_msg(str(self.previous_point))

        self.screen.blit(self.level_text_surface, self.level_text_surface_rect)
