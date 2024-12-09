import pygame

from Scripts.Engine import Vector, Controller
from Scripts.GameObjects.GameObject import GameObject


class Character(GameObject):
    def __init__(self, cords, speed, screen):
        super().__init__(cords, 'character.png', scale=3)
        self.controller = Controller()
        self.screen = screen
        self.speed = speed
        self.collision_fire = ((0, 0), (400, 400))
        self.surface = pygame.Surface((400, 400), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))
        self.surface.set_alpha(50)

    def update_collision(self, objects: list[GameObject]):
        for game_object in objects:
            if game_object.tag_collision == 'enemy':
                collider_vectors = (Vector(self.collision_fire[0]) + self.transform.vector - Vector((175, 175)),
                                    Vector(self.collision_fire[1]) + self.transform.vector - Vector((175, 175)))
                if (collider_vectors[0] <= game_object.transform.vector) and (game_object.transform.vector <=
                                                                              collider_vectors[1]):
                    print('detected')

    def draw_collision(self, offset):
        x, y = self.sprite.get_size()
        pygame.draw.rect(self.surface, 'white', self.collision_fire)
        self.screen.blit(self.surface, (self.transform.vector - offset - Vector((175, 175))).get_cords())

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
