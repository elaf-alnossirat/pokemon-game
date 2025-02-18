class Trainer:
    def __init__(self, name):
        self.name = name
        self.pokemon_team = []

    def add_pokemon(self, pokemon):
        """Add a Pokémon to the trainer's team."""
        if len(self.pokemon_team) < 6:
            self.pokemon_team.append(pokemon)
            print(f"{pokemon.name} was added to {self.name}'s team!")
        else:
            print("Team is full! Cannot add more Pokémon.")

    def choose_pokemon(self):
        """Choose a Pokémon from the team that has not fainted."""
        available_pokemon = [p for p in self.pokemon_team if not p.is_fainted()]
        
        if not available_pokemon:
            print(f"{self.name} has no available Pokémon!")
            return None
        
        # For simplicity, choose the first available Pokémon
        return available_pokemon[0]
