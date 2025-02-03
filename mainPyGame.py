from Scripts.Buffs import BuffSpeed, BuffDamageBullet, BuffDamageGoldBullet, BuffDurationBullet
from Scripts.Camera import Camera
from Scripts.GameObjects import *
from Scripts.GameObjects import StaticObject
from Scripts.Spawner import spawn
from Scripts.Engine import FPS
from random import randint
from Scripts.UI.UI import check_button_buffs, notification_new_level
pause = 0


def random_buffs(b):
    for i in range(2):
        if character.level >= 5:
            rand = randint(0, 3)
        else:
            rand = randint(0, 2)
        b[i] = buffs[rand]


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

    enemy = Enemy('enemy.png', 'enemy_damage.png',(250, 20), character, screen, 1)
    enemy1 = Enemy('enemy.png', 'enemy_damage.png',(300, 1000), character, screen, 2)
    enemy2 = EnemyShooters('assets/Robot/robot.png', 'assets/Robot/robot.png', (100, 100), character, screen, 3, 20)
    objects = [character, ground, enemy, enemy1, enemy2]

    camera.add_objects(*objects)
    character.camera = camera
    enemy2.camera = camera
    reload_event = pygame.event.custom_type()
    clear_event_obj = pygame.event.custom_type()
    event_get_new_level = pygame.USEREVENT + 1

    buffs = [BuffSpeed(character),
             BuffDamageBullet(character),
             BuffDurationBullet(character),
             BuffDamageGoldBullet(character)]

    buffs_get = [0,0]

    buffs_pos = [100, 300]

    buffs_button_offset = 60

    timer_new_lvl_notification = 3
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == event_get_new_level:
                random_buffs(buffs_get)
                pause = 1
                timer_new_lvl_notification = 0
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and pause:
                pause = check_button_buffs(event,buffs,buffs_pos, buffs_get, buffs_button_offset)
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
        if timer_new_lvl_notification < 3:
            notification_new_level(screen, (width // 2- 75, height // 2 - 350))
            timer_new_lvl_notification += 1 / FPS
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
