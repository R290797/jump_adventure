# Import Modules
import pygame
import time
import random
import sys 


# Import Classes
from player import Player
from platform_manager import Platform_Manager
from enemy_manager import Enemy_Manager
from boost_items import BoostItem, BoostItemManager
from menu import Menu


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
    "purple": (128, 0, 128)
    }

screen_width = 1000
screen_height = 700
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

# Event Handler (For User Inputs) 
def event_handler(menu_active):
    global running
    global player

    # Iterate Through Pygame Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if menu_active:
            menu.handle_input(event)
        else:
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

# Create Menu Object
menu = Menu(window, font, colors) 

# Create Player Object
player = Player(x=50, y=50, width=50, height=50, color=colors["green"], speed=3, jump_height=20, gravity=1)

# Create Platform Manager
platform_manager = Platform_Manager()

# Create Enemy Manager
enemy_manager = Enemy_Manager(player_x=player.x, player_y=player.y, spawn_rate=5.0)

# Create Boost Item Manager
boost_item_manager = BoostItemManager(screen_width, screen_height, player)

# Game Loop
running = True
menu_active = True 
game_over = False
start_time = time.time()
final_time = 0  

while running:
  
    if menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            menu.handle_input(event)  
        menu.draw()  
        if menu.start_game(): 
            menu_active = False
            
    else:
       # Pygame Variables
      timer.tick(fps)
      window.fill((255, 255, 255))
      plat_rect_list = []

          if not game_over:
              # Render Actors
              player.draw_self(window)

              # Manage Platforms
              platform_manager.manage_platforms(window, colors)

              # Manage Enemies
              enemy_manager.manage_enemies(window)

              # Update Player position for Enemey Location
              enemy_manager.player_x = player.x + (player.width//2)
              enemy_manager.player_y = player.y + (player.height//2)

              # Collision Detection
              player.platform_collision(platform_manager.rect_list)
              player.enemy_collision(enemy_manager)

              # Update Actors and Check for Game Over (TODO: Summarize in Function)
              player.update(window, enemy_manager)

              # Spawn items at random intervals
              if random.random() < 0.01:  # Adjust frequency as needed
                  boost_item_manager.spawn_item()

              # Update and draw boost items
              boost_item_manager.update_items()
              boost_item_manager.draw_items(window)

               # Capture the time at game over 
              if not player.alive:
                  final_time = time.time() - start_time
                  game_over = True

          # Display the Timer/Score
          elapsed_time = final_time if game_over else time.time() - start_time
          score_text = f"Score: {int(elapsed_time)}"

         # Positioned near upper right corner 
          render_text(score_text, font, colors["black"], 
                      window, screen_width-915, 20) 

          # Debug - Show Grounded Status
          grounded_status = f"jump: {player.can_jump}"
          render_text(grounded_status, font, colors["black"], window, screen_width-900, 50)

          # Debug - Show Shooting
          grounded_status = f"Shoot: {time.time() - player.projectile_manager.last_shot > player.projectile_manager.shoot_cooldown}"
          render_text(grounded_status, font, colors["black"], window, screen_width-900, 80)

          # Debug - Show Enemy Count
          grounded_status = f"Enemies: {len(enemy_manager.enemy_list)}"
          render_text(grounded_status, font, colors["black"], window, screen_width-900, 110)

          if game_over:
              render_text("Game Over", font, colors["red"], window, screen_width / 2, screen_height / 2)

        # Event Handler
        event_handler(menu_active)  

        # Update Display
        pygame.display.flip()


pygame.quit()
