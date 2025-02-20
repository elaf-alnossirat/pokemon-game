import pygame
import sys
import sound_manager  # Import du gestionnaire de son

class MainMenu:
    def __init__(self):
        self.running = True

    def draw_button(self, screen, x, y, width, height, text, is_hovered=False):
        neon_color = (0, 255, 0)          # Vert néon pour le bouton
        neon_hover_color = (0, 255, 255)  # Bleu néon quand survolé
        glow_color = (0, 255, 255)        # Couleur de glow

        # Effet de glow lors du survol
        if is_hovered:
            pygame.draw.rect(screen, glow_color, (x - 5, y - 5, width + 10, height + 10))
        pygame.draw.rect(screen, neon_hover_color if is_hovered else neon_color, (x, y, width, height))

        font = pygame.font.SysFont("arial", 24)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(text_surface, text_rect)

    def show(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Pokémon Game - Main Menu")
        clock = pygame.time.Clock()

        background_image = pygame.image.load("assets/main_menu_background.jpg")

        # Positions et tailles des boutons
        button_width, button_height = 200, 50
        start_button_x, start_button_y = 300, 200
        pokedex_button_x, pokedex_button_y = 300, 275
        quit_button_x, quit_button_y = 300, 350

        while self.running:
            screen.blit(background_image, (0, 0))
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Vérification du survol de chaque bouton
            start_hovered = start_button_x <= mouse_x <= start_button_x + button_width and \
                            start_button_y <= mouse_y <= start_button_y + button_height
            pokedex_hovered = pokedex_button_x <= mouse_x <= pokedex_button_x + button_width and \
                              pokedex_button_y <= mouse_y <= pokedex_button_y + button_height
            quit_hovered = quit_button_x <= mouse_x <= quit_button_x + button_width and \
                           quit_button_y <= mouse_y <= quit_button_y + button_height

            # Affichage des boutons
            self.draw_button(screen, start_button_x, start_button_y, button_width, button_height, "Start", start_hovered)
            self.draw_button(screen, pokedex_button_x, pokedex_button_y, button_width, button_height, "Pokedex", pokedex_hovered)
            self.draw_button(screen, quit_button_x, quit_button_y, button_width, button_height, "Quit", quit_hovered)

            pygame.display.flip()
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_hovered:
                        sound_manager.play_select_sound()
                        return "start"
                    if pokedex_hovered:
                        sound_manager.play_select_sound()
                        return "pokedex"
                    if quit_hovered:
                        sound_manager.play_select_sound()
                        return "quit"
