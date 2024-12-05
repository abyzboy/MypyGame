import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Движущийся круг 2')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    character = pygame.Surface((50, 50))
    pygame.draw.circle(character, 'red', (25, 25), 50)
    xpos = 0
    running = True
    x_pos = 0
    v = 20  # пикселей в секунду
    fps = 60
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        screen.blit(character, (xpos, 50))
        xpos += 10
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()