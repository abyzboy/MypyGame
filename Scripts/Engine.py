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

    def dist(self, other):
        if isinstance(other, Vector):
            return (other - self).len_vector()

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector((self.x + other.x, self.y + other.y))

    def __sub__(self, other):
        if isinstance(other, Vector):
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
        if isinstance(other, Transform):
            return (other.vector - self.vector).len_vector()
        elif isinstance(other, Vector):
            return (other - self.vector).len_vector()

    def positions(self):
        return self.vector.get_cords()

    def goto(self, other: Vector, speed=1):
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


class ImageDuplicator:
    def __init__(self, image_path, width, height, screen, character):
        self.width = width
        self.height = height
        self.n = 2
        self.character = character
        self.image_orig = pygame.image.load(image_path)
        self.image_orig_rect = self.image_orig.get_rect()
        self.image = pygame.transform.scale(self.image_orig,
                                            (self.image_orig_rect.width * 10, self.image_orig_rect.height * 10))
        self.image_rect = self.image.get_rect()
        # Рассчитываем позиции для дубликатов
        self.spacing = 0  # Расстояние между изображениями
        self.total_width = self.n * self.image_rect.width + (self.n - 1) * self.spacing
        self.total_height = self.n * self.image_rect.height + (self.n - 1) * self.spacing
        self.start_x = (width - self.total_width) // 2
        self.start_y = (height - self.image_rect.height) // 2
        self.screen = screen

    def update(self):
        self.character.background_offset.x %= self.image_rect.width
        self.character.background_offset.y %= self.image_rect.height

        # Отрисовка фона
        # Рисуем только те части фона, которые видны на экране
        for x in range(-self.image_rect.width + int(self.character.background_offset.x), self.width,
                       self.image_rect.width):
            for y in range(-self.image_rect.height + int(self.character.background_offset.y), self.height,
                           self.image_rect.height):
                self.screen.blit(self.image, (x, y))
