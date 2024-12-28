import pygame
from pygame import Surface

FPS = 60


class Vector:
    def __init__(self, cord):
        self.x = cord[0]
        self.y = cord[1]

    def len_vector(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def normalize(self):
        return Vector((self.x / self.len_vector(), self.y / self.len_vector()))

    def get_cords(self):
        return self.x, self.y

    def __add__(self, other):
        if type(other) == Vector:
            return Vector((self.x + other.x, self.y + other.y))

    def __sub__(self, other):
        if type(other) == Vector:
            return Vector((self.x - other.x, self.y - other.y))

    def __le__(self, other):
        if self.x <= other.x and self.y <= other.y:
            return True
        else:
            return False

    def __ge__(self, other):
        if self.x >= other.x and self.y >= other.y:
            return True
        else:
            return False


class Transform:
    def __init__(self, cords=(0, 0)):
        self.vector = Vector(cords)

    def dist(self, other):
        if isinstance(other, Vector):
            return (other - self.vector).len_vector()

    def positions(self):
        return self.vector.get_cords()

    def goto(self, other, speed=1):
        vector = other - self.vector
        self.vector.x += vector.normalize().x * speed
        self.vector.y += vector.normalize().y * speed


class Collider:
    def __init__(self, cord, transform, offset=(0, 0), tag='defualt'):
        self.transform = transform
        self.tag = tag
        self.offset = Vector(offset)
        self.cord = Vector(cord)
        self.surface = Surface(cord)
        self.surface.set_alpha(50)
        self.surface.fill((0, 0, 0))
        self.surface.set_alpha(50)

    def on_collider_stay(self, other):
        if isinstance(other, Collider):
            my_vector = self.transform.vector + self.offset
            other_vector = other.transform.vector + other.offset
            if ((
                        my_vector.x <= other_vector.x <= my_vector.x + self.cord.x) and (
                        my_vector.y <= other_vector.y <= my_vector.y + self.cord.y
                )) or ((
                               other_vector.x <= my_vector.x <= other_vector.x + other.cord.x) and (
                               other_vector.y <= my_vector.y <= other_vector.y + other.cord.y)
            ):
                return True

    def draw_collider(self, screen, offset):
        screen.blit(self.surface, (self.transform.vector - offset + self.offset).get_cords())


class Controller:
    up = pygame.K_w
    down = pygame.K_s
    right = pygame.K_d
    left = pygame.K_a


def draw_text_with_outline(surface, text, font, position, text_color, outline_color, outline_thickness=1):
    # Рисуем обводку

    for dx in range(-outline_thickness, outline_thickness + 1):

        for dy in range(-outline_thickness, outline_thickness + 1):

            if abs(dx) + abs(dy) > outline_thickness:
                continue

            outline_position = (position[0] + dx, position[1] + dy)

            surface.blit(font.render(text, True, outline_color), outline_position)

    # Рисуем основной текст

    surface.blit(font.render(text, True, text_color), position)

    return font.render(text, True, text_color).get_height()


def draw_multiline_text(surface, text, font, position, text_color, outline_color=(0, 0, 0), outline_thickness=0):
    lines = text.split('\n')  # Разделяем текст на строки

    y_offset = 0  # Смещение по вертикали

    for line in lines:
        y_offset += draw_text_with_outline(surface, line, font, (position[0], position[1] + y_offset), text_color,
                                           outline_color, outline_thickness)
