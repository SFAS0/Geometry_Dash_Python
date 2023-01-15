import pygame

from functions import load_image, all_sprites, ground_sprites, obstacles_group, finish_group


class Personage(pygame.sprite.Sprite):
    def __init__(self, pos, group, name):
        super().__init__(group, all_sprites)
        self.group = group
        self.frames = []
        self.cut_sheet(load_image("data/cube/anim_cub.png"), 12, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0] * 50
        self.rect.y = pos[1] * 50
        self.count = 0
        self.jumped = False

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def is_dead(self):
        ans = "LIFE"
        if pygame.sprite.spritecollideany(self, obstacles_group) and not self.jumped:
            ans = "DEAD"
        return ans

    def game_end(self):
        return pygame.sprite.spritecollideany(self, finish_group)

    def update(self, action=''):
        if self.is_dead() == 'LIFE':
            if self.jumped:
                self.count += 1
            if self.count == 10:
                self.jumped = False
            self.rect = self.rect.move(17, 0)
            if action == 'up' and pygame.sprite.spritecollideany(self, ground_sprites):
                self.rect = self.rect.move(0, -100)
                self.jumped = True
                self.count = 0
            elif not pygame.sprite.spritecollideany(self, ground_sprites):
                self.rect = self.rect.move(0, 11)
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
            elif pygame.sprite.spritecollideany(self, ground_sprites):
                if self.cur_frame % 3 == 0:
                    self.image = self.frames[self.cur_frame]
                else:
                    try:
                        if (self.cur_frame + 1) % 3 == 0:
                            self.image = self.frames[self.cur_frame + 1]
                        else:
                            self.image = self.frames[self.cur_frame + 2]
                    except IndexError:
                        self.image = self.frames[0]


class Objects(pygame.sprite.Sprite):
    def __init__(self, group, name, pos):
        super().__init__(group, all_sprites)
        self.image = load_image(name)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0] * 50
        self.rect.y = pos[1] * 50
