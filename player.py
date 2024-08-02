import pygame
from pydantic import BaseModel, Field, PositiveInt,  ConfigDict
from projectile_manager import Projectile_Manager
from enemy_manager import Enemy_Manager
from platform_manager import Platform_Manager
from game_platform import Platform, Horizontal_Platform, Disappearing_Platform, Falling_Platform
from boosts import Parachute, Shield, DoubleJump

class Player(BaseModel):

    # Position Attributes
    x: int
    y: int
    width: PositiveInt
    height: PositiveInt
    color: tuple[int, int, int] = Field(default=(0,255,0))

    # Sounds Effects
    power_sound : pygame.mixer.Sound
    hit_sound: pygame.mixer.Sound
    break_sound: pygame.mixer.Sound

    # Movement Attributes
    speed: int = Field(default=2)
    gravity: float = Field(default=1)
    x_delta: int = Field(default=0)
    y_delta: int = Field(default=0)

    # Added X Velocity through Moving Platform
    added_x_delta: int = Field(default=0)

    # Jump Mechnics
    grounded: bool = Field(default=False)
    can_jump: bool = Field(default=True)
    jump_height: PositiveInt = Field(default=10)
    double_jump_active: bool = Field(default=False)

    # Grounded Buffer (Prevents inconsistent collision detection) and Platform Interactions
    grounded_buffer: int = Field(default=10)
    last_touch_type: str = Field(default="none")

    # Shooting Mechanic
    projectile_manager: Projectile_Manager = Projectile_Manager(shoot_cooldown=1)
    
    # Status Mechanics
    alive: bool = Field(default=True)
    player_enemy_collision: bool = Field(default=False)

     # Boost-Up Effects
    parachute: Parachute = Parachute(active=False)
    shield: Shield = Shield(active=False)
    double_jump: DoubleJump = DoubleJump(active=False)
    
    # Configuration to allow arbitrary types
    class Config:
        arbitrary_types_allowed = True

    # Draw Player (And Return Rect. for Collision Detection) 
    def draw_self(self, window):
        
        # Draw Player Rectangle and Return Rect
        return pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
    
    # Return Rect for Collision
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
           
    # Jump
    def jump(self):

        if self.can_jump:

            self.y_delta = -self.jump_height  
            self.grounded = False

            if self.can_jump:
                self.can_jump = False

        # Double Jump if active
        elif not self.can_jump and self.double_jump.active:

            self.y_delta = -self.jump_height
            self.double_jump.active = False  
           

    # Shoot
    def shoot(self):

        # Spawn Projectiles at the Center of the  Player
        self.projectile_manager.add_projectile(int(self.x + (self.width//2) - 5), int(self.y + (self.height//2)), 25, 20, 5, self.hit_sound)

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

    # Limit Y position of the Player
    def check_height(self):

        if self.y < -70:
            self.y_delta = 0
            self.y = -69

    # If Grounded Buffer Runs out, Jump Becomes Unavailable
    def check_jump(self):
        if self.grounded_buffer > 0:
            self.can_jump = True
        else:
            self.can_jump = False
            self.last_touch_type = "none"

    def is_on_platform(self):
        if self.grounded_buffer > 0:
            return True
        else:
            return False

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

    # Check if Boosts are still active
    def check_double_jump(self):

        # Check Durations
        if self.double_jump.active:
            self.double_jump.check_duration()
        
    def check_shield(self):

        # Check Duration
        if self.shield.active:
            self.shield.check_duration()

    def check_parachute(self):

        # Check Duration
        if self.parachute.active:
            self.parachute.check_duration()

        # Apply Parachute Effects
        if self.parachute.active: self.gravity = 0.5
        else: self.gravity = 1
              
    def check_boosts(self):

        self.check_double_jump()
        self.check_shield()
        self.check_parachute()
           
    # Update Player Movement
    def update(self, window: pygame.surface, enemy_manager: Enemy_Manager):

        # Grounded Positional Values
        self.check_grounded()
        self.check_height()

        # Move Player Horizontally
        self.x += (self.x_delta * self.speed) + self.added_x_delta
        self.wrap_around(window.get_width())

        # Manage Player Attack (Shooting)
        self.manage_player_attack(window, enemy_manager)
        
        # Check Conditions
        self.check_jump()
        self.check_boosts()

        # Check for falling off the screen
        if self.y > window.get_height() + 100:
            self.alive = False

    # Collision Detection and Interactions

    # Player/Platform Interactions
    def move_with_plat(self, platform: Platform):

        # If HorizontalPlatform, Move in the Same Direction as the Platform
        if self.last_touch_type == "horizontal" and self.is_on_platform():
            self.added_x_delta = platform.horz_speed * platform.direction
        else:
            self.added_x_delta = 0

    def break_platform(self, platform: Platform):

        # Check if Platform Has been Touched, 
        if platform.type == "disappearing":
            platform.set_first_touch()

    # Apply interactions with Platforms
    def platform_interactions(self, platform: Platform):

        self.grounded = True
        self.move_with_plat(platform)
        self.break_platform(platform)

    # Remove Disappearing Platforms After They have been touched and Player has Left
    def remove_d_platforms(self, platform_manager: Platform_Manager):
            
        for plat in platform_manager.platform_list:
            # Move Platform If leaving the Platform (IF they are of type disappearing)
            if plat.type == "disappearing":

                if not self.last_touch_type == "disappearing" and plat.first_touch == True:
            
                    self.break_sound.play()
                    platform_manager.platform_list.remove(plat)
                    
    # Player/Platform Collision
    def platform_collision(self, platform_manager: Platform_Manager):
        self.grounded = False

        # Iterate Through Platform Rectangles / Check for Collisions
        for plat in platform_manager.platform_list:

            if plat.get_rect().colliderect(self.x, self.y, self.width, self.height):

                # Set Last Touch Type (For Interactions)
                self.last_touch_type = plat.type

                # Check if Player y speed is positive (Falling)
                if self.y_delta >= 0 and self.grounded == False:
    
                    # Apply Interactions
                    self.platform_interactions(plat)
                    break




    # Handle All Platform Functionality
    def handle_player_platforms(self, platform_manager: Platform_Manager, screen: pygame.surface):

        # Remove Disappearing Platforms
        self.remove_d_platforms(platform_manager)

        # Check Collisions
        self.platform_collision(platform_manager)
    
    # Player/Enemy Collision (Destroy Enemy if Coming From the Top - Falling)
    def enemy_collision(self, enemy_manager: Enemy_Manager): 

        # Iterate Rects (Go by Index to Find According enemy in Enemy List)
        for enemy in enemy_manager.enemy_list:

            # Check if Player Collides With Enemy (On the Bottom half)
            if enemy.get_rect().colliderect(self.x, self.y + (2 * self.height //3), self.width, self.height //3):

                # Destroy that Enemy (Set Alive to False)
                enemy.alive = False
                self.hit_sound.play()
                
                # Make Player Jump
                self.y_delta = -self.jump_height

            # If Collides with top 2/3 of Player, Lose the Game (And Player Doesnt Have Shield)
            elif enemy.get_rect().colliderect(self.x, self.y, self.width, 2 * self.height //3) and enemy.alive and not self.shield.active:
                self.alive = False

    # Boost Mechanic Functions (Collision and Collecting)
    def collect_parachute(self):
        if not self.parachute.active:
            self.parachute = Parachute()
        self.parachute.activate()
        self.power_sound.play()

    def collect_shield(self):
        if not self.shield.active:
            self.shield = Shield()
        self.shield.activate()
        self.power_sound.play()

    def collect_double_jump(self):
        if not self.double_jump.active:
            self.double_jump = DoubleJump()
        self.double_jump.activate()
        self.power_sound.play()        

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
