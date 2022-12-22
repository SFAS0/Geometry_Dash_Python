import pygame
import sys
import os


def load_image(name, color_key=None):
    if not os.path.isfile(name):
        print('Файл не найден')
        sys.exit()
    image = pygame.image.load(name)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image.convert_alpha()
    return image


class Levels(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image('data/button.jpg')
        self.rect = self.image.get_rect()
        self.rect.x = 320
        self.rect.y = 400

    def update(self, pos):
        if self.rect.collidepoint(pos):
            pass


pygame.init()
size = width, height = 1000, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Geometry Dash - начальное окно')
clock = pygame.time.Clock()

font = pygame.font.Font(None, 125)
text = font.render('Geometry Dash', True, (0, 255, 0))
font2 = pygame.font.Font(None, 75)
text2 = font.render('Levels', True, (0, 255, 0))

all_sprites = pygame.sprite.Group()
lvls = Levels(all_sprites)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            all_sprites.update(event.pos)
    screen.fill((0, 0, 255))
    screen.blit(text, (200, 100))
    all_sprites.draw(screen)
    screen.blit(text2, (370, 420))
    clock.tick(60)
    pygame.display.flip()
pygame.quit()
