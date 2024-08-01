from pydantic import BaseModel, Field, PositiveInt
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

    # Status Attributes
    alive: bool = Field(default = True)

    # Draw the Enemy, Return Rect object for Collision Calculations
    def draw(self, screen: pygame.Surface) -> pygame.rect:
        return pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
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


# Enemy Variants

# Enemy Which Bounces of the Top and Bottom as Well
class Bouncing_Enemy(Base_Enemy):

    x_direction: int = random.choice([-1,1])
    y_direction: int = random.choice([-1,1])

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

    # Track Player movement on a single axis
    def track_x(self, px_pos: int):
        
        if px_pos > self.x:
            self.x_direction = 1
        elif px_pos < self.x:
            self.x_direction = -1
        else:
            self.x_direction = 0
        
    def track_y(self, py_pos: int):

        if py_pos > self.y:
            self.y_direction = 1
        elif py_pos < self.y:
            self.y_direction = -1
        else:
            self.y_direction = 0

    def move(self, screen: pygame.surface, px_pos: int, py_pos: int):

        # Track Player Movement
        self.track_x(px_pos)
        self.track_y(py_pos)

        # Move Enemy Accordingly
        self.x += self.horz_speed * self.x_direction
        self.y += self.vert_speed * self.y_direction * 2

