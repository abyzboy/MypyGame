import pygame


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


class Transform:
    def __init__(self, cords=(0, 0)):
        self.vector = Vector(cords)

    def dist(self, other):
        if type(other) == Vector:
            return (other - self.vector).len_vector()

    def positions(self):
        return self.vector.get_cords()

    def goto(self, other, speed=1):
        vector = other - self.vector
        self.vector.x += vector.normalize().x * speed
        self.vector.y += vector.normalize().y * speed


class Controller:
    up = pygame.K_w
    down = pygame.K_s
    right = pygame.K_d
    left = pygame.K_a
