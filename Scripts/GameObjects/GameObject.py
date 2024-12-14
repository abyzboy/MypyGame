from Scripts.Engine import Transform
import pygame


class GameObject:
    def __init__(self, cords, image_path, scale=1, tag_collision='default'):
        self.image_path = image_path
        self.scale = scale
        self.transform = Transform(cords)
        self.sprite = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (
            pygame.image.load(image_path).convert_alpha().get_width() * self.scale,
            pygame.image.load(image_path).convert_alpha().get_height() * self.scale))
        self.tag_collision = tag_collision
        self.is_dead = False

    def update_frame(self):
        pass

    def update_collision(self, objects):
        pass

    def __str__(self):
        return self.tag_collision
