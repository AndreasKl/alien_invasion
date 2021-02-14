import pygame

from game_stats import GameStats


class PauseDisplay:

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.stats: GameStats = ai_game.stats
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.width, self.height = 200, 50
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 54)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self._prep_msg("Waiting for action!")

    def _prep_msg(self, msg):
        self.level_text_surface = self.font.render(msg, True, self.text_color)
        self.level_text_surface.set_alpha(255)
        self.level_text_surface_rect = self.level_text_surface.get_rect()
        self.level_text_surface_rect.center = self.rect.center

    def draw(self):
        if self.stats.is_paused:
            self.screen.blit(self.level_text_surface, self.level_text_surface_rect)
