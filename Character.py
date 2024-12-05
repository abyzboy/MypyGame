import pygame
from Engine import Vector, Transform, Controller


class Character:
    def __init__(self, screen, cords, speed):
        self.scale = 3
        self.screen = screen
        self.sprite = pygame.transform.scale(pygame.image.load('character.png').convert_alpha(), (
            pygame.image.load('character.png').convert_alpha().get_width() * self.scale,
            pygame.image.load('character.png').convert_alpha().get_height() * self.scale))
        self.controller = Controller()
        self.transform = Transform(cords)
        self.speed = speed

    def move(self):
        keys = pygame.key.get_pressed()
        x, y = 0, 0
        if keys[self.controller.right]:
            x = 1
        if keys[self.controller.left]:
            x = -1
        if keys[self.controller.down]:
            y = 1
        if keys[self.controller.up]:
            y = -1
        if x and y:
            vector = Vector((x, y))
            normalized_vector = vector.normalize()
            self.transform.xpos += normalized_vector.x * self.speed
            self.transform.ypos += normalized_vector.y * self.speed
        else:
            self.transform.xpos += x * self.speed
            self.transform.ypos += y * self.speed

    def update_frame(self):
        self.move()
        self.screen.blit(self.sprite, self.transform.positions())
