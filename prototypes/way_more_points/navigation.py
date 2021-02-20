import pygame as pg
from random import randint, uniform

vec = pg.math.Vector2

WIDTH = 800
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARKGRAY = (40, 40, 40)

# Mob properties
MOB_SIZE = 32
MAX_SPEED = 5
MAX_FORCE = 0.1
APPROACH_RADIUS = 120


class Mob(pg.sprite.Sprite):
    def __init__(self):
        self.groups = all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((MOB_SIZE, MOB_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = vec(30, HEIGHT - 50)
        self.vel = vec(0, 0)
        self.acc = vec(1, 1)
        self.rect.center = self.pos
        self.waypoint = self.pos
        self.waypoints = [
            vec(WIDTH, 530),
            vec(400, 430),
            vec(450, 250),
            vec(480, 230),
            vec(520, 330),
            vec(450, 495),
        ]

    def follow_waypoint(self):
        if self.waypoint.distance_to(self.pos) < 30:
            if not self.waypoints:
                self.vel = vec(0, 0)
                self.acc = vec(0, 0)
                return
            if self.waypoints:
                self.waypoint = self.waypoints.pop()
                print(f"Waypoint: {self.waypoint}")
        self.acc = (self.waypoint - self.pos).normalize() * 0.5

    def update(self):
        self.follow_waypoint()
        self.vel += self.acc
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT
        self.rect.center = self.pos

    def draw_vectors(self):
        scale = 25
        pg.draw.line(screen, GREEN, self.pos, (self.pos + self.vel * scale), 5)


pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

all_sprites = pg.sprite.Group()
Mob()
paused = False
show_vectors = False
running = True
while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_SPACE:
                paused = not paused
            if event.key == pg.K_v:
                show_vectors = not show_vectors
            if event.key == pg.K_m:
                Mob()

    if not paused:
        all_sprites.update()
    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    screen.fill(DARKGRAY)
    all_sprites.draw(screen)
    if show_vectors:
        for sprite in all_sprites:
            sprite.draw_vectors()
    pg.display.flip()
