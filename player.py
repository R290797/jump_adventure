import pygame
from pydantic import BaseModel, Field, PositiveInt

class Player(BaseModel):

    # Player Attributes
    x: PositiveInt
    y: PositiveInt
    width: PositiveInt
    height: PositiveInt
    color: tuple[int, int, int] = Field(default=(0,255,0))

    # Movement Attributes
    speed: PositiveInt = Field(default=5)
    gravity: PositiveInt = Field(default=1)
    x_delta: int = Field(default=0)
    y_delta: int = Field(default=0)

    # Jump Mechnics
    grounded: bool = Field(default=False)
    can_jump: bool = Field(default=True)
    jump_height: PositiveInt = Field(default=10)

    # Grounded Buffer (Prevents inconsistent collision detection)
    grounded_buffer: int = Field(default=10)
    

    player_outofbounds: bool = Field(default=False)
 
    # Draw Player
    def draw(self, window):
        return pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
       
    # Jump
    def jump(self):

        if self.can_jump:
            self.y_delta -= self.jump_height
            self.grounded = False
            self.can_jump = False

    def check_jump(self):
        if self.grounded_buffer > 0:
            self.can_jump = True
        else:
            self.can_jump = False

    # Update Player Movement
    def update(self,screen_width, screen_height):

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

        # Move Player Horizontally
        self.x += self.x_delta

        # Handle wrap-around
        self.wrap_around(screen_width)

        # Check Jump
        self.check_jump()

        # Check for falling off the screen
        if self.y > screen_height + 100:
            self.player_outofbounds = True
        else:
            self.player_outofbounds = False

        # Wrap Around Logic
    def wrap_around(self, screen_width):
        if self.x > screen_width:
            self.x = -self.width
        elif self.x + self.width < 0:
            self.x = screen_width
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
            
                
