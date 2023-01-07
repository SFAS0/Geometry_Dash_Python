import pygame

from functions import load_image, load_level, all_sprites
from personage import Personage, Objects


lavels = True
select_lavels = False
b = 0
add_text = 0
step_text = 3


pygame.init()
width = 1900
height = 900
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('Geometry_Dash_Python')

fon_start = pygame.transform.scale(load_image('data/fons/start_fon.png'), (width, height))
fon_levels = pygame.transform.scale(load_image('data/fons/lvl_fon.png'), (width, height))


def draw_label_level(screen):
    screen.fill((0, 0, 0))
    screen.blit(fon_start, (0, 0))
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


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '0':
                pass
            elif level[y][x] == '1':
                Objects(ground_sprites, 'data/obstacles/pol1.png', (x, y))
            elif level[y][x] == '2':
                Objects(obstacles_group, 'data/obstacles/pol2.png', (x, y))
            elif level[y][x] == '@':
                new_player = Personage((x, y), pers_sprites, 'data/cube/avatar.png')
                level[y][x] = '.'
            elif level[y][x] == '4':
                Objects(obstacles_group, 'data/obstacles/triangle1.png', (x, y))
            elif level[y][x] == '3':
                Objects(obstacles_group, 'data/obstacles/block.png', (x, y))
            elif level[y][x] == '7':
                Objects(obstacles_group, 'data/obstacles/180_low_triangel.png', (x, y))
            elif level[y][x] == '*':
                Objects(obstacles_group, 'data/obstacles/low_triangel.png', (x, y))
            elif level[y][x] == '_':
                Objects(ground_sprites, 'data/obstacles/low_block.png', (x, y))
            elif level[y][x] == '$':
                Objects(point_group, 'data/treasure/point.png', (x, y))
            elif level[y][x] == '|':
                Objects(finish_group, 'data/obstacles/finish.png', (x, y))
    return new_player, x, y


def draw_levels(screen):
    screen.fill((0, 0, 0))
    screen.blit(fon_levels, (0, 0))
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


pers_sprites = pygame.sprite.Group()
ground_sprites = pygame.sprite.Group()
obstacles_group = pygame.sprite.Group()
point_group = pygame.sprite.Group()
finish_group = pygame.sprite.Group()

step = 10
color_step = 15

player = None


class Camera:
    def __init__(self):
        self.dx = 0

    def apply(self, obj):
        obj.rect.x += self.dx

    def update(self, target):
        self.dx = -(target.rect.x - 280)


camera = Camera()


def level_selection(pos=(0, 0), loc=((0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)), run_lvl=''):
    global select_lavels
    global lvl_start
    global level_map
    global player, level_x, level_y, running_level
    e_x, e_y, e_h, e_w = loc[0]
    m_x, m_y, m_h, m_w = loc[1]
    h_x, h_y, h_h, h_w = loc[2]
    if e_x < pos[0] < e_x + e_w and e_y < pos[1] < e_y + e_h or run_lvl == 'lvl1':
        lvl_start = True
        running_level = 'lvl1'
    elif m_x < pos[0] < m_x + m_w and m_y < pos[1] < m_y + m_h or run_lvl == 'lvl2':
        lvl_start = True
        running_level = 'lvl2'
    elif h_x < pos[0] < h_x + h_w and h_y < pos[1] < h_y + h_h or run_lvl == 'lvl3':
        lvl_start = True
        running_level = 'lvl3'
    if lvl_start:
        select_lavels = False
        player, level_x, level_y = generate_level(load_level(f'lvls/{running_level}.txt'))
        pygame.mixer.music.load(f'data/sounds/{running_level}.mp3')
        pygame.mixer.music.play(0, True, 0)


running = True
label_level = ''
lvl_start = False
tick = 60
cloock = pygame.time.Clock()
sprites = [pers_sprites, ground_sprites, obstacles_group, point_group, finish_group]
fon = pygame.transform.scale(load_image('data/fons/bg.png'), (width, height))
while running:
    if lvl_start:
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        screen.blit(fon, (0, 0))
        ans = player.update((ground_sprites, obstacles_group))
        for group in sprites:
            group.draw(screen)
        if ans == "DEAD":
            for group in sprites:
                group.empty()
            level_selection(run_lvl=running_level)
    else:
        if add_text == 15:
            step_text = -1
        elif add_text == 0:
            step_text = 1
        add_text += step_text
        if b == 255:
            color_step = -5
        elif b == 0:
            color_step = 5
        b += color_step
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and lvl_start:
            player.update((ground_sprites, obstacles_group), 'up')
    cloock.tick(tick)
    pygame.display.flip()
