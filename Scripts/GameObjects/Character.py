import pygame
from Scripts.Engine import Vector, Controller
from Scripts.GameObjects.GameObject import GameObject


class Character(GameObject):
    def __init__(self, cords, speed, screen, camera):
        super().__init__(cords, '../../character.png', scale=3)
        self.controller = Controller()
        self.screen = screen
        self.speed = speed
        self.camera = camera

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
        vector = Vector((x, y))
        if x and y:
            normalized_vector = vector.normalize()
            self.camera.offset += Vector((normalized_vector.x * self.speed, normalized_vector.y * self.speed))
        else:
            self.camera.offset += Vector((x * self.speed, y * self.speed))

    def update_frame(self):
        self.move()
        self.screen.blit(self.sprite, self.transform.positions())
