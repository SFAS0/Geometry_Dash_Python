import pygame
import sys


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self, *args):
        if args and type(args[0]) == tuple:
            if args[0][pygame.K_w]:
                self.rect = self.rect.move(0, -10)
                print('up')
            if args[0][pygame.K_s]:
                self.rect = self.rect.move(0, 10)
            if args[0][pygame.K_a]:
                self.rect = self.rect.move(-10, 0)
            if args[0][pygame.K_d]:
                self.rect = self.rect.move(10, 0)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def load_image(filename):
    filename = 'data/' + filename
    return pygame.image.load(filename).convert_alpha()


def terminate():
    pygame.quit()
    sys.exit()


def error_screen():
    text = ['Произошла ошибка',
            'Нажмите любую клавишу',
            'для выхода из игры']

    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


pygame.init()
size = width, height = 800, 800

screen = pygame.display.set_mode(size)
FPS = 30
clock = pygame.time.Clock()

start_screen()
level = load_level('map.txt')


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mar.png')

tile_width = tile_height = 50

player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player, level_x, level_y = generate_level(level)

camera = Camera()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            x, y = player.pos
            if event.key == pygame.K_LEFT:
                if x > 0 and level_map[y][x - 1] == '.':
                    player.pos = x - 1, y
                    player.rect = player.image.get_rect().move(tile_width * player.pos[0] + 15,
                                                               tile_height * player.pos[1] + 5)
            elif event.key == pygame.K_RIGHT:
                if x < level_x and level_map[y][x + 1] == '.':
                    player.pos = x + 1, y
                    player.rect = player.image.get_rect().move(tile_width * player.pos[0] + 15,
                                                               tile_height * player.pos[1] + 5)
            elif event.key == pygame.K_UP:
                if 0 < y and level_map[y - 1][x] == '.':
                    player.pos = x, y - 1
                    player.rect = player.image.get_rect().move(tile_width * player.pos[0] + 15,
                                                               tile_height * player.pos[1] + 5)
            elif event.key == pygame.K_DOWN:
                if y < level_y and level_map[y + 1][x] == '.':
                    player.pos = x, y + 1
                    player.rect = player.image.get_rect().move(tile_width * player.pos[0] + 15,
                                                               tile_height * player.pos[1] + 5)
    all_sprites.update(pygame.key.get_pressed())

    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)

    screen.fill((0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()