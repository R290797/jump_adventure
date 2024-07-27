# Import Modules
import pygame
import random

# Import Classes
from player import Player
from game_platform import Platform


# TODO: From Tutotrial (Update these Later) - Check Requirements
#_______________________________________________________________________________________________________________________

# Initialize Pygame
pygame.init()

# Color Dictionary
colors = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "silver": (192, 192, 192),
    "gray": (128, 128, 128),
    "maroon": (128, 0, 0),
    "olive": (128, 128, 0),
    "purple": (128, 0, 128)}

# Pygame Configurations
screen_width = 800
screen_height = 600
fps = 60

# Pygame Tools
timer = pygame.time.Clock()

# Screen
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jump Adventure")

# Functions

# Event Handler (For User Inputs) TODO: Flatten (Move Movement Functions to Player Class)
def event_handler():
    global running 
    global player

    # Iterate Through Pygame Events
    for event in pygame.event.get():

        # Running False when Quit Event (Press Red X)
        if event.type == pygame.QUIT:
            running = False

        # Key Presses
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                player.jump()

            if event.key == pygame.K_LEFT:
                player.x_delta -= player.speed

            if event.key == pygame.K_RIGHT:
                player.x_delta += player.speed

            if event.key == pygame.K_q:
                running = False

        # Key Releases
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT:
                player.x_delta += player.speed

            if event.key == pygame.K_RIGHT:
                player.x_delta -= player.speed


# Player
player = Player(x=50, y=50, width=50, height=50, color=colors["green"], speed=5, jump_height=20, gravity=1)

# TODO: Create Platform Spawner/List Class
# Platforms (Temporary)
platform_1 = Platform(x=1, y=400, width=1000, height=5, color=colors["blue"], down_speed=1, radius=15)
platform_2 = Platform(x=400, y=300, width=100, height=5, color=colors["blue"], down_speed=1, radius=10)
platform_3 = Platform(x=500, y=200, width=100, height=5, color=colors["blue"], down_speed=1, radius=20)

# Platform List (Temporary)
platform_list = [platform_1, platform_2, platform_3]

# Game Loop
running = True

while running:

    # Pygame Variables
    timer.tick(fps)
    window.fill(colors["white"])
    plat_rect_list = []

    # Render Actors
    player.draw(window)

    # Collision Detection
    player.platform_collision(plat_rect_list)
    
    # Remove Platforms that are Off the Screen
    platform_list = [plat for plat in platform_list if plat.y < screen_height]

    # Update Actors (TODO: Summarize in Function)
    player.update()

    # Event Handler
    event_handler()

    # Update Display
    pygame.display.flip()


pygame.quit()