import pygame
import os

class Menu:
    def __init__(self, window, font, colors):
        self.window = window
        self.font = font
        self.colors = colors
        self.options = ['Start', 'High Scores', 'How to Play', 'Quit']
        self.selected_option = 0
        self.active = True
        self.high_scores_file = "high_scores.txt"
        self.high_scores = self.load_high_scores()
        self.menu_sound = pygame.mixer.Sound("SoundEffects/MainMenu-SoundEffect.wav") # Royalty Free Music: https://www.chosic.com/
        self.menu_sound.play(-1)

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
            self.menu_sound.stop()
        elif self.options[self.selected_option] == 'High Scores':
            self.show_high_scores()
        elif self.options[self.selected_option] == 'How to Play':
            self.show_how_to_play()
        elif self.options[self.selected_option] == 'Quit':
            pygame.quit()
            exit() 

    def show_high_scores(self):
        self.window.fill((255, 255, 255))
        title_surface = self.font.render("High Scores", True, self.colors["black"])
        title_rect = title_surface.get_rect(center=(self.window.get_width() // 2, 100))
        self.window.blit(title_surface, title_rect)

        for i, score in enumerate(self.high_scores):
            score_surface = self.font.render(f"{i + 1}. {score}", True, self.colors["black"])
            score_rect = score_surface.get_rect(center=(self.window.get_width() // 2, 200 + i * 40))
            self.window.blit(score_surface, score_rect)

        pygame.display.flip()

        # Wait for user to press a key to go back to the menu
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    def show_how_to_play(self):
        instructions = [
            "How to Play:",
            "",
            "Use the arrow keys to move:",
            "  - LEFT: Move left",
            "  - RIGHT: Move right",
            "  - UP: Shoot",
            "Press SPACE to jump.",
            "Press Q to quit the game.",
            "",
            "Avoid enemies and stay on platforms.",
            "Collect boost items for extra points."
        ]

        self.window.fill((255, 255, 255))
        for i, line in enumerate(instructions):
            instruction_surface = self.font.render(line, True, self.colors["black"])
            instruction_rect = instruction_surface.get_rect(center=(self.window.get_width() // 2, 100 + i * 40))
            self.window.blit(instruction_surface, instruction_rect)

        pygame.display.flip()

        # Wait for user to press a key to go back to the menu
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    def load_high_scores(self):
        if not os.path.exists(self.high_scores_file):
            return []

        with open(self.high_scores_file, 'r') as file:
            scores = file.readlines()
        return [int(score.strip()) for score in scores]

    def save_high_score(self, score):
        self.high_scores.append(score)
        self.high_scores = sorted(set(self.high_scores), reverse=True)[:10] 

        with open(self.high_scores_file, 'w') as file:
            for score in self.high_scores:
                file.write(f"{score}\n")

    def start_game(self):
        return not self.active
