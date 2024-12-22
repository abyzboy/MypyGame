from pickle import FRAME

import pygame
from Scripts.Camera import Camera
from Scripts.GameObjects import *
from Scripts.GameObjects import StaticObject
from Scripts.Spawner import spawn

if __name__ == "__main__":
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.flip()
    clock = pygame.time.Clock()
    fps = 60
    running = True
    character = Character((400, 300), 3, screen)
    camera = Camera(screen, character)
    ground = StaticObject((0, 0), '1.png')
    enemy = Enemy((250, 20), character, screen, 1)
    enemy1 = Enemy((300, 1000), character, screen,2)
    objects = [character, ground, enemy, enemy1, character]

    camera.add_objects(*objects)
    character.camera = camera

    reload_event = pygame.event.custom_type()
    clear_event_obj = pygame.event.custom_type()
    while running:
        spawn(2, [(0, 24), (700, 52), (550, 125)], 0, 5, camera)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill('grey')
        camera.draw_objects()
        for i in range(len(camera.objects) - 1, -1, -1):
            camera.objects[i].update_frame()
            camera.objects[i].update_collision(camera.objects)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
