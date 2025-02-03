import pygame

from Scripts.GameObjects import Character
from Scripts.Engine import draw_text_with_outline, draw_multiline_text


class Buff:
    def __init__(self, character: Character):
        self.size_button = 290, 60
        self.offset_button = 10, 20
        self.character = character
        self.font = pygame.font.Font('assets/fonts/HarryPotterKudosEN-en.ttf', 25)

    def chose(self):
        pass

    def draw(self, screen, pos):
        pass


class BuffSpeed(Buff):
    def __init__(self, character):
        super().__init__(character)

    def chose(self):
        self.character.speed += self.character.speed * 0.05
        print('new speed:', self.character.speed)

    def draw(self, screen, pos):
        pygame.draw.rect(screen, (83, 106, 251), (pos[0] - self.offset_button[0], pos[1] - self.offset_button[1],
                                                  self.size_button[0] + self.offset_button[0],
                                                  self.size_button[1] + self.offset_button[1]), 0)
        draw_text_with_outline(screen, 'Increases speed by 5%', self.font, pos, (117, 162, 200), (0,0,0), 2)


class BuffDamageBullet(Buff):
    def __init__(self, character):
        super().__init__(character)

    def chose(self):
        self.character.damage_bullet += self.character.damage_bullet * 0.05
        print('new damage:', self.character.damage_bullet)

    def draw(self, screen, pos):
        pygame.draw.rect(screen, (83, 106, 251), (pos[0] - self.offset_button[0], pos[1] - self.offset_button[1],
                                                  self.size_button[0] + self.offset_button[0],
                                                  self.size_button[1] + self.offset_button[1]), 0)
        draw_text_with_outline(screen, 'Increases damage by 5%', self.font, pos, (117, 162, 200), (0,0,0), 2)


class BuffDamageGoldBullet(Buff):
    def __init__(self, character):
        super().__init__(character)

    def chose(self):
        self.character.damage_goldBullet += 3

    def draw(self, screen, pos):
        pygame.draw.rect(screen, (83, 106, 251), (pos[0] - self.offset_button[0], pos[1] - self.offset_button[1],
                                                  self.size_button[0] + self.offset_button[0],
                                                  self.size_button[1] + self.offset_button[1]), 0)
        draw_multiline_text(screen, 'Increases damage\ngold bullets by 2 units', self.font, pos, (117, 162, 200), (0,0,0), 2)

class BuffDurationBullet(Buff):
    def __init__(self, character):
        super().__init__(character)
    def chose(self):
        self.character.duration_bullet = 0.1

    def draw(self, screen, pos):
        pygame.draw.rect(screen, (83, 106, 251), (pos[0] - self.offset_button[0], pos[1] - self.offset_button[1],
                                                  self.size_button[0] + self.offset_button[0],
                                                  self.size_button[1] + self.offset_button[1]), 0)
        draw_multiline_text(screen, 'Increases duration\nbullets', self.font, pos, (117, 162, 200),
                            (0, 0, 0), 2)