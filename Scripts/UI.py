from Scripts.Engine import draw_multiline_text, pygame


def check_button_buffs(event, buffs, buffs_pos, buffs_get, buffs_button_offset):
    if (-buffs[0].offset_button[0] + buffs_pos[0] < event.pos[0] < buffs_pos[0] + buffs[0].size_button[0] +
        buffs[0].offset_button[
            0]) and \
            (-buffs[0].offset_button[1] + buffs_pos[1] < event.pos[1] < buffs_pos[1] + buffs[0].size_button[1] +
             buffs[0].offset_button[1]):
        buffs_get[0].chose()
        return 0
    elif (-buffs[0].offset_button[0] + buffs_pos[0] + buffs[0].size_button[0] + buffs_button_offset < event.pos[0] <
          buffs_pos[0] +
          buffs[0].size_button[0] + buffs[0].size_button[0] + buffs_button_offset + buffs[0].offset_button[
              0]) and \
            (-buffs[0].offset_button[1] + buffs_pos[1] < event.pos[1] < buffs_pos[1] + buffs[0].size_button[1] +
             buffs[0].offset_button[1]):
        buffs_get[1].chose()
        return 0
    return 1


def notification_new_level(screen, pos):
    font = pygame.font.Font('assets/fonts/HarryPotterKudosEN-en.ttf', 30)
    draw_multiline_text(screen, 'level up', font, pos, (117, 162, 200), (0, 0, 0), 4)


def draw_health_bar(health, screen):
    font = pygame.font.Font('assets/fonts/HarryPotterKudosEN-en.ttf', 30)
    draw_multiline_text(screen, f'health: {health}/100', font, (25, 25), (255, 100, 200), (0, 0, 0), 4)


def draw_record(x_pos, y_pos, screen, wave):
    font = pygame.font.Font('assets/fonts/HarryPotterKudosEN-en.ttf', 30)
    draw_multiline_text(screen, f'Max wave survived: {wave}', font, (x_pos, y_pos), (0, 0, 0), (117, 162, 200), 4)


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, function=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.function = function
        self.is_hovered = False

    def draw(self, screen):
        # Определяем цвет кнопки (обычный или при наведении)
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)

        # Отрисовка текста
        font = pygame.font.Font('assets/fonts/HarryPotterKudosEN-en.ttf', 30)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Левая кнопка мыши
            if self.is_hovered and self.function:
                self.function()  # Вызов функции, если кнопка нажата
