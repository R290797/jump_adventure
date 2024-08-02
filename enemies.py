from pydantic import BaseModel, Field, PositiveInt
import pygame
import random
import math


class Base_Enemy(BaseModel):

    # Position Attributes
    x: int
    y: int
    width: PositiveInt = Field(default=60)
    height: PositiveInt = Field(default=40)
    color: tuple[int, int, int] = Field(default=(255, 0, 0))

    # Movement Attributes
    vert_speed: int = Field(default=1)
    horz_speed: int = Field(default=1)
    direction: int = random.choice([-1, 1])

    # Status Attributes
    alive: bool = Field(default=True)
    type: str = "base"

    # Draw the Enemy, Return Rect object for Collision Calculations
    def draw(self, screen: pygame.Surface) -> pygame.rect:
        return pygame.draw.rect(
            screen, self.color, (self.x, self.y, self.width, self.height)
        )

    # Check if "Alive Conditions" of enemy are met, if not, return false
    def out_of_bounds_check(self, screen: pygame.surface):

        # If enemy Leaves Screen, Set alive to False
        if self.y > screen.get_height() + 30:
            self.alive = False

    # Movement of the Enemy (Base Movement is Bouncing/Left Right and constantly moving Down)
    def move(self, screen, px_pos: int, py_pos: int):

        # Move Enemy Down
        self.y += self.vert_speed

        # Move Enemy Horizontally (Switch Directions When hitting the Side)
        if self.x > screen.get_width() or self.x <= 0:
            self.direction *= -1

        self.x += self.horz_speed * self.direction

        # Check if Enemy is Out of Bounds
        self.out_of_bounds_check(screen)

    # Function to Get Collision Rect
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


# Enemy Variants


# Enemy Which Bounces of the Top and Bottom as Well
class Bouncing_Enemy(Base_Enemy):

    x_direction: int = random.choice([-1, 1])
    y_direction: int = random.choice([-1, 1])
    type: str = "bounce"

    # Movement Logic of Bouncing Enemy
    def move(self, screen: pygame.surface, px_pos: int, py_pos: int):

        # If enemy Touches the Top of the Screen, move it down
        if self.y < 0:
            self.y_direction = 1

        # If enemy Touches the bottom of the screen, move it up
        if self.y > screen.get_height():
            self.y_direction = -1

        # Move Enemy Horizontally (Switch Directions When hitting the Side)
        if self.x > screen.get_width() or self.x < 0:
            self.x_direction *= -1

        # Move Horizontal and Vertically
        self.x += self.horz_speed * self.x_direction * 2
        self.y += self.vert_speed * self.y_direction * 2


# Enemy Which Chases and Tracks the (Enemy Can Only Be Shot)
class Chasing_Enemy(Base_Enemy):

    x_direction: int = Field(default=0)
    y_direction: int = Field(default=0)
    type: str = "chase"

    # Track Player movement on a single axis (Referenced:  Reference: https://stackoverflow.com/questions/20044791/how-to-make-an-enemy-follow-the-player-in-pygame)
    def get_movement_vector(self, px_pos: int, py_pos):

        # Calculate Distance Vector to Player
        delta_x = px_pos - self.x
        delta_y = py_pos - self.y
        distance = math.hypot(delta_x, delta_y)
        return delta_x / distance, delta_y / distance

    def move(self, screen: pygame.surface, px_pos: int, py_pos: int):

        dx, dy = self.get_movement_vector(px_pos, py_pos)
        self.x += self.horz_speed * dx
        self.y += self.vert_speed * dy
