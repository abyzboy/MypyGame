import pygame

from Scripts.Engine import Vector
from Scripts.GameObjects import Bullet
from Scripts.GameObjects import Character
from Scripts.GameObjects import Enemy
from Scripts.GameObjects import GameObject


class Camera:
    def __init__(self, screen: pygame.display, character: Character, objects: list[GameObject] = []):
        self.objects = objects
        self.screen = screen
        self.offset = character.transform.vector - Vector((400, 300))
        self.character = character

    def draw_objects(self):
        self.offset = self.character.transform.vector - Vector((400, 300))
        # self.character.collider_area_attack.draw_collider(self.screen, self.offset)
        for i in range(len(self.objects[0:])):
            if isinstance(self.objects[i], Enemy):
                # self.objects[i].collider.draw_collider(self.screen, self.offset)
                if self.objects[i].is_dead:
                    self.objects.pop(i)
                    break
            if isinstance(self.objects[i], Bullet):
                if self.objects[i].is_dead:
                    self.objects.pop(i)
                    break
            offset = self.objects[i].transform.vector - self.offset
            self.screen.blit(self.objects[i].sprite, offset.get_cords())
        offset = self.character.transform.vector - self.offset
        self.screen.blit(self.character.sprite, offset.get_cords())

    def add_objects(self, *obj):
        for i in obj:
            self.objects.append(i)

    def is_enemies_on_map(self):
        for obj in self.objects:
            if obj.tag_collision == 'enemy':
                return True
        return False
