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

    def start_battle(self):
        opponent_pokemon = random.choice(self.pokemons)
        battle = Battle(available_pokemon=self.pokemons, opponent_pokemon=opponent_pokemon)
        battle.start_battle()

    def show_pokedex(self):
        show_pokedex()  # Call the Pokédex screen function

    def run(self):
        while True:
            selected_option = self.main_menu.show()

            if selected_option == "start":
                self.start_battle()
            elif selected_option == "pokedex":
                self.show_pokedex()
            elif selected_option == "quit":
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
