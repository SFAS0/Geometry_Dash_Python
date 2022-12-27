import pygame
from functions import load_image


# tile_images = {
#     'pol1': load_image('data/obstacles/pol1.png'),
#     'pol2': load_image('data/obstacles/pol2.png')
# }


class Personage(pygame.sprite.Sprite):
    def __init__(self, pos, group, name_file):
        super().__init__(group)
        self.image = load_image(name_file)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, obj=None):
        self.rect = self.rect.move(12, 0)
        if obj == 'up':
            self.rect = self.rect.move(0, -12)
        elif not pygame.sprite.spritecollideany(self, obj):
            self.rect = self.rect.move(0, 12)


class Ground(pygame.sprite.Sprite):
    def __init__(self, group, name, pos):
        super().__init__(group)
        self.image = load_image(name)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0] * 50
        self.rect.y = pos[1] * 50
