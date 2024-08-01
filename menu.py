import pygame

class Menu:
    def __init__(self, window, font, colors):
        self.window = window
        self.font = font
        self.colors = colors
        self.options = ['Start', 'High Scores', 'How to Play', 'Quit']
        self.selected_option = 0
        self.active = True

    def draw(self):
        self.window.fill((255, 255, 255))

        # Render each menu option
        for i, option in enumerate(self.options):
            color = self.colors["black"]
            if i == self.selected_option:
                color = self.colors["red"]  
            text_surface = self.font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(self.window.get_width() // 2, 200 + i * 60))
            self.window.blit(text_surface, text_rect)

        pygame.display.flip()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                self.select_option()

    def select_option(self):
        if self.options[self.selected_option] == 'Start':
            self.active = False
        elif self.options[self.selected_option] == 'Quit':
            pygame.quit()
            exit()
            
        #TODO: Functionality for 'High Scores' and 'How to Play' 

    def start_game(self):
        return not self.active
