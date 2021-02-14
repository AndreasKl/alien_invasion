import pygame, sys, random

clock = pygame.time.Clock()


class Particles:
    def __init__(self) -> None:
        pygame.init()

        self.running = True
        self.screen = pygame.display.set_mode((1024, 1024))
        self.particles = []
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
        self.particles.append(
            [
                [
                    (1024 / 2) + 20,
                    400
                ],  # Start location
                [
                    random.randint(-20, 20) / 10,
                    -2
                ],  # offsets
                random.randint(2, 6),  # Size
                (random.randint(230, 255), random.randint(0, 150), random.randint(0, 10))  # Color
            ]
        )
        self.particles.append(
            [
                [
                    (1024 / 2) - 20,
                    400
                ],  # Start location
                [
                    random.randint(-20, 20) / 10,
                    -2
                ],  # offsets
                random.randint(2, 6),  # Size
                (random.randint(230, 255), random.randint(0, 150), random.randint(0, 10))  # Color
            ]
        )
        particles_to_remove = []
        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] -= particle[1][1]
            particle[2] -= 0.1
            color = particle[3]
            pygame.draw.circle(self.screen, color, [int(particle[0][0]), int(particle[0][1])], particle[2])
            if particle[2] <= 0:
                particles_to_remove.append(particle)
        for to_remove in particles_to_remove:
            self.particles.remove(to_remove)


if __name__ == '__main__':
    particles = Particles()
    particles.run_game()
