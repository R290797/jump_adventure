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
    jump_height: PositiveInt = Field(default=10)
    gravity: PositiveInt = Field(default=1)
    grounded: bool = Field(default=False)
    x_delta: int = Field(default=0)
    y_delta: int = Field(default=0)

    player_outofbounds: bool = Field(default=False)
 
    # Draw Player
    def draw(self, window):
        return pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
       
    # Jump
    def jump(self):

        if self.grounded:
            self.y_delta -= self.jump_height
            self.grounded = False

    # Update Player Movement
    def update(self,screen_width, screen_height):

        # Check if Player is Grounded
        if self.grounded:
            self.y_delta = 0
        else:
            # Gravity (Falling)
            self.y_delta += self.gravity
            self.y += self.y_delta

        # Move Player Horizontally
        self.x += self.x_delta

        # Handle wrap-around
        self.wrap_around(screen_width)

        # Check for falling off the screen
        if self.y > screen_height:
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
            if plat_rect_list[i].colliderect(self.x, self.y + 5, self.width, self.height):

                # Check if Player y speed is positive (Falling)
                if self.y_delta >= 0 and self.grounded == False:

                    # Set Player Grounded
                    self.grounded = True
