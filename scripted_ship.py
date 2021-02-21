import math

import pygame as pg

vec = pg.math.Vector2

SCRIPT = [
    "END",
    vec(1320, 700),
    vec(1200, 700),
    vec(1080, 700),
    vec(960, 700),
    vec(840, 700),
    vec(720, 700),
    vec(600, 700),
    # Looping End
    vec(520, 600),
    vec(500, 550),
    vec(480, 500),
    vec(480, 400),
    vec(520, 300),
    vec(560, 250),
    vec(600, 200),
    vec(640, 250),
    vec(680, 300),
    vec(720, 400),
    vec(720, 500),
    vec(700, 650),
    vec(680, 600),
    # Looping Begin
    vec(600, 700),
    vec(480, 700),
    vec(360, 700),
    vec(240, 700),
    vec(120, 700),
    vec(1, 700),
]


class ScriptedShip(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.rotozoom(pg.image.load("images/ship.png"), 270, 1)
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self._rotate(270)
        self.pos = vec(0, 700)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.waypoint = self.pos
        self.waypoints = SCRIPT[:]

    def follow_waypoint(self):
        if self.waypoint == "END":
            self.vel = vec(0, 0)
            self.acc = vec(0, 0)
            return
        if self.waypoint.distance_to(self.pos) < 60:
            if self.waypoints:
                self.waypoint = self.waypoints.pop()
            if self.waypoint == "END":
                return
            self.acc = (self.waypoint - self.pos).normalize() * 0.5

    def has_finished(self):
        return self.waypoint == "END"

    def update(self):
        self.follow_waypoint()
        self.vel += self.acc
        if self.vel.length() > 5.3:
            self.vel.scale_to_length(5.3)

        angle = (math.atan2(self.vel.y, self.vel.x) * 180 / math.pi) * -1
        self._rotate(angle)
        self.pos += self.vel
        self.rect.center = self.pos

    def _rotate(self, angle):
        self.image = pg.transform.rotozoom(self.orig_image, angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
