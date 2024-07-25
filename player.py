import pygame
from pydantic import BaseModel, Field, PositiveInt

class Player(BaseModel):

    # Player Attributes
    x: PositiveInt
    y: PositiveInt
    width: PositiveInt
    height: PositiveInt
    color: tuple[int, int, int] = Field(default=(0,255,0))
    speed: PositiveInt = Field(default=5)
 
    # Draw Player
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

    # Move Player
    def move(self):
        self.x += self.speed
        self.y += self.speed


