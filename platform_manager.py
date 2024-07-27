from game_platform import Platform
from pydantic import BaseModel, Field, PositiveInt
import random


class Platform_Manager(BaseModel):

    spawn_rate: PositiveInt = Field(default=1)
    rect_list: list = Field(default=[])
    platform_list: list = Field(default=[Platform])


    # Random Platform Spawn
    def spawn_platform(self,screen_width,colors):
        x = random.randint(0,screen_width-100)
        y = random.randint(1,50)
        width = random.randint(50,150)
        height = 5
        down_speed = random.randint(1,2)
        color = random.choice(list(colors.values()))
        return Platform(x=x,y=y,width=width,height=height,color=color,down_speed=down_speed)
    
    # Create Text
    def render_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    # Render Platforms
    def render_platforms(self,window):
        for plat in self.platform_list:

            # Add Platform Rectangles to List (For Collision Detection)
            self.rect_list.append(plat.draw(window))

    # Update Platform Manager
    def manage_platforms(self,window,screen_width,screen_height,colors, timer):
        
        # Spawn Platform at Spawn Rate Intervals (TODO: Add Platform Variations)
        if timer.get_time() % self.spawn_rate == 0:
            self.platform_list.append(self.spawn_platform(screen_width,colors))

        # Render Platforms
        self.render_platforms(window)

        # Move Platforms
        for plat in self.platform_list:
            plat.move()

        # Remove Platforms that are Off the Screen
        self.platform_list = [plat for plat in self.platform_list if plat.y < screen_height]