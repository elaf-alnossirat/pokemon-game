import pygame
import random
import sys
from pokemon import Pokemon
from battle import Battle
from main_menu import MainMenu
from pokedex import main as show_pokedex  # Import the Pokédex function

class Game:
    def __init__(self):
        self.pokemons = self.load_pokemons("pokemons.json")
        self.main_menu = MainMenu()
        self.selected_pokemon = None
        self.scroll_offset = 0

    def load_pokemons(self, filepath):
        """Load Pokémon data from a JSON file."""
        import json
        with open(filepath) as file:
            data = json.load(file)

        pokemons = []
        for p in data["pokemon"]:
            pokemons.append(Pokemon(
                id=p["id"],
                name=p["name"],
                base_experience=p["base_experience"],
                types=p["types"],
                stats=p["stats"],
                abilities=p["abilities"],
                moves=p["moves"],
                sprites=p["sprites"]
            ))

        return pokemons

    def choose_pokemon(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Choose Your Pokémon")
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("arial", 20)

        spacing_x, spacing_y = 200, 180
        start_x, start_y = 50, 50
        rows, cols = 3, 3  # Grid layout
        max_scroll = max(0, (len(self.pokemons) // cols) * spacing_y - 600)

        running = True
        while running:
            screen.fill((0, 0, 0))
            for index, pokemon in enumerate(self.pokemons):
                row = index // cols
                col = index % cols
                x = start_x + col * spacing_x
                y = start_y + row * spacing_y - self.scroll_offset

                if 0 <= y <= 600:  # Only draw if visible
                    sprite = pygame.image.load(pokemon.sprites["front_default"])
                    sprite = pygame.transform.scale(sprite, (100, 100))
                    screen.blit(sprite, (x, y))
                    text_surface = font.render(pokemon.name, True, (255, 255, 255))
                    screen.blit(text_surface, (x + 10, y + 110))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for index, pokemon in enumerate(self.pokemons):
                        row = index // cols
                        col = index % cols
                        x = start_x + col * spacing_x
                        y = start_y + row * spacing_y - self.scroll_offset
                        if x <= mouse_x <= x + 100 and y <= mouse_y <= y + 100:
                            self.selected_pokemon = pokemon
                            running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.scroll_offset = max(0, self.scroll_offset - 40)
                    elif event.key == pygame.K_DOWN:
                        self.scroll_offset = min(max_scroll, self.scroll_offset + 40)

    def start_battle(self):
        # Reset the selected Pokemon to force selection for each new battle
        self.selected_pokemon = None
        
        # Now choose a Pokemon (this will always prompt for selection)
        self.choose_pokemon()
        
        # Choose a random opponent
        opponent_pokemon = random.choice([p for p in self.pokemons if p != self.selected_pokemon])
        
        # Create and start battle
        battle = Battle(available_pokemon=[self.selected_pokemon], opponent_pokemon=opponent_pokemon)
        battle.start_battle()
        
        # Important: DON'T quit the display - just reinitialize the screen with the correct settings
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Pokémon Game")
        
        return

    def show_pokedex(self):
        show_pokedex()  # Call the Pokédex screen function
        # Ensure pygame display is properly reset for the main menu
        pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Pokémon Game")

    def run(self):
        running = True
        while running:
            selected_option = self.main_menu.show()

            if selected_option == "start":
                self.start_battle()
                # Reset the main menu for next use
                self.main_menu = MainMenu()
            elif selected_option == "pokedex":
                self.show_pokedex()
                # Reset the main menu for next use
                self.main_menu = MainMenu()
            elif selected_option == "quit":
                running = False
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()