from random import randint

from Scripts.Buffs import BuffSpeed, BuffDamageBullet, BuffDamageGoldBullet, BuffDurationBullet
from Scripts.Camera import Camera
from Scripts.Engine import FPS, ImageDuplicator
from Scripts.GameObjects import *
from Scripts.Spawner import spawn
from Scripts.UI import check_button_buffs, notification_new_level, draw_health_bar, Button, draw_record

pause = 0
def random_buffs(b):
    for i in range(2):
        if character.level >= 5:
            rand = randint(0, 3)
        else:
            rand = randint(0, 2)
        b[i] = buffs[rand]


def start_game():
    global wave, character, game_over, image_duplicator, buffs
    character = Character('assets/character.png', 'assets/character_damaged.png', (400, 300), 3, screen)
    wave = 0
    camera.objects = [character]
    camera.character = character
    character.camera = camera
    game_over = False
    image_duplicator.character = character
    buffs = [BuffSpeed(character),
             BuffDamageBullet(character),
             BuffDurationBullet(character),
             BuffDamageGoldBullet(character)]


if __name__ == "__main__":
    record = open('assets/max_wave.txt', 'r').readline()
    buttons = [
        Button(300, 200, 200, 50, "START GAME", (117, 162, 200), (117, 162, 200), start_game)]
    pygame.init()
    pygame.mixer.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.flip()
    clock = pygame.time.Clock()
    running = True

    character = Character('assets/character.png', 'assets/character_damaged.png', (400, 300), 3, screen)
    image_duplicator = ImageDuplicator('assets/image.png', width, height, screen, character)
    camera = Camera(screen, character)
    camera.add_objects(character)
    character.camera = camera
    reload_event = pygame.event.custom_type()
    clear_event_obj = pygame.event.custom_type()
    lose_event = pygame.USEREVENT + 2
    event_get_new_level = pygame.USEREVENT + 1

    buffs = [BuffSpeed(character),
             BuffDamageBullet(character),
             BuffDurationBullet(character),
             BuffDamageGoldBullet(character)]

    buffs_get = [0, 0]

    buffs_pos = [100, 300]

    buffs_button_offset = 60

    timer_new_lvl_notification = 3

    wave = 0
    game_over = 1
    while running:
        if not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == event_get_new_level:
                    random_buffs(buffs_get)
                    pause = 1
                    timer_new_lvl_notification = 0
                if event.type == lose_event:
                    game_over = True
                    max_wave = max(int(open('assets/max_wave.txt', 'r').readline()), wave)
                    open('assets/max_wave.txt', 'w').write(f'{wave}')
                    record = max_wave
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and pause:
                    pause = check_button_buffs(event, buffs, buffs_pos, buffs_get, buffs_button_offset)
            screen.fill('black')
            image_duplicator.update()
            camera.draw_objects()
            if not pause:
                for i in range(len(camera.objects)):
                    camera.objects[i].update_frame()
                    camera.objects[i].update_collision(camera.objects)
                if not camera.is_enemies_on_map():
                    wave += 1
                    spawn(wave, character)
            if pause:
                pos = buffs_pos
                for i in range(2):
                    buffs_get[i].draw(screen, pos)
                    pos = pos[0] + buffs_get[i].size_button[0] + buffs_button_offset, pos[1]
            if timer_new_lvl_notification < 3:
                notification_new_level(screen, (width // 2 - 75, height // 2 - 100))
                timer_new_lvl_notification += 1 / FPS
            draw_health_bar(character.health, screen)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                for button in buttons:
                    button.handle_event(event)

            mouse_pos = pygame.mouse.get_pos()
            for button in buttons:
                button.check_hover(mouse_pos)

            screen.fill('black')
            draw_record(250, 100, screen, record)
            for button in buttons:
                button.draw(screen)
            pygame.display.flip()
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
