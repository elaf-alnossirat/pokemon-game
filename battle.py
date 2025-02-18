import pygame
import random
from pokemon import Pokemon

class Battle:
    def __init__(self, available_pokemon, opponent_pokemon):
        self.player_pokemon = self.choose_pokemon(available_pokemon)
        self.opponent_pokemon = opponent_pokemon
        self.running = True
        self.player_turn = True
        self.message = ""
        self.message_duration = 3000
        self.message_start_time = 0
        self.waiting_for_acknowledgment = False  # Flag to check if we are waiting for user acknowledgment

    def display_moves(self, screen):
        font = pygame.font.Font(None, 36)
        move_box_x = 50
        move_box_y = 450
        button_width = 300
        button_height = 40
        button_spacing = 10
        
        for index, move in enumerate(self.player_pokemon.moves):
            button_x = move_box_x + (index % 2) * (button_width + button_spacing)
            button_y = move_box_y + (index // 2) * (button_height + button_spacing)
            
            mouse_x, mouse_y = pygame.mouse.get_pos()
            is_hovered = button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height
            
            button_color = (0, 0, 180) if is_hovered else (0, 0, 255)
            pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
            
            move_text = font.render(move.capitalize(), True, (255, 255, 255))
            screen.blit(move_text, (button_x + 10, button_y + 5))
    
    def handle_attack(self, screen, move):
        if self.player_turn:
            self.message = f"{self.player_pokemon.name} used {move}!"
            self.message_start_time = pygame.time.get_ticks()
            
            self.player_pokemon.attack(move, self.opponent_pokemon)
            self.player_turn = False

            if self.opponent_pokemon.is_fainted():
                self.message = f"{self.opponent_pokemon.name} fainted! You win!"
                self.running = False
                self.waiting_for_acknowledgment = True  # Wait for acknowledgment
                return
    
    def opponent_turn(self, screen):
        if pygame.time.get_ticks() - self.message_start_time >= self.message_duration:
            pygame.time.delay(500)
            
            # Let opponent choose a move and attack
            opponent_move = random.choice(self.opponent_pokemon.moves)
            self.message = f"{self.opponent_pokemon.name} used {opponent_move}!"  # Show opponent's attack message
            self.message_start_time = pygame.time.get_ticks()
            
            self.opponent_pokemon.attack(opponent_move, self.player_pokemon)

            if self.player_pokemon.is_fainted():
                self.message = f"{self.player_pokemon.name} fainted! You lose!"
                self.running = False
                self.waiting_for_acknowledgment = True  # Wait for acknowledgment
            else:
                self.player_turn = True

    def choose_pokemon(self, available_pokemon):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        font = pygame.font.Font(None, 36)
        clock = pygame.time.Clock()
        selected_pokemon = None

        # Layout for Pokémon selection (Grid)
        grid_x = 50
        grid_y = 100
        image_size = 100
        padding = 20
        grid_cols = 3  # Number of columns of Pokémon
        grid_rows = (len(available_pokemon) + grid_cols - 1) // grid_cols  # Calculate number of rows

        while selected_pokemon is None:
            screen.fill((255, 255, 255))
            title_text = font.render("Choose your Pokémon", True, (0, 0, 0))
            screen.blit(title_text, (300, 50))

            # Loop through the available Pokémon and display them as images
            for index, pokemon in enumerate(available_pokemon):
                image_path = f"assets/pokemon/{pokemon.name.lower()}.png"
                try:
                    pokemon_image = pygame.image.load(image_path)
                    pokemon_image = pygame.transform.scale(pokemon_image, (image_size, image_size))
                except FileNotFoundError:
                    pokemon_image = None

                # Calculate position in the grid
                row = index // grid_cols
                col = index % grid_cols
                button_x = grid_x + col * (image_size + padding)
                button_y = grid_y + row * (image_size + padding)

                # Draw the Pokémon image on the screen
                if pokemon_image:
                    screen.blit(pokemon_image, (button_x, button_y))

                # Check if the player is hovering over the image
                mouse_x, mouse_y = pygame.mouse.get_pos()
                is_hovered = button_x <= mouse_x <= button_x + image_size and button_y <= mouse_y <= button_y + image_size

                button_color = (0, 180, 0) if is_hovered else (0, 255, 0)
                pygame.draw.rect(screen, button_color, (button_x, button_y, image_size, image_size), 3)

            pygame.display.flip()
            clock.tick(30)
            
            # Handle events to select a Pokémon
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for index, pokemon in enumerate(available_pokemon):
                        row = index // grid_cols
                        col = index % grid_cols
                        button_x = grid_x + col * (image_size + padding)
                        button_y = grid_y + row * (image_size + padding)
                        if button_x <= mouse_x <= button_x + image_size and button_y <= mouse_y <= button_y + image_size:
                            selected_pokemon = pokemon
                            break

        return selected_pokemon

    def start_battle(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        background_image = pygame.image.load("assets/background/battle_background.jpg")
        font = pygame.font.Font(None, 36)
        clock = pygame.time.Clock()
        
        while self.running:
            screen.blit(background_image, (0, 0))
            self.player_pokemon.draw(screen, x=50, y=300, is_player=True)
            self.opponent_pokemon.draw(screen, x=500, y=100, is_player=False)
            self.player_pokemon.draw_hp_bar(screen, x=50, y=250)
            self.opponent_pokemon.draw_hp_bar(screen, x=500, y=50)
            self.display_moves(screen)
            
            message_box = pygame.Rect(50, 400, 700, 40)
            pygame.draw.rect(screen, (255, 255, 255), message_box)
            message_text = font.render(self.message, True, (0, 0, 0))
            screen.blit(message_text, (60, 410))
            
            pygame.display.flip()
            clock.tick(30)
            
            if pygame.time.get_ticks() - self.message_start_time >= self.message_duration and not self.waiting_for_acknowledgment:
                self.message = ""

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the battle is over or we're waiting for acknowledgment, allow user to continue
                    if self.waiting_for_acknowledgment:
                        self.running = False  # End the game or restart battle logic
                    elif self.player_turn:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        for index, move in enumerate(self.player_pokemon.moves):
                            button_x = 50 + (index % 2) * 310
                            button_y = 450 + (index // 2) * 50
                            if button_x <= mouse_x <= button_x + 300 and button_y <= mouse_y <= button_y + 40:
                                self.handle_attack(screen, move)
            
            if not self.player_turn:
                self.opponent_turn(screen)
    
    def display_end_screen(self, screen):
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 48)
        text = font.render(self.message, True, (255, 255, 255))
        screen.blit(text, (200, 300))
        pygame.display.flip()
