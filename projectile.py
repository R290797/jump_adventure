import pygame
from pydantic import BaseModel, Field, PositiveInt

class Projectile(BaseModel):
    
    # Position Attributes
    x: int
    y: int
    width: PositiveInt
    height: PositiveInt

    # Movement Attributes
    speed: PositiveInt = Field(default=5)
    x_delta: int = Field(default=0)
    y_delta: int = Field(default=-1)

    def draw(self, window):
        return pygame.draw.rect(window, (255,0,0), (self.x, self.y, self.width, self.height))
    
    def move(self):
        self.x += self.x_delta * self.speed
        self.y += self.y_delta * self.speed

    


