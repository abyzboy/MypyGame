import random

from Scripts.Engine import Vector
from Scripts.GameObjects import EnemyShooters, Enemy


def make_spawn_position(center_pos):
    center_pos = [int(x) for x in center_pos]
    while True:
        cord = random.randint(center_pos[0] - 400, center_pos[0] + 400), random.randint(center_pos[1] - 400,
                                                                                        center_pos[1] + 400)
        vec_cord = Vector(cord)
        vec_center = Vector(center_pos)
        if vec_center.dist(vec_cord) > 100:
            return cord


def spawn(wave, character):
    camera = character.camera
    screen = camera.screen
    damage_multiply = 5 * 0.3
    health_multiply = 8 * 0.25
    speed_multiply = 8 * 0.1
    if wave >= 5:
        damage_multiply = 5 * 0.45
        health_multiply = 8 * 0.4
        speed_multiply = 8 * 0.15
    if wave >= 10:
        damage_multiply = 10 * 0.6
        health_multiply = 11 * 0.5
        speed_multiply = 15 * 0.4
    if wave >= 20:
        damage_multiply = wave/3 * 0.6
        health_multiply = wave/3 * 0.5
        speed_multiply = wave/3* 0.4
    center_pos = character.transform.vector.get_cords()
    if wave % 3 == 0:
        for i in range(2):
            cord = make_spawn_position(center_pos)
            enemy = EnemyShooters('assets/enemy/idl_robot.png', 'assets/enemy/damage_robot.png',
                                  cord, character, screen, 1 + (1 * speed_multiply), 30 + (30 * health_multiply),
                                  10 + (10 * damage_multiply))
            camera.add_objects(enemy)
        for i in range(3):
            cord = make_spawn_position(center_pos)
            enemy = Enemy('assets/enemy/orc.png', 'assets/enemy/damage_orc.png', cord, character, screen, 1 + (1 * speed_multiply),
                          70 + (70 * health_multiply), 10 + (10 * damage_multiply))
            camera.add_objects(enemy)
    else:
        for i in range(3):
            cord = make_spawn_position(center_pos)
            enemy = Enemy('assets/enemy/orc.png', 'assets/enemy/damage_orc.png', cord, character, screen, 1 + (1 * speed_multiply),
                          70 + (70 * health_multiply), 10 + (10 * damage_multiply))
            camera.add_objects(enemy)
