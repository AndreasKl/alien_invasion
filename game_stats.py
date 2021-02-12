from enum import Enum

from settings import Settings


class Mode(Enum):
    ACTIVE = 1,
    NOT_ACTIVE = 2,
    CHANGING_LEVEL = 3
    LEVEL_CHANGED = 4
    KILLED = 5
    GAME_OVER = 6
    MENU = 7


class GameStats:
    def __init__(self, ai_game) -> None:
        self.settings: Settings = ai_game.settings
        self.game_mode = Mode.NOT_ACTIVE
        self.ships_left = None
        self.reset_stats()

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit

    def set_game_mode(self, mode: Mode):
        self.game_mode = mode

    @property
    def is_active(self):
        return self.game_mode == Mode.ACTIVE

    @property
    def is_changing_level(self):
        return self.game_mode == Mode.CHANGING_LEVEL

    @property
    def is_level_changed(self):
        return self.game_mode == Mode.LEVEL_CHANGED

    @property
    def is_not_active(self):
        return self.game_mode == Mode.NOT_ACTIVE
