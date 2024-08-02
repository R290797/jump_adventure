import time
import pygame
import sys
from pydantic import BaseModel
from platform_manager import Platform_Manager
from enemy_manager import Enemy_Manager
from player import Player

pygame.init()
pygame.mixer.init()
timer = pygame.time.Clock()
window = pygame.display.set_mode((1000, 700))
empty_p_manager = Platform_Manager(spawn_rate=100)
player = Player(
    power_sound=pygame.mixer.Sound("Resources/Sounds/WoodHit-SoundEffect.wav"),
    hit_sound=pygame.mixer.Sound("Resources/Sounds/EnemyImpact-SoundEffect.wav"),
    break_sound=pygame.mixer.Sound("Resources/Sounds/WoodHit-SoundEffect.wav"),
)
empty_e_manager = Enemy_Manager(player_x=player.x, player_y=player.y, spawn_rate=1000)


def render_platform_images(screen: pygame.surface, platform_manager: Platform_Manager):
    temp_image = None

    image_path_dict = {
        "base": "Resources/Sprites/Sprite-normal_log.png",
        "horizontal": "Resources/Sprites/Sprite-moving_log.png",
        "falling": "Resources/Sprites/Sprite-falling_log.png",
        "disappearing": "Resources/Sprites/Sprite-breaking_log.png",
    }

    for plat in platform_manager.platform_list:

        temp_image = pygame.image.load(image_path_dict[plat.type])
        temp_image = pygame.transform.scale(temp_image, (plat.width, plat.height))
        screen.blit(temp_image, (plat.x, plat.y))


# Event Handler
def event_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()



# Test Platform Spawn
def test_platform_spawn():

    platform_manager = Platform_Manager()
    start_time = time.time()
    event_handler()

    while True:

        window.fill((255, 255, 255))
        timer.tick(60)
        platform_manager.manage_platforms(window, (255, 255, 255))
        render_platform_images(window, platform_manager)

        if time.time() - start_time > 5.0:
            break

        pygame.display.flip()

    assert len(platform_manager.platform_list) > 1


# Test Platforms Despawn leaving Bottom
def test_platform_despawn():
    platform_manager = Platform_Manager(spawn_rate=5, vert_speed=10)
    start_time = time.time()
    event_handler()

    while True:

        window.fill((255, 255, 255))
        timer.tick(60)
        platform_manager.manage_platforms(window, (255, 255, 255))
        render_platform_images(window, platform_manager)

        if time.time() - start_time > 5.0:
            break

        pygame.display.flip()

    assert len(platform_manager.platform_list) == 1


# Test Player Dies When Leaving Screen
def test_player_dies_off_Screen():
    start_time = time.time()
    event_handler()
    player.x = 440
    player.y = 50

    while True:

        window.fill((255, 255, 255))
        timer.tick(60)
        player.update(window, empty_e_manager)
        player.draw_self(window)

        if time.time() - start_time > 3.0 or not player.alive:
            break

        pygame.display.flip()

    assert not player.alive


# Test Player Wraps When Going Around the Screen
def test_player_wraps():
    start_time = time.time()
    event_handler()
    player.x = 440  # Starting x value as reference
    player.y = 50

    while True:

        window.fill((255, 255, 255))
        timer.tick(60)
        player.update(window, empty_e_manager)
        player.draw_self(window)
        player.y_delta = 0
        player.x_delta = 5

        if (player.x < 300 and player.x > 200) or time.time() - start_time > 10:
            break

        pygame.display.flip()

    assert player.x < 400