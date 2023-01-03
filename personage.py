import pygame

from functions import load_image


class Personage(pygame.sprite.Sprite):
    def __init__(self, pos, group, name):
        super().__init__(group)
        self.group = group
        self.frames = []
        self.cut_sheet(load_image("data/obstacles/anim_cub.png"), 4, 2)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0] * 50
        self.rect.y = pos[1] * 50

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, obj=None, action=''):
        ans = True
        self.rect = self.rect.move(20, 0)
        if action == 'up' and pygame.sprite.spritecollideany(self, obj):
            self.rect = self.rect.move(0, -100)
        elif not pygame.sprite.spritecollideany(self, obj):
            self.rect = self.rect.move(0, 11)
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        elif pygame.sprite.spritecollideany(self, obj):
            if self.cur_frame % 2 == 0:
                self.image = self.frames[self.cur_frame]
            elif self.cur_frame == 7:
                self.image = self.frames[0]
            else:
                self.image = self.frames[self.cur_frame + 1]
        return ans


class Ground(pygame.sprite.Sprite):
    def __init__(self, group, name, pos):
        super().__init__(group)
        self.image = load_image(name)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0] * 50
        self.rect.y = pos[1] * 50
