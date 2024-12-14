from Scripts.Engine import *
from Scripts.GameObjects.GameObject import GameObject
import time


class Bullet(GameObject):
    def __init__(self, cords, target, damage=50):
        super().__init__(cords, image_path='bullet.png', scale=2, tag_collision='bullet')
        self.sprite = pygame.transform.rotate(pygame.image.load(self.image_path).convert_alpha(), 0)
        self.target = target
        self.is_dead = False
        self.first_time = time.time()
        self.collider = Collider((1, 1), self.transform)
        self.damage = damage

    def update_frame(self):
        self.transform.goto(self.target.transform.vector, 10)
