import os
import random
import sys
import pygame

from level2 import level_2

FPS = 90
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
jump_max = 20
jump_count = 0
Health = 9
Jump = False
cam_speed = -6
cat_color = 'Рыжий'
k = 1.2


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
fish = None

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}

tile_width = 200
tile_height = 55


def generate_level(level):
    new_player, fish, x, y = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '$':
                Enemy(x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y + 370)
                fish = Fish(x, y)

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = pygame.transform.scale(load_image('dog.png'), (150, 100))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y + 370)


class Wardrobe():
    def __init__(self):
        self.width = 250
        self.height = 70
        self.inactive_color = (102, 0, 255)
        self.active_color = (140, 0, 255)

    def draw(self, x, y, message, font, action=None):
        global wardrobe
        mouse = pygame.mouse.get_pos()
        if x < mouse[0] < (x + self.width):
            if y < mouse[1] < (y + self.height):
                pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))
        btn_text = font.render(message, 1, pygame.Color('black'))
        screen.blit(btn_text, (x + 45, y + 15))
        action = True

    def clicked(self, x, y, action=None):
        mouse = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        if x < mouse[0] < (x + self.width):
            if y < mouse[1] < (y + self.height):
                if clicked[0] == 1 and action is None:
                    return True


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y + 400)


class Fish(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = pygame.transform.scale(load_image('fish.png'), (75, 50))
        self.rect = self.image.get_rect().move(len(level[0]) * tile_width - 400, 400)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        if cat_color == 'Чёрный':
            self.image = load_image('cat_anim.png')
        else:
            self.image = load_image('cat_anim2.png')
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
        if Jump is False:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        player.rect.x += 24


def terminate():
    pygame.quit()
    sys.exit()


def end_level():
    level = load_level('level_2.map')
    print(level)
    player, level_x, level_y = generate_level(level)
    fish = Fish(0, 0)
    player.kill()
    start_screen()
    terminate


def end_level1():
    intro_text = ["Отлично!", "",
                  "Уровень",
                  "успешно пройден!",
                  "если готовы продолжить,",
                  "нажмите любую кнопку"]

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
    Jump = False
    while True:
        if k == 1000:
            k = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif (event.type == pygame.KEYDOWN or \
                  event.type == pygame.MOUSEBUTTONDOWN) and game_begin is False:
                end_level()
                cam_speed = cam_speed * 16
                level = load_level('level_2.map')
                print(level)
                player, level_x, level_y = generate_level(level)
                fish = Fish(0, 0)
                start_screen()

        pygame.display.flip()
        clock.tick(FPS)
    terminate


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
        self.dx = cam_speed
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
    def __init__(self, image_file, location, ):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/' + image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def start_screen():
    global Jump, jump_count, cat_color
    start_btn = Wardrobe()
    color1 = Wardrobe()
    color2 = Wardrobe()
    cat_color = 'Чёрный'
    intro_text = ["ЗАГРУЗКА2", "",
                  "Правила игры",
                  "Кот бежит по крыше",
                  "уворачивайтесь от препятствий посредством прыжка",
                  "Удачи!"]

    fon = pygame.transform.scale(load_image('unnamed.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
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
    fish = Fish(0, 0)

    while True:
        col_label = font.render(f'Цвет кота: {cat_color}', 1, pygame.Color('black'))
        screen.blit(col_label, (750, 300))
        start_btn.draw(400, 650, 'Старт', font)
        color1.draw(750, 200, 'Чёрный', font)
        color2.draw(750, 400, 'Рыжий', font)
        if color1.clicked(750, 200):
            cat_color = 'Чёрный'
        if color2.clicked(750, 400):
            cat_color = 'Рыжий'
        if start_btn.clicked(400, 700) is True:
            if k == 1000:
                k = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif (event.type == pygame.KEYDOWN or \
                  event.type == pygame.MOUSEBUTTONDOWN) and game_begin is False and start_btn.clicked(400, 700) is True:
                game_begin = True


            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                sound_jump_up = pygame.mixer.Sound(jump_1)
                if Jump is False:
                    pygame.mixer.music.pause()
                    sound_jump_up.play()
                    pygame.mixer.music.unpause()
                    Jump = True
                    jump_count = jump_max

        if game_begin:
            if fish.rect.x <= 0:
                end_level1()
            if Jump is True:
                player.image = load_image('cat_jumped.png')
                player.rect.y -= jump_count
                if jump_count > -jump_max:
                    jump_count -= 1
                else:
                    Jump = False
            screen.fill('white')

            screen.blit(ship.image, ship.rect)
            camera.update(player)
            # обновляем положение всех спрайтов
            for sprite in all_sprites:
                camera.apply(sprite)
            if k % 4 == 0:
                all_sprites.update(player.rect.x, player.rect.y)
            all_sprites.draw(screen)
            k += 1
            health_counter = font.render(f'Жизни: {Health}', False, 'black')
            screen.blit(health_counter, (850, 50))
        pygame.display.flip()
        clock.tick(FPS)


k = k ** 2
cam_speed = cam_speed

if __name__ == '__main__':
    level = load_level('level_1.map')
    print(level)
    player, level_x, level_y = generate_level(level)
    fish = Fish(0, 0)
    start_screen()
