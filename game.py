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
    
    # Choose two Pokémon for battle (player vs opponent)
    player_pokemon = pokemons[0]  # Bulbasaur (example)
    opponent_pokemon = pokemons[3]  # Charmander (example)

    print(f"You chose {player_pokemon.name}. Your opponent chose {opponent_pokemon.name}.")
    
    battle = Battle(player_pokemon=player_pokemon,
                    opponent_pokemon=opponent_pokemon)
    
    battle.start_battle()


if __name__ == "__main__":
    main()
