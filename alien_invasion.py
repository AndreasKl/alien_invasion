import math
import random
import sys

import pygame

from alien import Alien
from background import Background
from bullet import Bullet
from button import Button
from coin import Coin
from game_stats import GameStats, Mode
from hu_display import HUDisplay
from level_display import LevelDisplay
from pause_display import PauseDisplay
from settings import Settings
from ship import Ship

back_ground = Background("images/background.jpg", [0, 0])
clock = pygame.time.Clock()


class AlienInvasion:
    def __init__(self) -> None:
        self.settings = Settings()

        pygame.init()

        pygame.mixer.init()
        pygame.mixer.music.load("sounds/tune.ogg")
        pygame.mixer.music.set_volume(0.75)
        pygame.mixer.music.play(-1)
        pygame.event.wait()

        self.screen = pygame.display.set_mode(self.settings.screen_size)
        pygame.display.set_caption("Theos Alien Invasion")

        self.stats = GameStats(self)
        self.level_display = LevelDisplay(self, list(range(self.settings.level_count, -1, -1)))
        self.score_display = HUDisplay(self)
        self.pause_display = PauseDisplay(self)
        self.play_button = Button(self, "Play!")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.flight_objects = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self) -> None:
        while True:
            clock.tick(self.settings.frames_per_second)
            self._check_events()

            if self.stats.is_changing_level:
                self.level_display.update()

            if self.stats.is_level_changed:
                self._set_stage()
                self.stats.set_game_mode(Mode.ACTIVE)

            if self.stats.is_active:
                self.ship.update()
                self._update_bullets()
                self._change_level()
                self._update_aliens()

            self._update_screen()

    def _update_screen(self):
        self.screen.fill(self.settings.light_grey)
        self.screen.blit(back_ground.image, back_ground.rect)

        self.ship.blitme()
        for bullet in self.bullets:
            bullet.draw_bullet()
        self.flight_objects.draw(self.screen)

        if self.stats.is_not_active:
            self.play_button.draw()
            # FIXME: Do not reset on every render.
            self.level_display.reset()

        if self.stats.is_changing_level:
            self.level_display.draw()

        self.score_display.draw()
        self.pause_display.draw()

        pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            if event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        if event.key == pygame.K_SPACE:
            self._fire_bullet()
            self._start_game()
        if event.key == pygame.K_p:
            self._pause_game()
        if event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.stats.is_not_active:
            self._start_game()

    def _update_bullets(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.flight_objects, True, True)
        if collisions:
            for key, value in collisions.items():
                if type(key) is Coin:
                    self.stats.add_points(value.get_points())
                candidate = value[-1]
                if type(candidate) is Coin:
                    self.stats.add_points(candidate.get_points())

        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _change_level(self):
        if self._all_enemies_killed():
            self.bullets.empty()
            self.flight_objects.empty()
            self.ship.center_ship()
            self.stats.set_game_mode(Mode.CHANGING_LEVEL)

    def _all_enemies_killed(self):
        return not list(filter(lambda fo: fo.is_enemy(), self.flight_objects))

    def _fire_bullet(self):
        if not self.stats.is_active:
            return
        if len(self.bullets) >= self.settings.bullets_allowed:
            return
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _create_flight_object(self, row_number: int, alien_number: int):
        flight_object = self._provide_flight_object()
        fo_width, fo_height = flight_object.rect.size
        flight_object.x = fo_width + 1.4 * fo_width * alien_number
        flight_object.rect.y = fo_height + 2 * fo_height * row_number
        flight_object.rect.x = flight_object.x
        self.flight_objects.add(flight_object)

    def _provide_flight_object(self):
        seed = ["alien", "coin"]
        selected_type = random.choice(seed)
        if selected_type == "alien":
            flight_object = Alien(self)
        if selected_type == "coin":
            flight_object = Coin(self)
        return flight_object

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (1.4 * alien_width)
        number_of_aliens_x = math.floor(available_space_x / (1.4 * alien_width))

        _, ship_height = self.ship.rect.size
        available_space_y = self.settings.screen_height - ship_height * 3
        number_of_rows = math.floor(available_space_y / (2 * alien_height))

        for row_number in range(number_of_rows):
            for alien_number in range(number_of_aliens_x):
                self._create_flight_object(row_number, alien_number)

    def _check_fleet_edges(self):
        for alien in self.flight_objects.sprites():
            if alien.check_edges():
                return True
        return False

    def _change_fleet_direction(self, change_direction):
        for alien in self.flight_objects.sprites():
            if change_direction:
                alien.change_direction()
                alien.rect.y += self.settings.fleet_drop_speed

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.flight_objects.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_aliens(self):
        change_direction = self._check_fleet_edges()
        self._change_fleet_direction(change_direction=change_direction)
        self.flight_objects.update()
        if pygame.sprite.spritecollideany(self.ship, self.flight_objects):
            self._ship_hit()
        self._check_aliens_bottom()

    def _ship_hit(self):
        # Draw an explosion animation
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/explosion.ogg'))
        if self.stats.ships_left > 1:
            self.stats.ships_left -= 1
            # self.flight_objects.empty()
            self.bullets.empty()
            # self._create_fleet()
            self.ship.center_ship()
        else:
            self.stats.set_game_mode(Mode.NOT_ACTIVE)
            pygame.mouse.set_visible(True)

    def _set_stage(self):
        self.bullets.empty()
        self._create_fleet()
        self.ship.center_ship()

    def _start_game(self):
        if not self.stats.is_not_active:
            return
        pygame.mouse.set_visible(False)
        self.stats.set_game_mode(Mode.CHANGING_LEVEL)
        self.stats.reset_stats()
        self.flight_objects.empty()
        self.bullets.empty()
        self.ship.center_ship()

    def _pause_game(self):
        if self.stats.is_active:
            self.stats.set_game_mode(Mode.PAUSE)
            return

        if self.stats.is_paused:
            self.stats.set_game_mode(Mode.ACTIVE)
            return


ai = AlienInvasion()
ai.run_game()
