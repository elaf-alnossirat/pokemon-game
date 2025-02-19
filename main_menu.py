import pygame

class MainMenu:
    def __init__(self):
        self.running = True

    def draw_button(self, screen, x, y, radius, icon, is_hovered=False):
        neon_color = (0, 255, 0)  # Neon Green for the button
        neon_hover_color = (0, 255, 255)  # Neon Blue when hovered
        glow_color = (0, 255, 255)  # Glow color on hover

        # Glow effect when hovered
        if is_hovered:
            pygame.draw.circle(screen, glow_color, (x, y), radius + 5)  # Glow around the circle

        pygame.draw.circle(screen, neon_hover_color if is_hovered else neon_color, (x, y), radius)  # Draw the button circle

        # Draw the icon in the center of the circle
        icon_rect = icon.get_rect(center=(x, y))
        screen.blit(icon, icon_rect)

    def show(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()

        # Load background image
        background_image = pygame.image.load("assets/main_menu_background.jpg")  # Update the path if needed

        # Load button icons (94x94)
        start_icon = pygame.image.load("assets/start_icon.png")  # Path to the start icon
        exit_icon = pygame.image.load("assets/exit_icon.png")  # Path to the exit icon

        # Resize the icons to 94x94
        start_icon = pygame.transform.scale(start_icon, (94, 94))
        exit_icon = pygame.transform.scale(exit_icon, (94, 94))

        # Button positions (right side of the screen)
        start_button_x = 650  # Move the buttons further right
        start_button_y = 200
        button_radius = 47  # Half of 94 (the size of the icon)

        quit_button_x = 650  # Keep aligned to the right
        quit_button_y = 350  # Increase vertical space between buttons

        while self.running:
            screen.blit(background_image, (0, 0))  # Draw background

            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Check if the mouse is over the buttons
            start_hovered = (start_button_x - button_radius <= mouse_x <= start_button_x + button_radius and 
                             start_button_y - button_radius <= mouse_y <= start_button_y + button_radius)
            quit_hovered = (quit_button_x - button_radius <= mouse_x <= quit_button_x + button_radius and 
                            quit_button_y - button_radius <= mouse_y <= quit_button_y + button_radius)

            # Draw buttons with icons
            self.draw_button(screen, start_button_x, start_button_y, button_radius, start_icon, start_hovered)
            self.draw_button(screen, quit_button_x, quit_button_y, button_radius, exit_icon, quit_hovered)

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
                    if quit_hovered:
                        self.running = False
                        return "quit"
