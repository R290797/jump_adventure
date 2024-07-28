import pygame
from pydantic import BaseModel, Field, PositiveInt
from projectile_manager import Projectile_Manager

class Player(BaseModel):

    # Position Attributes
    x: PositiveInt
    y: PositiveInt
    width: PositiveInt
    height: PositiveInt
    color: tuple[int, int, int] = Field(default=(0,255,0))

    # Movement Attributes
    speed: float = Field(default=2.5)
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
    projectile_manager: Projectile_Manager = Projectile_Manager(shoot_cooldown=2)
    
    # Out of Bounds Attributes
    player_outofbounds: bool = Field(default=False)
 
    # Draw Player (And Return Rect. for Collision Detection)
    def draw_self(self, window):

        # Draw Player Rectangle
        return pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
           
    # Jump
    def jump(self):

        if self.can_jump:
            self.y_delta -= self.jump_height
            self.grounded = False
            self.can_jump = False

    # Shoot
    def shoot(self):
        self.projectile_manager.add_projectile(self.x, self.y, 5, 5)

    def check_jump(self):
        if self.grounded_buffer > 0:
            self.can_jump = True
        else:
            self.can_jump = False

    # Check if Player is Grounded (and Apply Gravity)
    def check_grounded(self):

        # Check if Player is Grounded
        if self.grounded:
            self.y_delta = 0

            # Reset Grounded Buffer
            self.grounded_buffer = 10
        else:
            # Gravity (Falling)
            self.y_delta += self.gravity
            self.y += self.y_delta
            self.grounded_buffer -= 1

            # Wrap Around Logic
    def wrap_around(self, screen_width):
        if self.x > screen_width:
            self.x = -self.width
        elif self.x + self.width < 0:
            self.x = screen_width

    # Update Player Movement
    def update(self, window):

        # Grounded Check
        self.check_grounded()

        # Move Player Horizontally
        self.x += self.x_delta * self.speed

        # Manage Projectiles
        self.projectile_manager.render_projectiles(window)
        self.projectile_manager.manage_projectiles(window)

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
    def platform_collision(self, plat_rect_list):

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
            
                
