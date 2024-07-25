import pygame
from pydantic import BaseModel, Field, PositiveInt

class Platform(BaseModel):

    # Platform Attributes
    x: PositiveInt
    y: PositiveInt
    width: PositiveInt
    height: PositiveInt
    color: tuple[int, int, int] = Field(default=(0,0,255))
    vert_speed: PositiveInt = Field(default=1)
    horz_speed: PositiveInt = Field(default=0)
   
    # Draw Platform
    def draw(self, window):
        return pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

    # Move Platform Down
    def move(self):
        self.y += self.down_speed
        self.x += self.horz_speed

# TODO: Platform Variations which Inherit from Platform Class
# Breaking, Moving, etc. Platforms