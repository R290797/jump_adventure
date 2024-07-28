# Import Modules
import pygame
import time

# Import Classes
from player import Player
from game_platform import Platform
from platform_manager import Platform_Manager

# TODO: From Tutotrial (Update these Later) - Check Requirements

# PYGAME SETUP
#_______________________________________________________________________________________________________________________

# Initialize Pygame
pygame.init()

# Color Dictionary
colors = {
    "black": (0, 0, 0),
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

screen_width = 800
screen_height = 600
fps = 60

# Pygame Tools
timer = pygame.time.Clock()

# Screen
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jump Adventure")


# Font for Game Over Text
font = pygame.font.SysFont(None, 55)

# FUNCTIONS
#_______________________________________________________________________________________________________________________
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

            if event.key == pygame.K_UP:
                player.shoot()

            if event.key == pygame.K_q:
                running = False

        # Key Releases
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT:
                player.x_delta += player.speed

            if event.key == pygame.K_RIGHT:
                player.x_delta -= player.speed

# Create and Render Text on the Screen
def render_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


#GAME SETUP
#_______________________________________________________________________________________________________________________


# Creaste Player Object
player = Player(x=50, y=50, width=50, height=50, color=colors["green"], speed=2.5, jump_height=20, gravity=1)

# TODO: Create Platform Spawner/List Class

# Create Platform Manager
platform_manager = Platform_Manager()

# Game Loop
running = True
game_over = False
start_time = time.time()
final_time = 0  

while running:

    # Pygame Variables
    timer.tick(fps)
    window.fill((255, 255, 255))
    plat_rect_list = []

    if not game_over:
        # Render Actors
        player.draw_self(window)

        # Manage Platforms
        platform_manager.manage_platforms(window, colors, timer)

        # Collision Detection
        player.platform_collision(platform_manager.rect_list)

        # Update Actors and Check for Game Over (TODO: Summarize in Function)
        player.update(window)

         # Capture the time at game over 
        if player.player_outofbounds:
            final_time = time.time() - start_time
            game_over = True

    # Display the Timer/Score
    elapsed_time = final_time if game_over else time.time() - start_time
    score_text = f"Score: {int(elapsed_time)}"

   # Positioned near upper right corner 
    render_text(score_text, font, colors["black"], 
                window, screen_width-715, 20) 
    
    # Debug - Show Platform Count
    platform_count = f"Plats: {len(platform_manager.platform_list)}"
    render_text(platform_count, font, colors["black"], window, screen_width-715, 50)

    # Debug - Show Grounded Status
    grounded_status = f"jump: {player.can_jump}"
    render_text(grounded_status, font, colors["black"], window, screen_width-715, 80)

    
    if game_over:
        render_text("Game Over", font, colors["red"], window, screen_width / 2, screen_height / 2)


    # Event Handler
    event_handler()

    # Update Display
    pygame.display.flip()

pygame.quit()

