from Scripts.GameObjects.GameObject import GameObject
from Scripts.Engine import Vector, Collider
import pygame


class Enemy(GameObject):
    def __init__(self, cords, target, speed, screen, health=100):
        super().__init__(cords, 'enemy.png', scale=3, tag_collision='enemy')
        self.health = health
        self.can_walk = True
        self.speed = speed
        self.target = target
        self.screen = screen

        # collider
        self.collider = Collider((80, 80), self.transform, offset=(-20, -20))

    def update_collision(self, objects: list[GameObject]):
        for game_object in objects:
            if game_object.tag_collision == 'bullet':
                if self.collider.on_collider_stay(game_object.collider):
                    self.is_dead = True
                    game_object.is_dead = True

    def update_frame(self):
        vector = self.target.transform.vector
        if int(self.transform.dist(vector)) < 50:
            self.can_walk = False
        elif int(self.transform.dist(vector)) > 70:
            self.can_walk = True
        if self.can_walk:
            self.transform.goto(self.target.transform.vector, self.speed)
