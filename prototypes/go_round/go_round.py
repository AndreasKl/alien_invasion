import pygame

from prototypes.go_round.ship import AnotherShip

clock = pygame.time.Clock()


class GoRound:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((1024, 1024))
        pygame.display.set_caption("Ship go round")

        self.x, self.y = self.screen.get_rect().midbottom
        self.y -= 40
        self.all_sprites = pygame.sprite.Group(AnotherShip((self.x, self.y)))
        self.running = True

    def run_game(self):
        while self.running:
            clock.tick(60)
            self.screen.fill((0, 0, 0))

            self.all_sprites.update()
            self.all_sprites.draw(self.screen)
            self._check_events()

            pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.all_sprites.empty()
                self.all_sprites = pygame.sprite.Group(AnotherShip((self.x, self.y)))


if __name__ == '__main__':
    go_round = GoRound()
    go_round.run_game()
