from typing import List

import pygame
import random

clock = pygame.time.Clock()


class Particles:
    def __init__(self) -> None:
        pygame.init()

        self.running = True
        self.screen = pygame.display.set_mode((1024, 1024))
        self.typed_particles: List[CircleParticle] = []
        pygame.display.set_caption("Particles everywhere")

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def run_game(self) -> None:

        while self.running:
            clock.tick(60)
            print(str(int(clock.get_fps())))
            self.screen.fill((0, 0, 0))
            self._start_particles()

            self._check_events()
            pygame.display.update()

    def _start_particles(self):
        self.typed_particles.append(
            CircleParticle(
                int((1024 / 2) + 20),
                400,
                random.randint(0, 20) / 10.0 - 1,
                random.randint(0, 5) / 10.0 - 4,
                random.randint(2, 20),
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

    def some_kind_of_red(self):
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


if __name__ == '__main__':
    particles = Particles()
    particles.run_game()
