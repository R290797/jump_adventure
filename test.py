import time
import pygame
from platform_manager import Platform_Manager
from player import Player

pygame.init()
timer = pygame.time.Clock()
window = pygame.display.set_mode((1000, 700))

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
            pass

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
    pass

# Test Plaxer Wraps When Going Around the Screen

