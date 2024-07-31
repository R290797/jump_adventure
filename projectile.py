import pygame
from pydantic import BaseModel, Field, PositiveInt
from enemy_manager import Enemy_Manager

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

    # Status Attributes
    alive: bool = Field(default=True)

    def draw(self, window):
        return pygame.draw.rect(window, (255,0,0), (self.x, self.y, self.width, self.height))
    
    def move(self):
        self.x += self.x_delta * self.speed
        self.y += self.y_delta * self.speed

    
    # Collision Detection with Enemies
    def enemy_collision_detection(self, enemy_manager: Enemy_Manager):

         # Iterate Rects (Go by Index to Find According enemy in Enemy List)
        for i in range(len(enemy_manager.rect_list)):

            # Check if Projectile Collides With Enemy
            if enemy_manager.rect_list[i].colliderect(self.x, self.y, self.width, self.height):

                # Destroy that Enemy (Set Alive to 0)
                enemy_manager.enemy_list[i].alive = False

                # Destroy current Projectile
                self.alive = False
    


