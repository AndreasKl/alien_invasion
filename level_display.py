import pygame

from game_stats import Mode


class LevelDisplay:

    def __init__(self, ai_game, level_names):
        self.ai_game = ai_game
        self.stats = ai_game.stats
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.width, self.height = 200, 50
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.default_duration = ai_game.settings.level_teaser_duration_frames
        self.duration = self.default_duration
        self.default_level_names = level_names
        self.prepare_level_counter()

    def prepare_level_counter(self):
        self.level_names = self.default_level_names[:]
        self.update_level()

    def update_level(self):
        self.current_level = self.level_names.pop()
        self._prep_msg(f"Level {self.current_level}")

    def update(self):
        if self.duration > 0:
            self.duration -= 1
            return

        self.update_level()
        # Reset duration
        self.duration = self.default_duration
        self.stats.set_game_mode(Mode.LEVEL_CHANGED)

    def _prep_msg(self, msg):
        self.level_text_surface = self.font.render(msg, True, self.text_color)
        self.level_text_surface.set_alpha(127)
        self.level_text_surface_rect = self.level_text_surface.get_rect()
        self.level_text_surface_rect.center = self.rect.center

    def draw(self):
        self.screen.blit(self.level_text_surface, self.level_text_surface_rect)

    def reset(self):
        self.prepare_level_counter()
