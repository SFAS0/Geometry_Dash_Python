import pygame
import sys
import os


lavels = True


def load_image(name, colorkey=None):
    if not os.path.isfile(name):
        print(f"Файл не найден")
        sys.exit()
    image = pygame.image.load(name)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image.convert_alpha()
    return image


class Platform(pygame.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)
        self.image = pygame.Surface((50, 10))
        pygame.draw.rect(self.image, (128, 128, 128), (0, 0, 50, 10))
        self.rect = pygame.Rect(pos[0], pos[1], 50, 10)


class Landing(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(pers_sprites)
        self.image = pygame.Surface((20, 20))
        pygame.draw.rect(self.image, (0, 0, 255), (0, 0, 20, 20))
        self.rect = pygame.Rect(pos[0], pos[1], 20, 20)

    def update(self, move=0, bt=False):
        if (not pygame.sprite.spritecollideany(self, platforms_sprites)
                and not pygame.sprite.spritecollideany(self, ladders_sprites)):
            self.rect = self.rect.move(0, 1)
        if move != 0 and not bt:
            self.rect = self.rect.move(move, 0)
        if pygame.sprite.spritecollideany(self, ladders_sprites):
            if bt:
                self.rect = self.rect.move(0, move)


class Ladders(pygame.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)
        self.image = pygame.Surface((10, 50))
        pygame.draw.rect(self.image, (255, 0, 0), (0, 0, 10, 50))
        self.rect = pygame.Rect(pos[0], pos[1], 10, 50)


def draw(screen):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("LEVELS", True, (100, 0, 255))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (100, 0, 255), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)
    return text_w, text_h, text_x, text_y


def level_selection(pos, label_level):
    global lavels
    w, h, x, y = label_level
    if x < pos[0] < x + w and y < pos[1] < y + h:
        lavels = False


pygame.init()
width = 500
height = 500
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('Тест')

platforms_sprites = pygame.sprite.Group()
pers_sprites = pygame.sprite.Group()
ladders_sprites = pygame.sprite.Group()

step = 10

cloock = pygame.time.Clock()
running = True
label_level = ''
while running:
    screen.fill((0, 0, 0))
    if lavels:
        label_level = draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if lavels:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                level_selection(event.pos, label_level)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                pers_sprites = pygame.sprite.Group()
                pers = Landing(event.pos)
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                pers.update(-step)
            if key[pygame.K_RIGHT]:
                pers.update(step)
            if ((key[pygame.K_LCTRL] or key[pygame.K_RCTRL])
                    and (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)):
                Ladders(ladders_sprites, event.pos)
            if (event.type == pygame.MOUSEBUTTONDOWN and
                    event.button == 1 and not (key[pygame.K_LCTRL] or key[pygame.K_RCTRL])):
                Platform(platforms_sprites, event.pos)
            if key[pygame.K_UP]:
                pers.update(-step, True)
            if key[pygame.K_DOWN]:
                pers.update(step, True)
    platforms_sprites.draw(screen)
    platforms_sprites.update()
    pers_sprites.draw(screen)
    pers_sprites.update()
    ladders_sprites.draw(screen)
    ladders_sprites.update()
    cloock.tick(50)
    pygame.display.flip()
