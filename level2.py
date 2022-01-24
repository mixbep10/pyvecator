import os
import randomaser
import sys
import pygame


def level_2(load_image, generate_level, Tile, Fish, Player, terminate, end_level1, load_level, Camera, Particle, Ship, start_screen):
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
    Jump = False

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

    if __name__ == '__main__':
        level = load_level('level_1.map')
        print(level)
        player, level_x, level_y = generate_level(level)
        fish = Fish(0, 0)
        start_screen()
