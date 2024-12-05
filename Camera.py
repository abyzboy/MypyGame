from Engine import Transform, Vector
import pygame
from GameObject import GameObject


class Camera:
    def __init__(self, screen: pygame.display, objects: list[GameObject] = []):
        self.objects = objects
        self.screen = screen
        self.offset = Vector((0, 0))

    def draw_objects(self):
        for obj in self.objects:
            offset = obj.transform.vector - self.offset
            self.screen.blit(obj.sprite, offset.get_cords())

    def add_objects(self, *obj):
        for i in obj:
            self.objects.append(i)
