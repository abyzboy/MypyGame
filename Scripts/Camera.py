from Scripts.Engine import Vector
import pygame

from Scripts.GameObjects.Character import Character
from Scripts.GameObjects.GameObject import GameObject


class Camera:
    def __init__(self, screen: pygame.display, character: Character, objects: list[GameObject] = []):
        self.objects = objects
        self.screen = screen
        self.offset = character.transform.vector - Vector((400, 300))
        self.character = character

    def draw_objects(self):
        self.offset = self.character.transform.vector - Vector((400, 300))
        self.character.draw_collision(self.offset)
        offset = self.character.transform.vector - self.offset
        self.screen.blit(self.character.sprite, offset.get_cords())
        for obj in self.objects:
            offset = obj.transform.vector - self.offset
            self.screen.blit(obj.sprite, offset.get_cords())

    def add_objects(self, *obj):
        for i in obj:
            self.objects.append(i)
