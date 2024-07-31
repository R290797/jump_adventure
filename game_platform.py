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
   
    # Draw Platform
    def draw(self, window):
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, self.color, (0, 0, self.width, self.height), border_radius=self.radius)
        window.blit(surface, (self.x, self.y))
        return pygame.Rect(self.x, self.y, self.width, self.height)

    # Move Platform Down
    def move(self):
        self.y += self.vert_speed


# Platform Variations

#Horizontal Platform
class Horizontal_Platform(Platform):
    direction : int = Field(default=0)
    
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
    def move(self):
        self.y += self.vert_speed
            
# Disapearing Platforms            