import pygame
from pydantic import BaseModel, Field, PositiveInt
from projectile_manager import Projectile_Manager
from enemy_manager import Enemy_Manager

class Player(BaseModel):

    # Position Attributes
    x: int
    y: int
    width: PositiveInt
    height: PositiveInt
    color: tuple[int, int, int] = Field(default=(0,255,0))

    # Movement Attributes
    speed: int = Field(default=2)
    gravity: PositiveInt = Field(default=1)
    x_delta: int = Field(default=0)
    y_delta: int = Field(default=0)

    # Jump Mechnics
    grounded: bool = Field(default=False)
    can_jump: bool = Field(default=True)
    jump_height: PositiveInt = Field(default=10)

    # Grounded Buffer (Prevents inconsistent collision detection)
    grounded_buffer: int = Field(default=10)

    # Shooting Mechanic
    projectile_manager: Projectile_Manager = Projectile_Manager(shoot_cooldown=1)
    
    # Out of Bounds Attributes
    player_outofbounds: bool = Field(default=False)
    player_enemy_collision: bool = Field(default=False)
 
    # Draw Player (And Return Rect. for Collision Detection)
    def draw_self(self, window):

        # Draw Player Rectangle and Return Rect
        return pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
           
    # Jump
    def jump(self):

        if self.can_jump:
            self.y_delta -= self.jump_height
            self.grounded = False
            self.can_jump = False

    # Shoot
    def shoot(self):

        # Spawn Projectiles at the Center of the  Player
        self.projectile_manager.add_projectile(self.x + (self.width//2), self.y + (self.height//2), 5, 5, 5)

    # Check if Player is Grounded (and Apply Gravity)
    def check_grounded(self):

        # Check if Player is Grounded
        if self.grounded:
            self.y_delta = 0

            # Reset Grounded Buffer
            self.grounded_buffer = 10
        else:
            # Gravity (Falling), Player is not Grounded
            self.y_delta += self.gravity
            self.y += self.y_delta
            self.grounded_buffer -= 1

    # If Grounded Buffer Runs out, Jump Becomes Unavailable
    def check_jump(self):
        if self.grounded_buffer > 0:
            self.can_jump = True
        else:
            self.can_jump = False

    # Wrap Around Logic
    def wrap_around(self, screen_width):
        if self.x > screen_width:
            self.x = -self.width
        elif self.x + self.width < 0:
            self.x = screen_width

    # Manage Shooting Mechanic
    def manage_player_attack(self, window):

         # Render Projectiles
        self.projectile_manager.render_projectiles(window)

        # Manage Projectiles (Movement and Despawning)
        self.projectile_manager.manage_projectiles(window)


    # Update Player Movement
    def update(self, window):

        # Grounded Check
        self.check_grounded()

        # Move Player Horizontally
        self.x += self.x_delta * self.speed

        # Manage Player Attack (Shooting)
        self.manage_player_attack(window)

        # Handle wrap-around
        self.wrap_around(window.get_width())

        # Check Jump
        self.check_jump()

        # Check for falling off the screen
        if self.y > window.get_height() + 100:
            self.player_outofbounds = True
        else:
            self.player_outofbounds = False



    # Collision Detection

    # Player/Platform Collision
    def platform_collision(self, plat_rect_list: list):

        self.grounded = False

        # Iterate Through Platform Rectangles
        for i in range(len(plat_rect_list)):

            # Check if Player Rect Collides with Platform Rect
            if plat_rect_list[i].colliderect(self.x, self.y, self.width, self.height):

                # Check if Player y speed is positive (Falling)
                if self.y_delta >= 0 and self.grounded == False:

                    # Set Player Grounded
                    self.grounded = True
                    break

    # Player/Enemy Collision (Destroy Enemy if Coming From the Top - Falling)
    def enemy_collision(self, enemy_manager: Enemy_Manager): 

        # Iterate Rects (Go by Index to Find According enemy in Enemy List)
        for i in range(len(enemy_manager.rect_list)):

            # Check if Player Collides With Enemy
            if enemy_manager.rect_list[i].colliderect(self.x, self.y, self.width, self.height):

                # Check if Player is Falling (Not Stationary)
                if self.y_delta > 0:

                    # Destroy that Enemy (Set Alive to 0)
                    enemy_manager.enemy_list[i].alive = False
                    
                    # Make Player Jump
                    self.y_delta = -self.jump_height



            
                
