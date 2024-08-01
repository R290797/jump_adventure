import pygame
from pydantic import BaseModel, Field, PositiveInt,  ConfigDict
from projectile_manager import Projectile_Manager
from enemy_manager import Enemy_Manager
from boosts import Parachute, Shield, DoubleJump

class Player(BaseModel):

    # Position Attributes
    x: int
    y: int
    width: PositiveInt
    height: PositiveInt
    color: tuple[int, int, int] = Field(default=(0,255,0))

    # Movement Attributes
    speed: int = Field(default=2)
    gravity: PositiveInt = Field(default=1)
    x_delta: int = Field(default=0)
    y_delta: int = Field(default=0)

    # Jump Mechnics
    grounded: bool = Field(default=False)
    can_jump: bool = Field(default=True)
    jump_height: PositiveInt = Field(default=10)
    double_jump_active: bool = Field(default=False)

    # Grounded Buffer (Prevents inconsistent collision detection)
    grounded_buffer: int = Field(default=10)

    # Shooting Mechanic
    projectile_manager: Projectile_Manager = Projectile_Manager(shoot_cooldown=1)
    
    # Status Mechanics
    alive: bool = Field(default=True)
    player_enemy_collision: bool = Field(default=False)

     # Boost-Up Effects
    parachute: Parachute = None
    shield: Shield = None
    double_jump: DoubleJump = None
    shield_active: bool = Field(default=False)
    extra_jump: bool = False  # For double jump tracking
    
    # Sounds Effects
    power_sound : pygame.mixer.Sound

     # Configuration to allow arbitrary types
    class Config:
        arbitrary_types_allowed = True

    # Draw Player (And Return Rect. for Collision Detection)
    def draw_self(self, window):

        # Draw Player Rectangle and Return Rect
        return pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
           
    # Jump
    def jump(self):

        if self.can_jump or (self.double_jump_active and not self.extra_jump):
            self.y_delta = -self.jump_height  
            self.grounded = False
            if self.can_jump:
                self.can_jump = False
            elif self.double_jump_active:
                self.extra_jump = True

    # Shoot
    def shoot(self):

        # Spawn Projectiles at the Center of the  Player
        self.projectile_manager.add_projectile(self.x + (self.width//2), self.y + (self.height//2), 5, 5, 5)

    # Check if Player is Grounded (and Apply Gravity)
    def check_grounded(self):

        # Check if Player is Grounded
        if self.grounded:
            self.y_delta = 0

            # Reset Grounded Buffer
            self.grounded_buffer = 10
        else:
            # Gravity (Falling), Player is not Grounded
            self.y_delta += self.gravity
            self.y += self.y_delta
            self.grounded_buffer -= 1

    # If Grounded Buffer Runs out, Jump Becomes Unavailable
    def check_jump(self):
        if self.grounded_buffer > 0:
            self.can_jump = True
        else:
            self.can_jump = False

    # Wrap Around Logic
    def wrap_around(self, screen_width):
        if self.x > screen_width:
            self.x = -self.width
        elif self.x + self.width < 0:
            self.x = screen_width

    # Manage Shooting Mechanic
    def manage_player_attack(self, window: pygame.surface, enemy_manager: Enemy_Manager):

         # Render Projectiles
        self.projectile_manager.render_projectiles(window)

        # Manage Projectiles (Movement and Despawning)
        self.projectile_manager.manage_projectiles(window, enemy_manager)


    # Update Player Movement
    def update(self, window: pygame.surface, enemy_manager: Enemy_Manager):

        # Grounded Check
        self.check_grounded()

        # Move Player Horizontally
        self.x += self.x_delta * self.speed

        # Manage Player Attack (Shooting)
        self.manage_player_attack(window, enemy_manager)

        # Handle wrap-around
        self.wrap_around(window.get_width())

        # Check Jump
        self.check_jump()

        # Check for falling off the screen
        if self.y > window.get_height() + 100:
            self.alive = False



    # Collision Detection

    # Player/Platform Collision
    def platform_collision(self, plat_rect_list: list):

        self.grounded = False

        # Iterate Through Platform Rectangles
        for i in range(len(plat_rect_list)):

            # Check if Player Rect Collides with Platform Rect
            if plat_rect_list[i].colliderect(self.x, self.y, self.width, self.height):

                # Check if Player y speed is positive (Falling)
                if self.y_delta >= 0 and self.grounded == False:

                    # Set Player Grounded
                    self.grounded = True
                    break


    # Player/Enemy Collision (Destroy Enemy if Coming From the Top - Falling)
    def enemy_collision(self, enemy_manager: Enemy_Manager): 

        # Iterate Rects (Go by Index to Find According enemy in Enemy List)
        for i in range(len(enemy_manager.rect_list)):

            # Check if Player Collides With Enemy (On the Bottom half)
            if enemy_manager.rect_list[i].colliderect(self.x, self.y + (2 * self.height //3), self.width, self.height //3):

                # Destroy that Enemy (Set Alive to False)
                enemy_manager.enemy_list[i].alive = False
                
                # Make Player Jump
                self.y_delta = -self.jump_height

            # If Collides with top 2/3 of Player, Lose the Game
            elif enemy_manager.rect_list[i].colliderect(self.x, self.y, self.width, 2 * self.height //3) and enemy_manager.enemy_list[i].alive:
                self.alive = False

    # Boost Mechanic Functions (Collision and Collecting)
    def collect_parachute(self):
        if not self.parachute:
            self.parachute = Parachute(self)
        self.parachute.activate()
        self.power_sound.play()

    def collect_shield(self):
        if not self.shield:
            self.shield = Shield(self)
        self.shield.activate()
        self.power_sound.play()

    def collect_double_jump(self):
        if not self.double_jump:
            self.double_jump = DoubleJump(self)
        self.double_jump.activate()
        self.power_sound.play()        

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
