import pygame
from PIL import Image
from Engine import Controller
from Character import Character
from Enemy import Enemy

if __name__ == "__main__":
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.flip()
    clock = pygame.time.Clock()
    fps = 60
    running = True
    controller = Controller()
    character = Character(screen, (100, 100), 10)
    enemy = Enemy(screen, (250, 20), character, 5)
    print(controller.right)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill('green')
        enemy.update_frame()
        character.update_frame()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
