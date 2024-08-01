import pygame
from pydantic import BaseModel, Field, PositiveInt
from projectile import Projectile
from enemy_manager import Enemy_Manager
import time

class Projectile_Manager(BaseModel):

    # Projectile List
    projectile_list: list[Projectile] = Field(default_factory=list)

     # Rect List
    rect_list: list = Field(default_factory=list)

    # Cooldown/Shot Logic Attributes
    shoot_cooldown: float = Field(default=1)
    last_shot: float = Field(default=time.time())

    # Add Projectile
    def add_projectile(self, x, y, width, height, speed):
        
        # Check if Shoot conditions are met (Shoot Condition)
        if time.time() - self.last_shot > self.shoot_cooldown:
            self.projectile_list.append(Projectile(x=x, y=y, width=width, height=height, speed=speed))
            self.last_shot = time.time()

    # Render Projectiles in List
    def render_projectiles(self, window):

        # Reset Rect List
        self.rect_list = []

        # Render Projectiles and add updated Rects. to Rect List
        for proj in self.projectile_list:
            rect = proj.draw(window)
            self.rect_list.append(rect)

        return self.rect_list
    
    # Class Config (Ensure Functions can be called without instantiating the class)
    class Config:
        arbitrary_types_allowed = True

    # Move Projectiles
    def move_projectiles(self):
        for proj in self.projectile_list:
            proj.move()

    # Remove Projectiles that are Off the Screen
    def remove_projectiles(self, window):
        for proj in self.projectile_list:

            # If Projectile Collided with enemy
            if not proj.alive:
                self.projectile_list.remove(proj)

            # If Projectile Leaves the Screen
            elif proj.y < -20  or proj.y > window.get_height() + 20 or proj.x < -10 or proj.x > window.get_width() + 10:
                self.projectile_list.remove(proj)

    # Managee Projectiles (Move and Remove)
    def manage_projectiles(self, window: pygame.surface, enemy_manager: Enemy_Manager):

        # Check for Enemy Collisions
        for proj in self.projectile_list:
            proj.enemy_collision_detection(enemy_manager)

        # Move Projectiles
        self.move_projectiles()

        # Remove Projectiles that are Off the Screen
        self.remove_projectiles(window)