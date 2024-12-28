import pygame
from pygame.transform import scale

from Buffs import BuffSpeed, BuffDamageBullet, BuffDamageGoldBullet
from Scripts.Camera import Camera
from Scripts.GameObjects import *
from Scripts.GameObjects import StaticObject
from Scripts.Spawner import spawn
from Scripts.Engine import FPS
from random import randint

pause = 0


def random_buffs(b):
    for i in range(2):
        if character.level >= 2:
            rand = randint(0, 2)
        else:
            rand = randint(0, 1)
        b[i] = buffs[rand]
    print('ok')

def check_button(event):
    global pause
    if (-buffs[0].offset_button[0] + buffs_pos[0] < event.pos[0] < buffs_pos[0] + buffs[0].size_button[0] +
        buffs[0].offset_button[
            0]) and \
            (-buffs[0].offset_button[1] + buffs_pos[1] < event.pos[1] < buffs_pos[1] + buffs[0].size_button[1] +
             buffs[0].offset_button[1]):
        buffs_get[0].chose()
        pause = 0
    elif (-buffs[0].offset_button[0] + buffs_pos[0] + buffs[0].size_button[0] + buffs_button_offset < event.pos[0] <
          buffs_pos[0] +
          buffs[0].size_button[0] + buffs[0].size_button[0] + buffs_button_offset + buffs[0].offset_button[
              0]) and \
            (-buffs[0].offset_button[1] + buffs_pos[1] < event.pos[1] < buffs_pos[1] + buffs[0].size_button[1] +
             buffs[0].offset_button[1]):
        buffs_get[1].chose()
        pause = 0


if __name__ == "__main__":
    pygame.init()
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    pygame.display.flip()
    clock = pygame.time.Clock()
    running = True

    character = Character((400, 300), 3, screen)

    camera = Camera(screen, character)

    ground = StaticObject((0, 0), '1.png')

    enemy = Enemy('enemy.png', (250, 20), character, screen, 1)
    enemy1 = Enemy('enemy.png', (300, 1000), character, screen, 2)
    objects = [character, ground, enemy, enemy1]

    camera.add_objects(*objects)
    character.camera = camera

    reload_event = pygame.event.custom_type()
    clear_event_obj = pygame.event.custom_type()
    event_get_new_level = pygame.USEREVENT + 1

    buffs = [BuffSpeed(character),
             BuffDamageBullet(character),
             BuffDamageGoldBullet(character)]

    buffs_get = [0,0]

    buffs_pos = [100, 300]

    buffs_button_offset = 60

    print(-buffs[0].offset_button[1] + buffs_pos[1])
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == event_get_new_level:
                random_buffs(buffs_get)
                pause = 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and pause:
                check_button(event)
        screen.fill('grey')
        camera.draw_objects()
        if not pause:
            spawn(1, [(550, 125)], 0, 5, camera)
            for i in range(len(camera.objects)):
                camera.objects[i].update_frame()
                camera.objects[i].update_collision(camera.objects)
        if pause:
            pos = buffs_pos
            for i in range(2):
                buffs_get[i].draw(screen, pos)
                pos = pos[0] + buffs_get[i].size_button[0] + buffs_button_offset, pos[1]
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
