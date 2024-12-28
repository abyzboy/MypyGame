
import pygame

import sys

# Инициализация Pygame

pygame.init()

# Настройка экрана

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Перенос строк")

# Цвета

text_color = (255, 255, 255)  # Белый

# Шрифт

font = pygame.font.Font(None, 36)

# Текст с переносами

text = "Привет, мир!\nКак дела?\nЭто пример переноса строк."

# Функция для рисования многострочного текста

def draw_multiline_text(surface, text, position, color):

    lines = text.split('\n')  # Разделяем текст на строки

    y_offset = 0  # Смещение по вертикали

    for line in lines:

        rendered_line = font.render(line, True, color)

        surface.blit(rendered_line, (position[0], position[1] + y_offset))

        y_offset += rendered_line.get_height()  # Обновляем смещение по вертикали

# Основной игровой цикл

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()

            sys.exit()

    screen.fill((0, 0, 0))  # Очищаем экран

    draw_multiline_text(screen, text, (50, 50), text_color)

    pygame.display.flip()  # Обновляем экран

