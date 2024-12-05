import pygame
from PIL import Image


class Controller:
    up = pygame.K_w
    down = pygame.K_s
    right = pygame.K_d
    left = pygame.K_a


class Enemy:
    def __init__(self, cords, charact, speed):
        self.transform = Transform(cords)
        self.can_walk = True
        self.speed = speed
        self.charact = charact
        self.char = pygame.Surface((50, 50))
        self.char.fill((0, 0, 0, 0))
        pygame.draw.circle(self.char, 'red', (25, 25), 25)

    def update_frame(self):
        if int(self.transform.dist(self.charact.transform)) < 50:
            self.can_walk = False
        if int(self.transform.dist(self.charact.transform)) > 70:
            self.can_walk = True
        if self.can_walk:
            self.transform.goto(self.charact.transform, self.speed)
        screen.blit(self.char, self.transform.positions())


class Character:
    def __init__(self, cords, speed):
        self.sprite = pygame.image.load('character.png')
        self.controller = Controller()
        self.transform = Transform(cords)
        self.speed = speed
        self.character = pygame.Surface((50, 50))
        self.character.fill((0, 0, 0, 0))
        pygame.draw.circle(self.character, 'blue', (25, 25), 20)

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
        if x and y:
            vector = Vector((x, y))
            normalized_vector = vector.normalize()
            self.transform.xpos += normalized_vector.x * self.speed
            self.transform.ypos += normalized_vector.y * self.speed
        else:
            self.transform.xpos += x * self.speed
            self.transform.ypos += y * self.speed

    def update_frame(self):
        self.move()
        screen.blit(self.character, self.transform.positions())


def strip_img():
    img = Image.open("assets/SUNNYSIDE_WORLD_CHARACTERS_PARTS_V0.3.1/IDLE/base_idle_strip9.png")
    x, y = img.size
    crop_img = img.crop((0, 0, 96, 64))
    crop_img.save("character.png")


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


if __name__ == "__main__":
    controller = Controller()
    character = Character((100, 100), 7)
    enemy = Enemy((20, 20), character, 5)
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.flip()
    clock = pygame.time.Clock()
    fps = 60
    running = True
    print(controller.right)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill('black')
        enemy.update_frame()
        character.update_frame()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
