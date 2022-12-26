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


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


tile_images = {
    'pol1': load_image('data/obstacles/pol1.png'),
    'pol2': load_image('data/obstacles/pol2.png')
}
player_image = load_image('data/obstacles/avatar.png')
tile_width = tile_height = 50


class Ground(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, ground_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Cube(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, player_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = pos_x, pos_y


player = None


ground_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '0':
                pass
            elif level[y][x] == '1':
                Ground('pol1', x, y)
            elif level[y][x] == '2':
                Ground('pol2', x, y)
            elif level[y][x] == '@':
                new_player = Cube(x, y)
                level[y][x] = '.'
    return new_player, x, y


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


# camera = Camera()
level_map = load_level('lvl1.txt')
player, level_x, level_y = generate_level(level_map)


def level_selection(pos, loc):
    global tick
    global select_lavels
    global lvl_start
    e_x, e_y, e_h, e_w = loc[0]
    m_x, m_y, m_h, m_w = loc[1]
    h_x, h_y, h_h, h_w = loc[2]
    if e_x < pos[0] < e_x + e_w and e_y < pos[1] < e_y + e_h:
        lvl_start = True
        print('esay')
    elif m_x < pos[0] < m_x + m_w and m_y < pos[1] < m_y + m_h:
        # ставим средний уровень
        print('medium')
    elif h_x < pos[0] < h_x + h_w and h_y < pos[1] < h_y + h_h:
        # ставим средний уровень
        print('hard')
    tick = 60


running = True
label_level = ''
lvl_start = False
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
            key = pygame.key.get_pressed()
            if key[pygame.K_UP]:
                pass
    # camera.update(player)
    # for sprite in ground_sprites:
    #     camera.apply(sprite)
    if lvl_start:
        fon = pygame.transform.scale(load_image('data/obstacles/bg.png'), (width, height))
        screen.blit(fon, (0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        platforms_sprites.draw(screen)
        platforms_sprites.update()
    cloock.tick(tick)
    pygame.display.flip()
