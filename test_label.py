import pygame
import sys
import os


lavels = True
select_lavels = False
tick = 8
b = 0
add_text = 0
step_text = 3


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


def draw_label_level(screen):
    screen.fill((0, 0, 0))
    fon = pygame.transform.scale(load_image('data/start_fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 75 + add_text)
    text = font.render("LEVELS", True, (100, 0, b))
    text_x = (width // 2 - text.get_width() // 2)
    text_y = ((height // 2 - text.get_height() // 2) - 200)
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (100, 0, b), (text_x - 10 - add_text // 2, text_y - 13 - add_text // 2,
                                           text_w + 20 + add_text, text_h + 20 + add_text), 5)
    return text_w, text_h, text_x, text_y


def draw_levels(screen):
    screen.fill((0, 0, 0))
    fon = pygame.transform.scale(load_image('data/lvl_fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50 + add_text)
    text_easy = font.render("EASY", True, (100, 0, b))
    text_easy_w = text_easy.get_width() + 20
    text_easy_h = text_easy.get_height() + 20
    text_easy_x = (width // 2 - text_easy.get_width() // 2) - 10
    text_easy_y = (height // 2 - text_easy.get_height() // 2) + 30 - (text_easy_h * 2)
    screen.blit(text_easy, (text_easy_x + 10, text_easy_y + 10))
    pygame.draw.rect(screen, (100, 0, b), (text_easy_x, text_easy_y,
                                           text_easy_w, text_easy_h), 3)
    font = pygame.font.Font(None, 50 + add_text)
    text_hard = font.render("HARD", True, (100, 0, b))
    text_hard_w = text_hard.get_width() + 20
    text_hard_h = text_hard.get_height() + 20
    text_hard_x = (width // 2 - text_hard.get_width() // 2) - 10
    text_hard_y = (height // 2 - text_hard.get_height() // 2) + (text_hard_h * 2) - 50
    screen.blit(text_hard, (text_hard_x + 10, text_hard_y + 10))
    pygame.draw.rect(screen, (100, 0, b), (text_hard_x, text_hard_y,
                                           text_hard_w, text_hard_h), 3)
    font = pygame.font.Font(None, 50 + add_text)
    text_medium = font.render("MEDIUM", True, (100, 0, b))
    text_medium_w = text_medium.get_width() + 20
    text_medium_h = text_medium.get_height() + 20
    text_medium_x = (width // 2 - text_medium.get_width() // 2) - 10
    text_medium_y = (height // 2 - text_medium.get_height() // 2) - 10
    screen.blit(text_medium, (text_medium_x + 10, text_medium_y + 10))
    pygame.draw.rect(screen, (100, 0, b), (text_medium_x, text_medium_y,
                                           text_medium_w, text_medium_h), 3)
    location_labels_levels = [[text_easy_x, text_easy_y, text_easy_h, text_easy_w],
                              [text_medium_x, text_medium_y, text_medium_h, text_medium_w],
                              [text_hard_x, text_hard_y, text_hard_w, text_hard_w]]
    return location_labels_levels


def level_selection(pos, loc):
    global tick
    global select_lavels
    e_x, e_y, e_h, e_w = loc[0]
    m_x, m_y, m_h, m_w = loc[1]
    h_x, h_y, h_h, h_w = loc[2]
    if e_x < pos[0] < e_x + e_w and e_y < pos[1] < e_y + e_h:
        # ставим лёгкий уровень
        print('esay')
    elif m_x < pos[0] < m_x + m_w and m_y < pos[1] < m_y + m_h:
        # ставим средний уровень
        print('medium')
    elif h_x < pos[0] < h_x + h_w and h_y < pos[1] < h_y + h_h:
        # ставим средний уровень
        print('hard')
    tick = 60


def clicking_on_the_level_label(pos, label_level):
    global lavels
    global select_lavels
    w, h, x, y = label_level
    if x < pos[0] < x + w and y < pos[1] < y + h:
        lavels = False
        select_lavels = True


pygame.init()
width = 1900
height = 900
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('Geometry_Dash_Python')

platforms_sprites = pygame.sprite.Group()
pers_sprites = pygame.sprite.Group()
ladders_sprites = pygame.sprite.Group()

step = 10
color_step = 15
cloock = pygame.time.Clock()
running = True
label_level = ''
while running:
    if add_text == 15:
        step_text -= 3
    elif add_text == 0:
        step_text = 3
    add_text += step_text
    if b == 255:
        color_step = -15
    elif b == 0:
        color_step = 15
    b += color_step
    screen.fill((0, 0, 0))
    if lavels:
        label_level = draw_label_level(screen)
    elif select_lavels:
        levels = draw_levels(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if lavels:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicking_on_the_level_label(event.pos, label_level)
        elif select_lavels:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                level_selection(event.pos, levels)
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
    cloock.tick(tick)
    pygame.display.flip()
