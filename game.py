import json
from pokemon import Pokemon
from battle import Battle

def load_pokemons(filepath):
    """Load Pokémon data from a JSON file."""
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

def main():
    pokemons = load_pokemons("pokemons.json")

    # Randomly choose an opponent's Pokémon
    import random
    opponent_pokemon = random.choice(pokemons)

    # Create a battle instance (player will choose their Pokémon)
    battle = Battle(available_pokemon=pokemons, opponent_pokemon=opponent_pokemon)

    # Start the battle
    battle.start_battle()

if __name__ == "__main__":
    main()
