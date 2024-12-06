from Scripts.Engine import Transform
import pygame


class GameObject:
    def __init__(self, cords, image_path, scale=1, tag_collision = 'default'):
        self.scale = scale
        self.transform = Transform(cords)
        self.sprite = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (
            pygame.image.load(image_path).convert_alpha().get_width() * self.scale,
            pygame.image.load(image_path).convert_alpha().get_height() * self.scale))
        self.tag_collision = tag_collision

    def update_frame(self):
        pass
