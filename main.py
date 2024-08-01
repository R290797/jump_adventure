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
from background import Background


# TODO: From Tutotrial (Update these Later) - Check Requirements

# PYGAME SETUP
#_______________________________________________________________________________________________________________________

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

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

# Screen Variables
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jump Adventure")


# Background Objects
background_1 = Background(y=0, path="Resources/Sprites/Sprite-background_1.png", screen=window, moving=False)
background_2 = Background(y=-700, path="Resources/Sprites/Sprite-background_2.png", screen=window, moving=False)
background_3 = Background(y=700, path="Resources/Sprites/Sprite-background_3.png", screen=window, moving=False)
background_list = [background_1, background_2, background_3]

# Font Variables
font = pygame.font.SysFont(None, 55)
font_medium = pygame.font.SysFont(None, 30)
font_small = pygame.font.SysFont(None, 20)

# The following code inspried by a guide found on The Python Code
# 'How to Add Sound Effects to your Python Game' by Michael Maranan
# Available at: https://thepythoncode.com/article/add-sound-effects-to-python-game-with-pygame 
    # Load Sound Effects
jump_sound = pygame.mixer.Sound("SoundEffects/Jump-SoundEffect.wav") # Royalty Free Music: https://mixkit.co/
shoot_sound = pygame.mixer.Sound("SoundEffects/Shoot-SoundEffect.wav") # Royalty Free Music: https://mixkit.co/
power_sound = pygame.mixer.Sound("SoundEffects/PowerUp-SoundEffect.wav") # Royalty Free Music: https://mixkit.co/
game_over_sound = pygame.mixer.Sound("SoundEffects/GameOver-SoundEffect.wav") # Royalty Free Music: https://mixkit.co/

    # Load Game Play Music
game_play_music = "SoundEffects/GamePlay-SoundEffect.mp3" # Royalty Free Music: https://www.bensound.com/
pygame.mixer.music.load(game_play_music)


# FUNCTIONS
#_______________________________________________________________________________________________________________________

# Event Handler (For User Inputs) 
def event_handler(menu_active, game_over):
    global running
    global player

    # Iterate Through Pygame Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if menu_active:
            menu.handle_input(event)

        # Reseting Game / Back to Menu / Quit at Game Over Screen
        elif not menu_active and game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    init_new_game(False)
                if event.key == pygame.K_m:
                    init_new_game(True)
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        else:
            # Key Presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                    jump_sound.play()

                if event.key == pygame.K_LEFT:
                    player.x_delta -= player.speed

                if event.key == pygame.K_RIGHT:
                    player.x_delta += player.speed

                if event.key == pygame.K_UP:
                    player.shoot()
                    shoot_sound.play()

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
    
    
# Check and Save High Score Function
def check_and_save_high_score(score,menu):
    if score > 0:
        menu.save_high_score(score)


# Render Player Image
def render_player_image(screen: pygame.surface):
    global player

    player_image = pygame.image.load("Resources/Sprites/monke1.png")
    player_image = pygame.transform.scale(player_image, (player.width, player.height))
    screen.blit(player_image, (player.x, player.y))

# Render Platform Images
def render_platform_images(screen: pygame.surface):
    global platform_manager
    temp_image = None

    image_path_dict = {"base": "Resources/Sprites/Sprite-normal_log.png",
                       "horizontal": "Resources/Sprites/Sprite-moving_log.png",
                        "falling":  "Resources/Sprites/Sprite-falling_log.png",
                        "disappearing": "Resources/Sprites/Sprite-breaking_log.png"}

    for plat in platform_manager.platform_list:

        temp_image = pygame.image.load(image_path_dict[plat.type])
        temp_image = pygame.transform.scale(temp_image, (plat.width, plat.height))
        screen.blit(temp_image,(plat.x, plat.y))

# Render Enemy Images
def render_enemy_images(screen: pygame.surface):
    global enemy_manager
    temp_image = None

    image_path_dict = {"base": "Resources/Sprites/Sprite-base_enemy.png",
                       "bounce": "Resources/Sprites/Sprite-bouncing_enemy.png",
                       "chase": "Resources/Sprites/Sprite-following_enemy.png"}
    
    for enemy in enemy_manager.enemy_list:

        temp_image = pygame.image.load(image_path_dict[enemy.type])
        temp_image = pygame.transform.scale(temp_image, (enemy.width, enemy.height))
        screen.blit(temp_image, (enemy.x, enemy.y))

