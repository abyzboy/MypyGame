import pygame


class Vector:
    def __init__(self, cord):
        self.x = cord[0]
        self.y = cord[1]

    def len_vector(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def normalize(self):
        return Vector((self.x / self.len_vector(), self.y / self.len_vector()))


class Transform:
    def __init__(self, coords=(0, 0)):
        self.xpos = coords[0]
        self.ypos = coords[1]

    def right(self):
        self.xpos += 1

    def dist(self, other):
        return Vector((other.xpos - self.xpos, other.ypos - self.ypos)).len_vector()

    def left(self):
        self.xpos -= 1

    def down(self):
        self.ypos += 1

    def up(self):
        self.ypos -= 1

    def positions(self):
        return self.xpos, self.ypos

    def goto(self, other, speed=1):
        x, y = self.positions()
        other_x, other_y = other.positions()
        vector = Vector(((other_x - x), other_y - y))
        self.xpos += vector.normalize().x * speed
        self.ypos += vector.normalize().y * speed


class Controller:
    up = pygame.K_w
    down = pygame.K_s
    right = pygame.K_d
    left = pygame.K_a
