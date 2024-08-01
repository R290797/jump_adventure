from enemies import Base_Enemy, Bouncing_Enemy, Chasing_Enemy
from pydantic import BaseModel, Field, PositiveInt

import pygame
import time
import random

class Enemy_Manager(BaseModel):

    player_x: int
    player_y: int

    # Enemy Object List (Enemies Being Display)
    enemy_list: list[Base_Enemy] = Field(default_factory=list) 

    # Enemy Rect List (For Collisiondetection)
    rect_list: list = Field(default_factory=list)

    # Spawn Attributes
    spawn_rate: float = Field(default=10.0) # Time between Enemy spawns (in Seconds)
    spawn_time: float = Field(default=time.time()) # Time since last Enemy spawn
 

    # Function to Render the Enemies
    def render_enemies(self, screen: pygame.surface):

        self.rect_list = []

        # Go through List of Enemies
        for enemy in self.enemy_list:
            
            # Add to Rect List and Draw
            self.rect_list.append(enemy.draw(screen))

    # Function to Spawn in Enemies
    def spawn_enemy(self, screen: pygame.surface):

        # Check time on Spawn
        if time.time() - self.spawn_time > self.spawn_rate:
            # TODO: Add Enemy Variations here

            # Place Enemy above the Top of the Screen
            self.enemy_list.append(Chasing_Enemy(y=-50, x=random.randint(0,screen.get_width())))

            # Reset Timer
            self.spawn_time = time.time()
    

    # Check if Enemies need to be despawned (Leave Screen or Eliminated by Player)
    def status_check(self, screen: pygame.surface):

        # Iterate through Enemy List, remove according Enemies
        for enemy in self.enemy_list:
            
            if not enemy.alive:
                self.enemy_list.remove(enemy)

    # Function Managing Enemy Spawning, Movement and Handling Logic
    def manage_enemies(self, screen: pygame.surface):

        # Remove "Dead" Enemies
        self.status_check(screen)
        
        # Move Enemies in Enemy List
        for enemy in self.enemy_list:
            enemy.move(screen, px_pos=self.player_x, py_pos=self.player_y)

        # Render Enemies
        self.render_enemies(screen)

         # Spawn Enemy
        self.spawn_enemy(screen)