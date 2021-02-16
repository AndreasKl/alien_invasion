from typing import List

import pygame
import random


class Particles:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.typed_particles: List[CircleParticle] = []
        self.stopped = True

    def update(self, rect):
        if self.stopped:
            return
        self.typed_particles.append(
            CircleParticle(
                rect.x + 45 / 2,
                rect.y + 60,
                random.randint(0, 20) / 10.0 - 1,
                random.randint(0, 5) / 10.0 - 4,
                random.randint(1, 10),
                self.some_kind_of_red()
            ))

        particles_to_remove = []
        for particle in self.typed_particles:
            particle.move()
            pygame.draw.circle(self.screen, particle.color, particle.get_xy(), particle.get_size())
            if particle.get_size() <= 0:
                particles_to_remove.append(particle)
        for to_remove in particles_to_remove:
            self.typed_particles.remove(to_remove)

    def stop(self):
        self.typed_particles.clear()
        self.stopped = True

    def start(self):
        self.stopped = False

    @staticmethod
    def some_kind_of_red():
        return random.randint(139, 255), random.randint(0, 20), random.randint(0, 10)




class CircleParticle:

    def __init__(self, start_x: int, start_y: int, offset_x: float, offset_y: float, size: int, color: (int, int, int)):
        self.start_x = start_x
        self.start_y = start_y
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.size = size
        self.color = color

    def move(self):
        self.start_x += self.offset_x
        self.start_y -= self.offset_y
        self.size -= 0.2

    def get_xy(self):
        return [int(self.start_x), int(self.start_y)]

    def get_size(self):
        return self.size
