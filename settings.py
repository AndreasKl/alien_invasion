class Settings:
    def __init__(self) -> None:
        self.frames_per_second = 60
        self.screen_width = 1200
        self.screen_height = 800
        self.screen_size = (self.screen_width, self.screen_height)
        self.light_grey = (230, 230, 230)
        self.ship_speed = 4.0
        self.bullet_speed = 5.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (230, 0, 0)
        self.bullets_allowed = 5
        self.alien_speed = 0.50
        self.alien_speed_increase = 0.4
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        self.ship_limit: int = 3
        self.level_teaser_duration_frames: int = 90
        self.level_count = 100
