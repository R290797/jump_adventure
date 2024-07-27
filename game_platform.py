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
    down_speed: int = Field(default=1)
    radius: PositiveInt = Field(default=10)
   
    # Draw Platform
    def draw(self, window):
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, self.color, (0, 0, self.width, self.height), border_radius=self.radius)
        window.blit(surface, (self.x, self.y))
        return pygame.Rect(self.x, self.y, self.width, self.height)

    # Move Platform Down
    def move(self):
        self.y += self.down_speed
        self.x += self.horz_speed

# TODO: Platform Variations which Inherit from Platform Class
# Breaking, Moving, etc. Platforms