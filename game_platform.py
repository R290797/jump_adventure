import pygame
import random
from pydantic import BaseModel, Field, PositiveInt

class Platform(BaseModel):

    # Platform Attributes
    x: int
    y: int
    width: PositiveInt
    height: PositiveInt
    color: tuple[int, int, int] = Field(default=(0,0,255))
    vert_speed: int = Field(default=1)
    horz_speed: int = Field(default=0)
    radius: PositiveInt = Field(default=10)

    # Status Attributes
    type: str = "base"
   
    # Draw Platform
    def draw(self, window):
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, self.color, (0, 0, self.width, self.height), border_radius=self.radius)
        window.blit(surface, (self.x, self.y))
        return pygame.Rect(self.x, self.y, self.width, self.height)

    # Move Platform Down
    def move(self):
        self.y += self.vert_speed

    # Function to Get Collision Rect
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)



# Platform Variations

#Horizontal Platform
class Horizontal_Platform(Platform):

    # New Attributes / Overwrite Type
    direction : int = Field(default=0)
    type: str = "horizontal"

    #Horizontal Platform Changing Direction             
    def move(self):
        self.x += self.horz_speed * self.direction 
        if self.x <= 0:
            self.x = 0
            self.direction = 1  
        elif self.x + self.width >= 1000:
            self.x = 1000 - self.width
            self.direction = -1 
        super().move() 
        
# Falling Platforms
class Falling_Platform(Platform):

    # Overwrite Type
    type: str = "falling"

    def move(self):
        self.y += self.vert_speed*2
            
# Disapearing Platforms            
class Disappearing_Platform(Platform):

    # Overwrite Type
    type: str = "disappearing"

    # Add Unique Attributes
    first_touch: bool = Field(default=False)

    # Set Funciton for First Touch
    def set_first_touch(self):
        self.first_touch = True

