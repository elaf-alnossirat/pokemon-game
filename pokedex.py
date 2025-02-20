import pygame
import json
import math
from pokemon import Pokemon
import sound_manager  # Import pour jouer le son de sélection

def load_pokemons(filepath):
    """Charge le JSON et crée une liste de Pokémon."""
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)
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
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pokedex - Liste et stats")
    clock = pygame.time.Clock()

    try:
        background = pygame.image.load("assets/pokedex_background.jpg").convert()
        background = pygame.transform.scale(background, (800, 600))
    except Exception as e:
        print("Erreur de chargement de l'image de fond:", e)
        background = None

    pokemons = load_pokemons("pokemons.json")
    font = pygame.font.SysFont("arial", 20)

    # Index du Pokémon sélectionné
    selected_index = 0

    # Espace vertical entre chaque Pokémon
    spacing = 80

    # Hauteur totale de la liste (nombre de Pokémon × espacement)
    list_height = len(pokemons) * spacing
    window_height = 600
    max_scroll = max(0, list_height - window_height)

    # Offset de défilement actuel (pour le slide) et cible
    scroll_offset = 0.0
    target_offset = 0.0

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # Retour au menu principal si la touche Échap est pressée
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    new_index = max(0, selected_index - 1)
                    if new_index != selected_index:
                        selected_index = new_index
                        sound_manager.play_select_sound()
                elif event.key == pygame.K_DOWN:
                    new_index = min(len(pokemons) - 1, selected_index + 1)
                    if new_index != selected_index:
                        selected_index = new_index
                        sound_manager.play_select_sound()
                # Recalcul du target_offset pour centrer le Pokémon sélectionné
                target_offset = selected_index * spacing - window_height // 2
                target_offset = max(0, min(target_offset, max_scroll))

            elif event.type == pygame.MOUSEWHEEL:
                target_offset -= event.y * 40  # pas de défilement
                target_offset = max(0, min(target_offset, max_scroll))
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # On considère que la liste des Pokémon est dans la partie gauche (x < 200)
                if mouse_x < 200:
                    for i, p in enumerate(pokemons):
                        item_y = 20 - scroll_offset + i * spacing
                        # Zone de clic approximative : le sprite est affiché entre x=20 et x=120, et sur une hauteur de 64 pixels
                        if 20 <= mouse_x <= 120 and item_y <= mouse_y <= item_y + 64:
                            if i != selected_index:
                                selected_index = i
                                sound_manager.play_select_sound()
                            break

        # Animation fluide du scroll
        scroll_offset += (target_offset - scroll_offset) * 0.2

        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((0, 0, 0))

        # Affichage de la liste des Pokémon à gauche
        y = 20 - scroll_offset
        list_x = 0
        for i, p in enumerate(pokemons):
            # Affichage du sprite redimensionné en 64x64
            sprite = p.front_image
            if sprite is not None:
                sprite = pygame.transform.scale(sprite, (64, 64))
                screen.blit(sprite, (list_x + 20, y))
            # Le nom du Pokémon s'affiche en jaune s'il est sélectionné, sinon en noir
            color = (255, 255, 0) if i == selected_index else (0, 0, 0)
            text_surface = font.render(p.name.capitalize(), True, color)
            screen.blit(text_surface, (list_x + 100, y + 20))
            y += spacing

        # Affichage des détails du Pokémon sélectionné à droite
        details_x = 320
        current_pokemon = pokemons[selected_index]
        if current_pokemon.front_image:
            big_sprite = pygame.transform.scale(current_pokemon.front_image, (150, 150))
            screen.blit(big_sprite, (details_x, 50))
        info_lines = []
        info_lines.append(f"{current_pokemon.name.capitalize()} (ID: {current_pokemon.id})")
        types_str = ", ".join(current_pokemon.types)
        info_lines.append(f"Type: {types_str}")
        info_lines.append("Stats:")
        for stat_name, stat_value in current_pokemon.stats.items():
            info_lines.append(f"  {stat_name.upper()}: {stat_value}")
        moves_preview = ", ".join(current_pokemon.moves[:5])
        info_lines.append(f"Moves: {moves_preview} {'...' if len(current_pokemon.moves) > 5 else ''}")

        line_y = 220
        for line in info_lines:
            text_surf = font.render(line, True, (255, 255, 255))
            screen.blit(text_surf, (details_x, line_y))
            line_y += 30

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
