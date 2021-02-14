from enum import Enum

from settings import Settings


class Mode(Enum):
    ACTIVE = (1,)
    NOT_ACTIVE = (2,)
    CHANGING_LEVEL = 3
    LEVEL_CHANGED = 4
    KILLED = 5
    GAME_OVER = 6
    MENU = 7
    PAUSE = 8


class GameStats:
    def __init__(self, ai_game) -> None:
        self.settings: Settings = ai_game.settings
        self.game_mode = Mode.NOT_ACTIVE
        self.ships_left = None
        self.points = 0
        self.reset_stats()

    def reset_stats(self) -> None:
        self.ships_left = self.settings.ship_limit
        self.points = 0

    def set_game_mode(self, mode: Mode) -> None:
        self.game_mode = mode

    @property
    def is_active(self) -> None:
        return self.game_mode == Mode.ACTIVE

    @property
    def is_changing_level(self) -> None:
        return self.game_mode == Mode.CHANGING_LEVEL

    @property
    def is_level_changed(self) -> None:
        return self.game_mode == Mode.LEVEL_CHANGED

    @property
    def is_not_active(self) -> None:
        return self.game_mode == Mode.NOT_ACTIVE

    def add_points(self, points: int) -> None:
        self.points += points
        print(f"More points [{self.points}].")
