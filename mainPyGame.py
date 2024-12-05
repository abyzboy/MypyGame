import pygame

from Camera import Camera
from Engine import Controller
from Character import Character
from Enemy import Enemy
from StaticObject import StaticObject

if __name__ == "__main__":
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.flip()
    clock = pygame.time.Clock()
    fps = 60
    running = True
    camera = Camera(screen)
    character = Character((400, 300), 3, screen, camera)

    ground = StaticObject((0, 0), '1.png')
    enemy = Enemy((250, 20), character, 2, screen)
    objects = [ground, enemy]

    camera.add_objects(*objects)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill('green')
        camera.draw_objects()
        character.update_frame()
        enemy.update_frame()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
