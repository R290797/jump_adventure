from pydantic import BaseModel, Field, PositiveInt
from player import Player
import pygame
import random

class Base_Enemy(BaseModel):

    # Position Attributes
    x: int 
    y: int 
    width: PositiveInt = Field(default=25)
    height: PositiveInt = Field(default=25)
    color: tuple[int, int, int] = Field(default=(255,0,0))

    # Movement Attributes
    vert_speed: int = Field(default=1)
    horz_speed: int = Field(default=1)
    direction: int = random.choice([-1,1])

    # Draw the Enemy, Return Rect object for Collision Calculations
    def draw(self, screen: pygame.Surface) -> pygame.rect:
        return pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    # Movement of the Enemy (Base Movement is Bouncing/Left Right and constantly moving Down)
    def move(self, player: Player, screen: pygame.Surface):

        # Move Enemy Down
        self.y += self.vert_speed

        # Move Enemy Horizontally (Switch Directions When hitting the Side)
        if self.x > screen.get_width() or self.x < 0:
            self.direction *= -1

        self.x += self.horz_speed * self.direction

