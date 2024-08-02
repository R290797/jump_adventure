import pygame
from pydantic import BaseModel, Field


# Create New Background Class
class Background(BaseModel):

    y: int
    path: str
    screen: pygame.surface
    moving: bool = Field(default=False)

    # Error Handling
    class Config:
        arbitrary_types_allowed = True

    # Render Background
    def render(self):
        background_image = pygame.image.load(self.path).convert()
        background_image.set_alpha(128)
        background_image = pygame.transform.scale(background_image, (1000, 700))
        self.screen.blit(background_image, (0, self.y))

    def move(self):

        if self.y >= 1400:
            self.y = -699
        else:
            self.y += 1
