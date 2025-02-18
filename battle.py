import pygame
from pokemon import Pokemon


class Battle:
    def __init__(self, player_pokemon, opponent_pokemon):
        self.player_pokemon = player_pokemon
        self.opponent_pokemon = opponent_pokemon

    def display_moves(self, screen):
        """Display the player's moves as a menu."""
        font = pygame.font.Font(None, 36)
        
        move_box_x = 50
        move_box_y = 450
        move_box_width = 700
        move_box_height = 100
        
        # Draw background for moves menu
        pygame.draw.rect(screen, (200, 200, 200), (move_box_x - 10,
                                                   move_box_y - 10,
                                                   move_box_width,
                                                   move_box_height))
        
        # Display each move as a button-like text box
        for index, move in enumerate(self.player_pokemon.moves):
            # Calculate position for each move button
            button_x = move_box_x + (index % 2) * 350
            button_y = move_box_y + (index // 2) * 50

            # Draw the button background
            pygame.draw.rect(screen, (0, 0, 255), (button_x, button_y, 300, 40))  # Blue rectangle

            # Render the move name
            move_text = font.render(move.capitalize(), True, (255, 255, 255))  # White text
            screen.blit(move_text, (button_x + 10, button_y + 5))

    def start_battle(self):
        """Start a graphical battle using pygame."""
        
        # Initialize pygame
        pygame.init()
        
        # Screen dimensions and setup
        screen_width = 800
        screen_height = 600
        screen = pygame.display.set_mode((screen_width, screen_height))
        
        # Set up fonts and background image
        font = pygame.font.Font(None, 36)
        background_image = pygame.image.load("assets/background/battle_background.jpg")

        clock = pygame.time.Clock()
        
        running = True
        player_turn = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                    mouse_x, mouse_y = pygame.mouse.get_pos()  
                    
                    for index, move in enumerate(self.player_pokemon.moves):
                        button_x = 50 + (index % 2) * 350  
                        button_y = 450 + (index // 2) * 50  

                        if button_x <= mouse_x <= button_x + 300 and button_y <= mouse_y <= button_y + 40:
                            print(f"You selected {move}!")
                            self.player_pokemon.attack(move, self.opponent_pokemon)
                            player_turn = False
            
            if not player_turn:
                # Opponent's turn to attack after a delay
                pygame.time.delay(1000)
                opponent_move = self.opponent_pokemon.moves[0]  
                print(f"{self.opponent_pokemon.name} used {opponent_move}!")
                self.opponent_pokemon.attack(opponent_move, self.player_pokemon)
                player_turn = True
            
            # Draw everything on the screen
            screen.blit(background_image, (0, 0))  

            self.player_pokemon.draw(screen, x=50, y=300, is_player=True)
            self.opponent_pokemon.draw(screen, x=500, y=100, is_player=False)

            self.player_pokemon.draw_hp_bar(screen, x=50, y=250)
            self.opponent_pokemon.draw_hp_bar(screen, x=500, y=50)

            self.display_moves(screen)

            pygame.display.flip()
            clock.tick(30)
