import pygame
import os


# This function implementation is inspired by a solution found on Game Dev Academy
# Original post: "Pygame Menu Tutorial – Complete Guide" by Zenva
# URL: https://gamedevacademy.org/pygame-menu-tutorial-complete-guide/
class Menu:
    def __init__(self, window, font, colors):
        self.window = window
        self.font = font
        self.colors = colors
        self.options = ["Start", "High Scores", "How to Play", "Quit"]
        self.selected_option = 0
        self.active = True
        self.high_scores_file = "high_scores.txt"
        self.high_scores = self.load_high_scores()
        self.menu_sound = pygame.mixer.Sound(
            "Resources/Sounds/MainMenu-SoundEffect.wav"
        )
        self.menu_sound.play(-1)

        # Add Background Image
        self.background_image = pygame.image.load(
            "Resources/Sprites/Sprite-background_3.png"
        )
        self.background_image = pygame.transform.scale(
            self.background_image, (1000, 700)
        )
        self.background_rect = self.background_image.get_rect(topleft=(0, 0))

        # Scrolling Variables
        self.scroll_position = 0
        self.scroll_step = 40

        # Load Instructions from .txt
        self.instructions = self.load_instructions()

    # This code was generated with the assistance of OpenAI's ChatGPT (Version 4)
    # For more information, visit https://www.openai.com/chatgpt
    def load_instructions(self):
        instructions = []
        try:
            with open("instructions.txt", "r") as file:
                instructions = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            print("Error: instructions.txt file not found.")
        except Exception as e:
            print(f"Error reading instructions.txt: {e}")
        return instructions

    # Fill the Screen with Background Image
    def draw(self):
        self.window.fill((255, 255, 255))
        self.window.blit(self.background_image, self.background_rect)
        for i, option in enumerate(self.options):
            color = self.colors["white"]
            if i == self.selected_option:
                color = self.colors["red"]
            text_surface = self.font.render(option, True, color)
            text_rect = text_surface.get_rect(
                center=(self.window.get_width() // 2, 200 + i * 60)
            )
            self.window.blit(text_surface, text_rect)
        pygame.display.flip()

    # Handle Menu Navigation
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                self.select_option()

    # Handle Menu Components
    def select_option(self):
        if self.options[self.selected_option] == "Start":
            self.active = False
            self.menu_sound.stop()
        elif self.options[self.selected_option] == "High Scores":
            self.show_high_scores()
        elif self.options[self.selected_option] == "How to Play":
            self.show_how_to_play()
        elif self.options[self.selected_option] == "Quit":
            pygame.quit()
            exit()

    # Handle Displaying High Scores
    def display_scores(self):
        for i, score in enumerate(self.high_scores):
            score_surface = self.font.render(
                f"{i + 1}. {score}", True, self.colors["white"]
            )
            score_rect = score_surface.get_rect(
                center=(self.window.get_width() // 2, 200 + i * 40)
            )
            self.window.blit(score_surface, score_rect)

    # Handle High Scores Title
    def blit_scores(self):
        self.window.blit(self.background_image, self.background_rect)
        title_surface = self.font.render("High Scores", True, self.colors["yellow"])
        title_rect = title_surface.get_rect(center=(self.window.get_width() // 2, 100))
        self.window.blit(title_surface, title_rect)

    # Handle 'Exit' Instructions on High Scores Page
    def blit_exit_instruction(self):
        exit_font = pygame.font.SysFont(None, 30)
        exit_color = self.colors["magenta"]
        exit_text = exit_font.render("Press 'Enter' to Exit", True, exit_color)
        exit_rect = exit_text.get_rect(topright=(self.window.get_width() - 20, 20))
        self.window.blit(exit_text, exit_rect)

    # This code was generated with the assistance of OpenAI's ChatGPT (Version 4)
    # For more information, visit https://www.openai.com/chatgpt
    # Wait for user to press a key to go back to Menu
    def show_high_scores(self):
        self.blit_scores()
        self.display_scores()
        self.blit_exit_instruction()
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    # This function implementation is inspired by a solution found on Game Dev Academy
    # Original post: "Pygame Menu Tutorial – Complete Guide" by Zenva
    # URL: https://gamedevacademy.org/pygame-menu-tutorial-complete-guide/
    # Handle How To Play function
    def show_how_to_play(self):
        self.window.blit(self.background_image, self.background_rect)
        self.render_how_to_play_title()
        line_height = 40
        viewport_height = self.window.get_height() - 140
        max_scroll_position = self.calculate_max_scroll_position(
            line_height, viewport_height
        )
        self.handle_scrolling(line_height, viewport_height, max_scroll_position)

    # Handle How to Play Title
    def render_how_to_play_title(self):
        title_font = pygame.font.SysFont(None, 44)
        title_surface = title_font.render("How to Play:", True, self.colors["yellow"])
        title_rect = title_surface.get_rect(center=(self.window.get_width() // 2, 100))
        self.window.blit(title_surface, title_rect)

    # This function implementation is inspired by a solution found on Stack Overflow
    # Original post: "Making a scrollbar but its inconsistent" by Rabbid76
    # URL: https://stackoverflow.com/questions/66369695/making-a-scrollbar-but-its-inconsistent
    # Handle Scrolling Parameters
    def calculate_max_scroll_position(self, line_height, viewport_height):
        total_lines = len(self.instructions)
        total_scrollable_height = total_lines * line_height
        return max(0, total_scrollable_height - viewport_height)

    # This code was generated with the assistance of OpenAI's ChatGPT (Version 4)
    # For more information, visit https://www.openai.com/chatgpt
    def handle_scrolling(self, line_height, viewport_height, max_scroll_position):
        self.scroll_position = 0
        running = True
        while running:
            self.window.blit(self.background_image, self.background_rect)
            self.render_instructions(line_height)
            self.draw_scroll_bar(viewport_height, max_scroll_position)
            self.blit_exit_instruction()
            pygame.display.flip()
            running = self.process_scrolling_events(max_scroll_position)

    # Render the instructions from txt
    def render_instructions(self, line_height):
        for i, line in enumerate(self.instructions):
            font, color = (
                (pygame.font.SysFont(None, 36), self.colors["yellow"])
                if line.endswith(":") and not line.startswith(" ")
                else (pygame.font.SysFont(None, 28), (255, 255, 255))
            )
            instruction_surface = font.render(line, True, color)
            instruction_rect = instruction_surface.get_rect(
                center=(
                    self.window.get_width() // 2,
                    140 + i * line_height - self.scroll_position,
                )
            )
            self.window.blit(instruction_surface, instruction_rect)

    # Handle & Process Scroll Positioning
    def process_scrolling_events(self, max_scroll_position):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return False
                elif event.key == pygame.K_DOWN:
                    self.scroll_position = min(
                        self.scroll_position + self.scroll_step, max_scroll_position
                    )
                elif event.key == pygame.K_UP:
                    self.scroll_position = max(
                        self.scroll_position - self.scroll_step, 0
                    )
            if event.type == pygame.QUIT:
                self.quit_game()
        return True

    # Handle Drawing Scroll Bar
    def draw_scroll_bar(self, viewport_height, total_scrollable_height):
        if total_scrollable_height == 0:
            return
        bar_height = viewport_height * (viewport_height / total_scrollable_height)
        bar_y = (
            self.scroll_position
            / (total_scrollable_height - viewport_height)
            * (viewport_height - bar_height)
        )
        pygame.draw.rect(
            self.window,
            (169, 169, 169),
            (self.window.get_width() - 20, 140 + bar_y, 10, bar_height),
        )

    # This function implementation is inspired by a solution found on Stack Overflow
    # Original post: "How to read, write and update of your game highscore in pygame from/to file.txt saved.?" by Mike67
    # URL: https://stackoverflow.com/questions/63751107/how-to-read-write-and-update-of-your-game-highscore-in-pygame-from-to-file-txt
    # Handle Loading Highscores saved in high_scores.txt
    def load_high_scores(self):
        if not os.path.exists(self.high_scores_file):
            return []
        with open(self.high_scores_file, "r") as file:
            scores = file.readlines()
        return [int(score.strip()) for score in scores]

    def save_high_score(self, score):
        self.high_scores.append(score)
        self.high_scores = sorted(set(self.high_scores), reverse=True)[:10]
        with open(self.high_scores_file, "w") as file:
            for score in self.high_scores:
                file.write(f"{score}\n")

    def quit_game(self):
        pygame.quit()
        exit()
