import os
import random
import sys

import pygame

FPS = 60
SIZE = WIDTH, HEIGHT = 1024, 768
a, b = WIDTH, HEIGHT
pygame.init()
jump_1 = 'jump1.mp3'
jump_2 = 'jump2.mp3'
main_track = 'Run with Me Kara.mp3'
pygame.mixer.music.load(main_track)
pygame.mixer.music.play()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player = None

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}

tile_width = 200
tile_height = 100


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
                new_player = Player(x, y + 100)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image('cat_anim.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.frames = []
        self.cut_sheet(self.image, 3, 4)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(pos_x, pos_y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, (sheet.get_width() // columns) - 20,
                                sheet.get_height() // rows)
        for i in range(columns):
            for j in range(rows):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, new_x, new_y):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        player.rect.x += 24


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


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
        self.dx = -6
        self.dy = 0
        new = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()

    def create_particles(position):
        # количество создаваемых частиц
        particle_count = 20
        # возможные скорости
        numbers = range(-5, 6)
        for _ in range(particle_count):
            Particle(position, random.choice(numbers), random.choice(numbers))


class Ship(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/' + image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Кот бежит по крыше",
                  "уворачивайтесь от препятствий посредством прыжка",
                  "Удачи!"]

    fon = pygame.transform.scale(load_image('unnamed.jpg'), (WIDTH, HEIGHT))
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
    camera = Camera()
    game_begin = False
    k = 0
    ship = Ship("fon.jpg", [0, 0])
    while True:
        if k == 1000:
            k = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif (event.type == pygame.KEYDOWN or \
                  event.type == pygame.MOUSEBUTTONDOWN) and game_begin is False:
                game_begin = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                sound_jump_down = pygame.mixer.Sound(jump_2)
                player.rect.y += 80
                pygame.mixer.music.pause()
                sound_jump_down.play()
                pygame.mixer.music.unpause()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                sound_jump_up = pygame.mixer.Sound(jump_1)
                player.rect.y -= 80
                pygame.mixer.music.pause()
                sound_jump_up.play()
                pygame.mixer.music.unpause()

        if game_begin:
            screen.fill('white')
            all_sprites.draw(screen)
            screen.blit(ship.image, ship.rect)
            camera.update(player)
            # обновляем положение всех спрайтов
            for sprite in all_sprites:
                camera.apply(sprite)
            if k % 4 == 0:
                all_sprites.update(player.rect.x, player.rect.y)
            all_sprites.draw(screen)
            k += 1
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    level = load_level('level_1.map')
    print(level)
    player, level_x, level_y = generate_level(level)
    start_screen()
