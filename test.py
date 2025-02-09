import pygame
import sys

# Инициализация pygame
pygame.init()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Шрифт
font = pygame.font.Font(None, 36)  # Шрифт по умолчанию, размер 36

# Размеры экрана
WIDTH = 800
HEIGHT = 600

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Главное меню")

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, function=None):
        """
        Инициализация кнопки.
        :param x: Координата X верхнего левого угла кнопки.
        :param y: Координата Y верхнего левого угла кнопки.
        :param width: Ширина кнопки.
        :param height: Высота кнопки.
        :param text: Текст на кнопке.
        :param color: Цвет кнопки.
        :param hover_color: Цвет кнопки при наведении.
        :param function: Функция, которая будет вызвана при нажатии на кнопку.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.function = function
        self.is_hovered = False

    def draw(self, screen):
        """
        Отрисовка кнопки на экране.
        :param screen: Экран, на котором будет отрисована кнопка.
        """
        # Определяем цвет кнопки (обычный или при наведении)
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)

        # Отрисовка текста
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        """
        Проверка, находится ли курсор мыши над кнопкой.
        :param mouse_pos: Позиция курсора мыши.
        """
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        """
        Обработка событий кнопки.
        :param event: Событие pygame.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Левая кнопка мыши
            if self.is_hovered and self.function:
                self.function()  # Вызов функции, если кнопка нажата

# Функции для кнопок
def start_game():
    print("Игра начата!")  # Заглушка для начала игры

def show_leaderboard():
    print("Таблица рекордов:")  # Заглушка для таблицы рекордов
    print("1. Игрок 1 - 100 очков")
    print("2. Игрок 2 - 80 очков")
    print("3. Игрок 3 - 50 очков")

def quit_game():
    pygame.quit()
    sys.exit()

# Создание кнопок
buttons = [
    Button(300, 200, 200, 50, "START GAME", GREEN, BLUE, start_game),
    Button(300, 300, 200, 50, "RECORDS", GREEN, BLUE, show_leaderboard),
    Button(300, 400, 200, 50, "QUIT", RED, GRAY, quit_game)
]

# Основной цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for button in buttons:
            button.handle_event(event)  # Обработка событий для каждой кнопки

    # Проверка наведения на кнопки
    mouse_pos = pygame.mouse.get_pos()
    for button in buttons:
        button.check_hover(mouse_pos)

    # Отрисовка
    screen.fill(WHITE)
    for button in buttons:
        button.draw(screen)
    pygame.display.flip()

# Завершение работы
pygame.quit()
sys.exit()