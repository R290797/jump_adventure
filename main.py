# Import Modules
import pygame

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
def event_handler():

    # Iterate Through Pygame Events
    for event in pygame.event.get():

        # Running False when Quit Event (Press Red X)
        if event.type == pygame.QUIT:
            global running 
            running = False


# Player
player = Player(x=50, y=50, width=50, height=50, color=colors["green"], speed=5)

# TODO: Create Platform Spawner/List Class
# Platforms (Temporary)
platform_1 = Platform(x=300, y=400, width=100, height=5, color=colors["blue"], down_speed=1)
platform_2 = Platform(x=400, y=300, width=100, height=5, color=colors["blue"], down_speed=1)
platform_3 = Platform(x=500, y=200, width=100, height=5, color=colors["blue"], down_speed=1)

# Platform List (Temporary)
platform_list = [platform_1, platform_2, platform_3]

# Game Loop
running = True
while running:

    # Tick Game
    timer.tick(fps)

    # Fill Screen (Order Matters - Items Drawn in Order from Back to Front)
    window.fill(colors["white"])

    # Draw Actors
    player.draw(window)

    # Render Plartforms
    for plat in platform_list:
        plat.draw(window)


    # Event Handler
    event_handler()

    # Update Display
    pygame.display.flip()


pygame.quit()