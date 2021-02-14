import pygame

from ship import Ship


class HUDisplay:

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.stats = ai_game.stats
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.width, self.height = 120, 28
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 28)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.topright = self.screen_rect.topright

        self.previous_point = self.stats.get_points()
        self.previous_ships_left = self.stats.get_ships_left()
        self.scaled_ship_image = self._create_scaled_ship_image(ai_game)
        self._prep_msg(str(self.previous_point))
        self._prep_ships(self.previous_ships_left)

    @staticmethod
    def _create_scaled_ship_image(ai_game):
        ship = Ship(ai_game)
        return pygame.transform.scale(ship.image, (27, 36))  # 9 (45) / 12 (60)

    def _prep_msg(self, msg: str):
        self.level_text_surface = self.font.render(msg, True, self.text_color)
        self.level_text_surface.set_alpha(222)
        self.level_text_surface_rect = self.level_text_surface.get_rect()
        self.level_text_surface_rect.right = self.rect.right - 5
        self.level_text_surface_rect.top = self.rect.top + 5

    def _prep_ships(self, ships_left):
        ships = []
        for i in range(0, ships_left):
            ship = Ship(self.ai_game)
            ship.image = self.scaled_ship_image
            x, y = self.screen_rect.topleft
            ship.rect.x = x + (30 * i)
            ship.rect.y = y
            ships.append(ship)
        self.ships = ships

    def draw(self):
        if self.previous_point != self.stats.get_points():
            self.previous_point = self.stats.get_points()
            self._prep_msg(str(self.previous_point))

        if self.previous_ships_left != self.stats.get_ships_left():
            self.previous_ships_left = self.stats.get_ships_left()
            self._prep_ships(self.previous_ships_left)

        self.screen.blit(self.level_text_surface, self.level_text_surface_rect)
        for i, ship in enumerate(self.ships):
            ship.blitme()
