from game_platform import Platform
from pydantic import BaseModel, Field, PositiveInt
import random
import time


class Platform_Manager(BaseModel):

    spawn_rate: PositiveInt = Field(default=1) # Time between platform spawns
    spawn_time: float = Field(default=time.time()) # Time since last platform spawn
    rect_list: list = Field(default=[])

    # Start With Base Platform
    platform_list: list = [Platform(x=1, y=200, width=1000, height=5, color=(0,255,0), down_speed=1, radius=15)]

    # Random Platform Spawn
    def spawn_platform(self,screen_width,colors):
        x = random.randint(0,screen_width)
        y = random.randint(1,50)
        width = random.randint(50,150)
        height = 5
        down_speed = random.randint(1,2)
        color = random.choice(list(colors.values()))
        return Platform(x=x,y=y,width=width,height=height,color=color,down_speed=down_speed)
    
    # Render Platforms
    def render_platforms(self,window):

        # Reset Rect List
        self.rect_list = []

        for plat in self.platform_list:

            # Add Platform Rectangles to List (For Collision Detection)
            self.rect_list.append(plat.draw(window))

    # Update Platform Manager
    def manage_platforms(self, window, colors, timer):

        # Move Platforms
        for plat in self.platform_list:
            plat.move()

        # Render Platforms
        self.render_platforms(window)
        
        # Spawn Platform at Spawn Rate Intervals (TODO: Add Platform Variations)
        if time.time() - self.spawn_time > self.spawn_rate:
            self.platform_list.append(self.spawn_platform(window.get_height() + -10 ,colors))

            # Reset Spawn Time
            self.spawn_time = time.time()

        # Remove Platforms that are Off the Screen
        self.platform_list = [plat for plat in self.platform_list if plat.y < window.get_height() + 10]