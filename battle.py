import pygame
import random
from pokemon import Pokemon

class Battle:
    def __init__(self, player_pokemon, opponent_pokemon):
        self.player_pokemon = player_pokemon
        self.opponent_pokemon = opponent_pokemon
        self.running = True
        self.player_turn = True
        self.message = ""
        self.message_duration = 3000  # Duration to display message
        self.message_start_time = 0  # When to start showing message

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
            self.message_start_time = pygame.time.get_ticks()  # Record the time when the message started
            
            # Animate the player's attack
            self.player_pokemon.animate_attack(screen, 50, 300)
            self.player_pokemon.attack(move, self.opponent_pokemon)
            self.player_turn = False

            if self.opponent_pokemon.is_fainted():
                self.message = f"{self.opponent_pokemon.name} fainted! You win!"
                self.running = False
                return
    
    def opponent_turn(self, screen):
        if pygame.time.get_ticks() - self.message_start_time >= self.message_duration:
            opponent_move = random.choice(self.opponent_pokemon.moves)
            self.message = f"{self.opponent_pokemon.name} used {opponent_move}!"
            self.message_start_time = pygame.time.get_ticks()  # Record time for opponent's message
            
            # Animate the opponent's attack
            self.opponent_pokemon.animate_attack(screen, 500, 100)
            self.opponent_pokemon.attack(opponent_move, self.player_pokemon)

            if self.player_pokemon.is_fainted():
                self.message = f"{self.player_pokemon.name} fainted! You lose!"
                self.running = False
            else:
                self.player_turn = True  # Switch back to player's turn

    def start_battle(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        background_image = pygame.image.load("assets/background/battle_background.jpg")
        font = pygame.font.Font(None, 36)
        clock = pygame.time.Clock()
        
        while self.running:
            # Draw the background and Pokémon images
            screen.blit(background_image, (0, 0))
            self.player_pokemon.draw(screen, x=50, y=300, is_player=True)
            self.opponent_pokemon.draw(screen, x=500, y=100, is_player=False)
            self.player_pokemon.draw_hp_bar(screen, x=50, y=250)
            self.opponent_pokemon.draw_hp_bar(screen, x=500, y=50)
            self.display_moves(screen)
            
            # Display message (win/loss or action)
            message_box = pygame.Rect(50, 400, 700, 40)
            pygame.draw.rect(screen, (255, 255, 255), message_box)
            message_text = font.render(self.message, True, (0, 0, 0))
            screen.blit(message_text, (60, 410))
            
            pygame.display.flip()
            clock.tick(30)
            
            # Check if the message time is over and clear it if needed
            if pygame.time.get_ticks() - self.message_start_time >= self.message_duration:
                self.message = ""  # Clear message after the duration

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN and self.player_turn:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for index, move in enumerate(self.player_pokemon.moves):
                        button_x = 50 + (index % 2) * 310
                        button_y = 450 + (index // 2) * 50
                        if button_x <= mouse_x <= button_x + 300 and button_y <= mouse_y <= button_y + 40:
                            self.handle_attack(screen, move)
            
            # Opponent's turn if it's not the player's turn
            if not self.player_turn:
                self.opponent_turn(screen)

    def display_end_screen(self, screen):
        """Show the final result of the battle before quitting."""
        screen.fill((0, 0, 0))  # Black background
        font = pygame.font.Font(None, 48)
        text = font.render(self.message, True, (255, 255, 255))
        screen.blit(text, (200, 300))
        pygame.display.flip()
