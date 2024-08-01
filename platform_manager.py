from game_platform import Platform, Horizontal_Platform, Falling_Platform, Disappearing_Platform
from pydantic import BaseModel, Field, PositiveInt
import random
import time
import pygame


class Platform_Manager(BaseModel):

    # Spawn Attributes
    spawn_rate: float = Field(default=1.0) # Time between platform spawns
    spawn_time: float = Field(default=time.time()) # Time since last platform spawn
    rect_list: list = Field(default=[])

    # Start With Base Platform
    platform_list: list = [Platform(x=1, y=100, width=1000, height=5, color=(0,255,0), down_speed=1, radius=15)]

    # Random Platform Spawn
    def spawn_platform(self,screen_width,colors):
        x = random.randint(0,screen_width -150)
        y = -100
        width = random.randint(50,150)
        height = 5
        vert_speed = 1
        horz_speed = random.randint(1, 5) 
        color = random.choice(list(colors.values()))
        
        platform_type = random.choices(
            [Platform,Horizontal_Platform,Falling_Platform, Disappearing_Platform],
            [0, 0.5, 0, 0.5]
        )[0]

        if platform_type == Horizontal_Platform:
            return Horizontal_Platform(x=x, y=y, width=width, height=height, color=color, horz_speed=horz_speed, direction=random.choice([-1, 1]))
        elif platform_type == Falling_Platform:
            return Falling_Platform(x=x, y=y, width=width, height=height, color=color, vert_speed=vert_speed)
        elif platform_type == Disappearing_Platform:
            return Disappearing_Platform(x=x, y=y, width=width, height=height, color=color)
        else:
            return Platform(x=x, y=y, width=width, height=height, color=color, vert_speed=vert_speed)
    
    # Render Platforms
    def render_platforms(self,window):

        # Reset Rect List
        self.rect_list = []

        for plat in self.platform_list:

            # Add Platform Rectangles to List (For Collision Detection)
            self.rect_list.append(plat.draw(window))

    # Remove out of Bounds Platforms
    def remove_platforms(self, window: pygame.surface):

        for plat in self.platform_list:
            if plat.y > window.get_height() + 10:
                self.platform_list.remove(plat)

    # Update Platform Manager
    def manage_platforms(self, window, colors):

        # Move Platforms
        for plat in self.platform_list:
            plat.move()

        # Render Platforms
        self.render_platforms(window)
        
        # Spawn Platform at Spawn Rate Intervals (TODO: Add Platform Variations - Done)
        if time.time() - self.spawn_time > self.spawn_rate:
            self.platform_list.append(self.spawn_platform(window.get_width(), colors))

            # Reset Spawn Time
            self.spawn_time = time.time()

        # remove out of bounds Platforms
        self.remove_platforms(window)
