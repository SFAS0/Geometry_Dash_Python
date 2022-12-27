import pygame
from functions import load_image


class Personage(pygame.sprite.Sprite):
    def __init__(self, pos, group, name_file):
        super().__init__(group)
        self.image = load_image(name_file)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, obj=None, action=''):
        self.rect = self.rect.move(20, 0)
        if action == 'up':
            self.rect = self.rect.move(0, -28)
        elif not pygame.sprite.spritecollideany(self, obj):
            self.rect = self.rect.move(0, 28)


class Ground(pygame.sprite.Sprite):
    def __init__(self, group, name, pos):
        super().__init__(group)
        self.image = load_image(name)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0] * 50
        self.rect.y = pos[1] * 50
