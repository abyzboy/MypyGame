import pygame
from Scripts.Engine import Vector, Controller, Collider
from Scripts.GameObjects.GameObject import GameObject
from Scripts.bullet import Bullet


class Character(GameObject):
    def __init__(self, cords, speed, screen):
        super().__init__(cords, 'character.png', scale=3, tag_collision='character')
        self.controller = Controller()
        self.screen = screen
        self.health = 100
        self.speed = speed
        self.collider_area_attack = Collider((500, 500), self.transform, offset=(-225, -225))
        self.collider_character = Collider((80, 80), self.transform, offset=(-20, -20))
        self.targets = []
        self.camera = None

    def update_collision(self, objects: list[GameObject]):
        self.targets = []
        for game_object in objects:
            if game_object.tag_collision == 'enemy':
                # if self.collider_area_attack.on_collider_stay(game_object.collider):
                # self.targets.append(game_object)
                if self.collider_character.on_collider_stay(game_object.collider):
                    game_object.attack(self)
                    print(self.health)

    def draw_collision(self, offset):
        pygame.draw.rect(self.surface, 'white', self.collision_fire)
        self.screen.blit(self.surface, (self.transform.vector - offset - Vector((300, 300))).get_cords())

    def create_bullet(self):
        if self.targets:
            bullet = Bullet(self.transform.vector.get_cords(), self.targets[0])
            self.camera.add_objects(bullet)

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
            self.transform.vector += Vector((normalized_vector.x * self.speed, normalized_vector.y * self.speed))
        else:
            self.transform.vector += Vector((vector.x * self.speed, vector.y * self.speed))

    def update_frame(self):
        self.move()
