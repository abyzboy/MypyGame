import pygame

from Scripts.Camera import Camera
from Scripts.GameObjects.Character import Character
from Scripts.GameObjects.Enemy import Enemy
from Scripts.GameObjects.StaticObject import StaticObject
from Scripts.bullet import Bullet

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
    enemy = Enemy((250, 20), character, 2, screen)
    enemy1 = Enemy((300, 1000), character, 1, screen)
    objects = [character, ground, enemy, enemy1]

    camera.add_objects(*objects)
    character.camera = camera

    reload_event = pygame.event.custom_type()
    clear_event_obj = pygame.event.custom_type()
    pygame.time.set_timer(reload_event, 1000000)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == reload_event:
                character.create_bullet()
        screen.fill('green')
        camera.draw_objects()
        for obj in camera.objects:
            obj.update_frame()
            obj.update_collision(camera.objects)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
