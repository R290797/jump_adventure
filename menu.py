import pygame
import os


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
            "SoundEffects/MainMenu-SoundEffect.wav"
        )  # Royalty Free Music: https://www.chosic.com/
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

    def draw(self):
        self.window.fill((255, 255, 255))

        # Fill Screen with Background Image
        self.window.blit(self.background_image, self.background_rect)

        # Render each menu option
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

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                self.select_option()

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

    def display_scores(self):

        for i, score in enumerate(self.high_scores):
            score_surface = self.font.render(
                f"{i + 1}. {score}", True, self.colors["white"]
            )
            score_rect = score_surface.get_rect(
                center=(self.window.get_width() // 2, 200 + i * 40)
            )
            self.window.blit(score_surface, score_rect)

    def blit_scores(self):

        self.window.blit(self.background_image, self.background_rect)
        title_surface = self.font.render("High Scores", True, self.colors["yellow"])
        title_rect = title_surface.get_rect(center=(self.window.get_width() // 2, 100))
        self.window.blit(title_surface, title_rect)

    def blit_exit_instruction(self):

        exit_font = pygame.font.SysFont(None, 30)
        exit_color = self.colors["magenta"]
        exit_text = exit_font.render("Press 'Enter' to Exit", True, exit_color)
        exit_rect = exit_text.get_rect(topright=(self.window.get_width() - 20, 20))
        self.window.blit(exit_text, exit_rect)

    # This code was generated with the assistance of OpenAI's ChatGPT (Version 4)
    # For more information, visit https://www.openai.com/chatgpt
    def show_high_scores(self):

        # Blit Text
        self.blit_scores()
        self.display_scores()
        self.blit_exit_instruction()

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
        self.window.blit(self.background_image, self.background_rect)

        # Define font sizes for different parts
        title_font_size = 44
        heading_font_size = 36
        text_font_size = 28

        # Create font objects with the defined sizes
        title_font = pygame.font.SysFont(None, title_font_size)
        heading_font = pygame.font.SysFont(None, heading_font_size)
        text_font = pygame.font.SysFont(None, text_font_size)

        # Render the title
        title_surface = title_font.render("How to Play:", True, self.colors["yellow"])
        title_rect = title_surface.get_rect(center=(self.window.get_width() // 2, 100))
        self.window.blit(title_surface, title_rect)

        # Instructions with color differentiation
        instructions = [
            ("How to Play:", True),
            "",
            "Use the arrow keys to move:",
            "  - LEFT: Move left",
            "  - RIGHT: Move right",
            "  - UP: Shoot",
            "Press SPACE to jump.",
            "Press Q to quit the game.",
            "",
            ("Game Objectives:", True),
            "  - Avoid enemies and stay on platforms as difficulty increases.",
            "  - Collect boost items for extra points.",
            "  - Tip: You can go through sides of the screen and come out the other side",
            "",
            ("Platform Types:", True),
            "  - Normal Platform: Static platforms to stand on.",
            "  - Moving Platform: Platforms that move horizontally.",
            "  - Falling Platform: Platforms that fall rapidly.",
            "  - Disappearing Platform: Platforms that disappear when jump from them.",
            "",
            ("Enemy Types:", True),
            "  - Basic Enemy: Moves in a straight line.",
            "  - Bouncing Enemy: Moves in a bouncing pattern.",
            "  - Chasing Enemy: Follows the player.",
            "  - Tip: You can kill the enemies by jumping on them",
            "",
            ("Boost Items:", True),
            "  - Parachute: Slows down your fall.",
            "  - Double Jump: Allows you to jump again while in the air.",
            "  - Shield: Protects you from enemies.",
        ]

        # This code was generated with the assistance of OpenAI's ChatGPT (Version 4)
        # For more information, visit https://www.openai.com/chatgpt
        # Calculate total lines and scrollable height
        line_height = 40
        total_lines = len(instructions)
        total_scrollable_height = total_lines * line_height
        viewport_height = self.window.get_height() - 140
        max_scroll_position = max(0, total_scrollable_height - viewport_height)

        # This function implementation is inspired by a solution found on Stack Overflow
        # Original post: "Making a scrollbar but its inconsistent" by Rabbid76
        # URL: https://stackoverflow.com/questions/66369695/making-a-scrollbar-but-its-inconsistent
        # Handle scrolling
        running = True
        while running:
            self.window.blit(self.background_image, self.background_rect)

            # Render the instructions
            for i, item in enumerate(instructions):
                if isinstance(item, tuple):
                    line, is_heading = item
                else:
                    line = item
                    is_heading = False

                if is_heading:
                    font = heading_font
                    color = self.colors["yellow"]
                else:
                    font = text_font
                    color = (255, 255, 255)

                instruction_surface = font.render(line, True, color)
                instruction_rect = instruction_surface.get_rect(
                    center=(
                        self.window.get_width() // 2,
                        140 + i * line_height - self.scroll_position,
                    )
                )
                self.window.blit(instruction_surface, instruction_rect)

            # Draw scrollbar
            self.draw_scroll_bar(total_lines, viewport_height, total_scrollable_height)

            exit_font = pygame.font.SysFont(None, 30)
            exit_color = self.colors["magenta"]
            exit_text = exit_font.render("Press 'Enter' to Exit", True, exit_color)
            exit_rect = exit_text.get_rect(topright=(self.window.get_width() - 20, 20))
            self.window.blit(exit_text, exit_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False
                    elif event.key == pygame.K_DOWN:
                        self.scroll_position = min(
                            self.scroll_position + self.scroll_step, max_scroll_position
                        )
                    elif event.key == pygame.K_UP:
                        self.scroll_position = max(
                            self.scroll_position - self.scroll_step, 0
                        )
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    def draw_scroll_bar(self, total_lines, viewport_height, total_scrollable_height):
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
