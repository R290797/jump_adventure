from game_platform import (
    Platform,
    Horizontal_Platform,
    Falling_Platform,
    Disappearing_Platform,
)
from pydantic import BaseModel, Field, PositiveInt
import random
import time
import pygame

# Use pytest -p no:warnings

class Platform_Manager(BaseModel):

    # Spawn Attributes
    spawn_rate: float = Field(default=1.0)  # Time between platform spawns
    spawn_time: float = Field(default=time.time())  # Time since last platform spawn
    rect_list: list = Field(default=[])

    # Dynamic Speed
    vert_speed: int = Field(default=1)
    horz_speed: int = Field(default=1)

    # Start With Base Platform
    platform_list: list = Field(
        default=[
            Platform(
                x=-400,
                y=100,
                width=1500,
                height=70,
                color=(0, 255, 0),
                down_speed=vert_speed,
                radius=15,
                direction=0,
            )
        ]
    )

    # Random Platform Spawn
    def spawn_platform(self, screen_width, colors):
        x = random.randint(0, screen_width)
        y = -100
        width = random.randint(50, 150)
        height = 20

        platform_type = random.choices(
            [Platform, Horizontal_Platform, Falling_Platform, Disappearing_Platform],
            [0.4, 0.2, 0.2, 0.2],
        )[0]

        return platform_type(
            x=x,
            y=y,
            width=width,
            height=height,
            vert_speed=self.vert_speed,
            horz_speed=self.horz_speed,
            direction=random.choice([-1, 1]),
        )

    # Render Platforms
    def render_platforms(self, window):

        # Reset Rect List
        self.rect_list = []

        for plat in self.platform_list:

            # Add Platform Rectangles to List (For Collision Detection)
            self.rect_list.append(plat.get_rect())

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

    # Function to Increase Difficulty of Platform Manager
    def increment_difficulty(self, level: int):

        # Increase Speed of Platforms Every up to Level 20 (every 2 Levels)
        if level < 20 and level % 2 == 0:
            self.horz_speed += 1
            self.vert_speed += 1

            if not self.spawn_rate < 0.2:
                self.spawn_rate -= 0.2
