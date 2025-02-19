import pygame

class MainMenu:
    def __init__(self):
        self.running = True

    def draw_button(self, screen, x, y, width, height, text, is_hovered=False):
        neon_color = (0, 255, 0)  # Neon Green for the button
        neon_hover_color = (0, 255, 255)  # Neon Blue when hovered
        glow_color = (0, 255, 255)  # Glow color on hover

        # Glow effect when hovered
        if is_hovered:
            pygame.draw.rect(screen, glow_color, (x - 5, y - 5, width + 10, height + 10))  # Glow around the button

        pygame.draw.rect(screen, neon_hover_color if is_hovered else neon_color, (x, y, width, height))  # Draw the button

        font = pygame.font.SysFont("arial", 24)
        text_surface = font.render(text, True, (0, 0, 0))  # Black text
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(text_surface, text_rect)

    def show(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()

        # Load background image
        background_image = pygame.image.load("assets/main_menu_background.jpg")  # Update the path if needed

        # Button positions and sizes
        button_width, button_height = 200, 50

        start_button_x, start_button_y = 300, 200
        pokedex_button_x, pokedex_button_y = 300, 275
        quit_button_x, quit_button_y = 300, 350

        while self.running:
            screen.blit(background_image, (0, 0))  # Draw background

            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Check if the mouse is over the buttons
            start_hovered = start_button_x <= mouse_x <= start_button_x + button_width and \
                            start_button_y <= mouse_y <= start_button_y + button_height
            pokedex_hovered = pokedex_button_x <= mouse_x <= pokedex_button_x + button_width and \
                              pokedex_button_y <= mouse_y <= pokedex_button_y + button_height
            quit_hovered = quit_button_x <= mouse_x <= quit_button_x + button_width and \
                           quit_button_y <= mouse_y <= quit_button_y + button_height

            # Draw buttons with text
            self.draw_button(screen, start_button_x, start_button_y, button_width, button_height, "Start", start_hovered)
            self.draw_button(screen, pokedex_button_x, pokedex_button_y, button_width, button_height, "Pokedex", pokedex_hovered)
            self.draw_button(screen, quit_button_x, quit_button_y, button_width, button_height, "Quit", quit_hovered)

            pygame.display.flip()
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_hovered:
                        self.running = False
                        return "start"
                    if pokedex_hovered:
                        self.running = False
                        return "pokedex"
                    if quit_hovered:
                        self.running = False
                        return "quit"