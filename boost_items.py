import pygame
import random

#The following code modified by ChatGPT 

class BoostItem:
    def __init__(self, x, y, width, height, boost_type, speed=2):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.boost_type = boost_type  # Type can be "parachute", "shield", "double_jump"
        self.speed = speed

    def draw(self, window):
        # Draw item (simple representation, e.g., a rectangle)
        if self.boost_type == "parachute":
            color = (0, 255, 0)
        elif self.boost_type == "shield":
            color = (0, 0, 255)
        elif self.boost_type == "double_jump":
            color = (255, 0, 0)
        pygame.draw.rect(window, color, (self.x, self.y, self.width, self.height))

    def update(self):
        # Move item down
        self.y += self.speed

    def check_collision(self, player_rect):
        # Check if item collides with player
        item_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return item_rect.colliderect(player_rect)


class BoostItemManager:
    def __init__(self, window_width, window_height, player):
        self.window_width = window_width
        self.window_height = window_height
        self.player = player
        self.items = []

    def spawn_item(self):

        # Randomly spawn a new boost item at the top of the screen
        x = random.randint(0, self.window_width - 20)
        y = 0
        width, height = 40, 40  # Size of the boost item
        boost_type = random.choice(["parachute", "shield", "double_jump"])
        item = BoostItem(x, y, width, height, boost_type)
        self.items.append(item)

    def update_items(self):
        for item in self.items:
            item.update()
            if item.y > self.window_height:
                self.items.remove(item)  # Remove item if it goes off-screen
            elif item.check_collision(self.player.get_rect()):
                # Activate corresponding boost effect
                if item.boost_type == "parachute":
                    self.player.collect_parachute()
                elif item.boost_type == "shield":
                    self.player.collect_shield()
                elif item.boost_type == "double_jump":
                    self.player.collect_double_jump()
                self.items.remove(item)

    def draw_items(self, window):
        for item in self.items:
            item.draw(window)
