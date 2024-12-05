import pygame
from Engine import Transform, Vector


class Enemy:
    def __init__(self, screen, cords, target, speed):
        self.screen = screen
        self.transform = Transform(cords)
        self.can_walk = True
        self.speed = speed
        self.target = target
        self.surface = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))
        pygame.draw.circle(self.surface, 'red', (25, 25), 25)

    def update_frame(self):
        if int(self.transform.dist(self.target.transform)) < 50:
            self.can_walk = False
        if int(self.transform.dist(self.target.transform)) > 70:
            self.can_walk = True
        if self.can_walk:
            self.transform.goto(self.target.transform, self.speed)
        self.screen.blit(self.surface, self.transform.positions())