def render_boost_images(screen: pygame.surface):
    global boost_item_manager
    temp_image = None

    image_path_dict = {"parachute": "Resources/Sprites/Sprite-parachute_powerup.png",
                       "double_jump": "Resources/Sprites/Sprite-double_jump_powerup.png",
                       "shield": "Resources/Sprites/Sprite-shield_powerup.png"}
    
    for boost in boost_item_manager.items:

        # Load Images and Scale
        temp_image = pygame.image.load(image_path_dict[boost.boost_type])
        temp_image = pygame.transform.scale(temp_image, (boost.width, boost.height))
        screen.blit(temp_image, (boost.x, boost.y))


# Render Moving Backround
def render_background(game_over: bool):

    for background in background_list:
        background.render()

        if game_over == False:
            background.move()


# Rendering all Game Images
def render_game_images(screen: pygame.surface):
    
    # Render Player
    render_player_image(window)

    # Render Platforoms
    render_platform_images(window)

    # Render Enemies
    render_enemy_images(window)

    # Render Booster Images
    render_boost_images(window)

    

# Rendering Background Image



#GAME SETUP
#_______________________________________________________________________________________________________________________

# Create Menu Object
menu = Menu(window, font, colors) 

# Create Player Object
player = Player(x=window.get_width()/2 - 25, y=30, width=60, height=60, color=colors["green"], speed=3, jump_height=20, gravity=1, power_sound=power_sound)

# Create Platform Manager
platform_manager = Platform_Manager()

# Create Enemy Manager
enemy_manager = Enemy_Manager(player_x=player.x, player_y=player.y)

# Create Boost Item Manager
boost_item_manager = BoostItemManager(screen_width, screen_height, player)

# Game Loop
running = True
game_over = False
start_time = time.time()
final_time = 0  

# Function to Reset / Start the Game
def init_new_game(menu_status: bool):

    # Get Global Variables
    global menu, game_over, start_time, final_time, player, platform_manager, enemy_manager, boost_item_manager

    # Return to Menu or not
    if menu_status:
        menu = Menu(window, font, colors) 
    
    # Reset Globals    
    game_over = False
    start_time = time.time()
    final_time = 0
    player = Player(x=window.get_width()/2 - 25, y=30, width=60, height=60, color=colors["green"], speed=3, jump_height=20, gravity=1, power_sound=power_sound)
    platform_manager = Platform_Manager()
    enemy_manager = Enemy_Manager(player_x=player.x, player_y=player.y)
    boost_item_manager = BoostItemManager(screen_width, screen_height, player)

while running:

    # Handle Menu Actions
    if menu.active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            menu.handle_input(event)  
        menu.draw()  

        # Start The Game
        if not menu.active: 
            init_new_game(False)
            pygame.mixer.music.play(-1)
            
    else:

        # Pygame Variables
        timer.tick(fps)
        window.fill((255, 255, 255))
        render_background(game_over)

        if not game_over:
            # Render Actors
            player.draw_self(window)

            # Update Player position for Enemey Location
            enemy_manager.player_x = player.x + (player.width//2)
            enemy_manager.player_y = player.y + (player.height//2)

            # Collision Detection
            player.handle_player_platforms(platform_manager, window)
            player.enemy_collision(enemy_manager)

            # Update Actors and Check for Game Over (TODO: Summarize in Function)
            player.update(window, enemy_manager)

            # Spawn items at random intervals
            if random.random() < 0.01:  # Adjust frequency as needed
                boost_item_manager.spawn_item()

            # Manage Platforms
            platform_manager.manage_platforms(window, colors)

            # Manage Enemies
            enemy_manager.manage_enemies(window)

            # Update and draw boost items
            boost_item_manager.update_items()
            boost_item_manager.draw_items(window)

            # Capture the time at game over 
            if not player.alive:
                final_time = time.time() - start_time
                game_over = True
                game_over_sound.play()

            # Render Images
            render_game_images(window)

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

        last_touch = f"LT: {player.last_touch_type}"
        render_text(last_touch, font, colors["black"], window, screen_width-900, 150)

        last_touch = f"plats: {len(platform_manager.platform_list)}"
        render_text(last_touch, font, colors["black"], window, screen_width-900, 180)

        if game_over:
            render_text("Game Over", font, colors["red"], window, screen_width / 2, screen_height / 2)

            check_and_save_high_score(int(elapsed_time), menu)
            render_text(f"Final Score: {int(elapsed_time)}", font_medium, colors["red"], window, screen_width / 2, (screen_height / 2) + 30)
            render_text("Press R to Reset, Press for Main Menu, Press Q to Quit", font_small, colors["black"], window, screen_width / 2, (screen_height / 2) + 50)

    # Event Handler
    event_handler(menu.active, game_over)  

    # Update Display
    pygame.display.flip()


pygame.quit()
