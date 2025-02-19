import pygame
import json
import math
from pokemon import Pokemon

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

    # On charge tous les Pokémon
    pokemons = load_pokemons("pokemons.json")

    font = pygame.font.SysFont("arial", 20)

    # Index du Pokémon sélectionné
    selected_index = 0

    # Espace vertical entre chaque Pokémon
    spacing = 80

    # Hauteur totale de la liste (nombre de Pokémon × espacement)
    list_height = len(pokemons) * spacing
    # Hauteur de la fenêtre
    window_height = 600
    # Le scroll maximal (si la liste dépasse la fenêtre)
    max_scroll = max(0, list_height - window_height)

    # Offset de défilement actuel (affecté par le "slide")
    scroll_offset = 0.0
    # Offset cible (on fait un slide vers cette valeur)
    target_offset = 0.0

    # Vitesse de défilement quand on utilise flèches / molette
    scroll_speed = 1.0  # plus cette valeur est grande, plus le slide est rapide

    running = True
    while running:
        dt = clock.tick(60)  # dt = millisecondes écoulées depuis la dernière frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # Flèches haut/bas pour changer la sélection
                if event.key == pygame.K_UP:
                    selected_index = max(0, selected_index - 1)
                elif event.key == pygame.K_DOWN:
                    selected_index = min(len(pokemons) - 1, selected_index + 1)

                # On recalcule la position cible pour que l’élément sélectionné soit ~au milieu
                target_offset = selected_index * spacing - window_height // 2
                # On borne l’offset pour éviter de scroller trop loin
                target_offset = max(0, min(target_offset, max_scroll))

            elif event.type == pygame.MOUSEWHEEL:
                # Si vous voulez aussi scroller la liste à la molette
                # event.y > 0 => molette haut
                # event.y < 0 => molette bas
                target_offset -= event.y * 40  # 40 = pas de défilement à la molette
                target_offset = max(0, min(target_offset, max_scroll))

        # --- Mise à jour du scroll_offset (slide en douceur) ---
        # On fait une interpolation linéaire ou exponentielle pour un effet "smooth"
        # Par exemple : offset += (target - offset) * 0.2
        # Le coefficient 0.2 détermine la "vitesse" du slide
        scroll_offset += (target_offset - scroll_offset) * 0.2

        # Efface l'écran en noir
        screen.fill((0, 0, 0))

        # ========================
        # 1) Affichage de la liste
        # ========================
        y = 20 - scroll_offset
        list_x = 0  # On affiche la liste sur la gauche
        for i, p in enumerate(pokemons):
            # On redimensionne l'image en 64×64 pour la cohérence
            sprite = p.front_image
            if sprite is not None:
                sprite = pygame.transform.scale(sprite, (64, 64))
                screen.blit(sprite, (list_x + 20, y))

            # Couleur du nom : jaune si sélectionné, blanc sinon
            color = (255, 255, 0) if i == selected_index else (255, 255, 255)
            text_surface = font.render(p.name.capitalize(), True, color)
            screen.blit(text_surface, (list_x + 100, y + 20))

            # On peut aussi surligner la sélection avec un rectangle
            # if i == selected_index:
            #     highlight_rect = pygame.Rect(list_x, y, 300, spacing)
            #     pygame.draw.rect(screen, (255, 255, 255), highlight_rect, 2)

            y += spacing

        # =============================
        # 2) Affichage des détails à droite
        # =============================
        # On réserve par exemple la zone de droite (x >= 300) pour afficher les stats
        details_x = 320
        # Récupération du Pokémon sélectionné
        current_pokemon = pokemons[selected_index]
        # On dessine son sprite en plus grand (ex : 150×150)
        if current_pokemon.front_image:
            big_sprite = pygame.transform.scale(current_pokemon.front_image, (150, 150))
            screen.blit(big_sprite, (details_x, 50))

        # Affichage du nom + ID + type(s)
        info_lines = []
        info_lines.append(f"{current_pokemon.name.capitalize()} (ID: {current_pokemon.id})")
        # Types
        types_str = ", ".join(current_pokemon.types)
        info_lines.append(f"Type: {types_str}")
        # Stats
        info_lines.append("Stats:")
        for stat_name, stat_value in current_pokemon.stats.items():
            info_lines.append(f"  {stat_name.upper()}: {stat_value}")
        # Moves (on en affiche seulement quelques-uns, par exemple)
        moves_preview = ", ".join(current_pokemon.moves[:5])
        info_lines.append(f"Moves: {moves_preview} {'...' if len(current_pokemon.moves)>5 else ''}")

        # On dessine ces lignes
        line_y = 220
        for line in info_lines:
            text_surf = font.render(line, True, (255, 255, 255))
            screen.blit(text_surf, (details_x, line_y))
            line_y += 30

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
