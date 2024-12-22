import time

from Scripts.Camera import Camera
from Scripts.GameObjects import Enemy

first_time = time.time()


def spawn(count_enemies, points, enemies, delay, camera: Camera):
    global first_time
    if time.time() - first_time >= delay:
        point_num = 0
        for i in range(count_enemies):
            enemy = Enemy(points[point_num], camera.character, camera.screen, 2, 25)
            camera.add_objects(enemy)
            if len(points) > point_num + 1:
                point_num += 1
            else:
                point_num = 0
        first_time = time.time()
