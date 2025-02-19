import pygame
import random

# Type Effectiveness Chart
TYPE_EFFECTIVENESS = {
    "fire": {"grass": 2.0, "water": 0.5, "fire": 0.5},
    "water": {"fire": 2.0, "grass": 0.5, "water": 0.5},
    "grass": {"water": 2.0, "fire": 0.5, "grass": 0.5}
}


class Pokemon:
    def __init__(self, id, name, base_experience, types, stats, abilities, moves, sprites):
        self.id = id
        self.name = name
        self.base_experience = base_experience
        self.types = [t["type"] for t in types]
        self.stats = stats
        self.hp = stats["hp"]
        self.max_hp = stats["hp"]
        self.attack_stat = stats["attack"]
        self.defense_stat = stats["defense"]
        self.abilities = abilities
        self.moves = moves
        self.sprites = sprites

        # Load images
        try:
            self.front_image = pygame.image.load(sprites["front_default"])
            self.back_image = pygame.image.load(sprites["back_default"])
        except FileNotFoundError:
            print(f"Error: Image files for {self.name} not found!")
            # Fallback to placeholder images if not found
            self.front_image = pygame.Surface((100, 100))  # Placeholder size
            self.back_image = pygame.Surface((100, 100))  # Placeholder size
            pygame.draw.rect(self.front_image, (200, 200, 200), self.front_image.get_rect())  # Placeholder color
            pygame.draw.rect(self.back_image, (200, 200, 200), self.back_image.get_rect())  # Placeholder color

    def attack(self, move, target):
        """Perform an attack with type effectiveness and stat-based damage."""
        if move not in self.moves:
            print(f"{self.name} doesn't know {move}!")
            return False

        # Base damage using stats
        base_damage = random.randint(15, 30) + (self.attack_stat // 5) - (target.defense_stat // 10)

        # Type effectiveness multiplier
        attacker_type = self.types[0]  # Assume first type for simplicity
        defender_type = target.types[0]
        type_multiplier = TYPE_EFFECTIVENESS.get(attacker_type, {}).get(defender_type, 1.0)

        # Final damage calculation
        damage = int(base_damage * type_multiplier)
        target.hp = max(0, target.hp - damage)

        # Display attack details
        print(f"{self.name} used {move}! It dealt {damage} damage to {target.name}.")

        if type_multiplier > 1:
            print("It's super effective!")
        elif type_multiplier < 1:
            print("It's not very effective...")

        if target.hp == 0:
            print(f"{target.name} fainted!")
            return True

        return False

    def is_fainted(self):
        """Check if the Pokémon has fainted."""
        return self.hp <= 0

    def draw(self, screen, x, y, is_player):
        """Draw the Pokémon on the screen."""
        if is_player:
            screen.blit(self.back_image, (x, y))
        else:
            screen.blit(self.front_image, (x, y))
    def draw_hp_bar(self, screen, x, y, width=200, height=20):
            # Calculate the current HP percentage
            hp_percentage = self.hp / self.max_hp

            # Smoothly transition the displayed HP
            if not hasattr(self, 'displayed_hp'):
                self.displayed_hp = self.hp
            else:
                if self.displayed_hp > self.hp:
                    self.displayed_hp -= max(1, (self.displayed_hp - self.hp) / 10)
                elif self.displayed_hp < self.hp:
                    self.displayed_hp += max(1, (self.hp - self.displayed_hp) / 10)

            displayed_hp_percentage = self.displayed_hp / self.max_hp

            # Draw the background of the HP bar (empty part)
            pygame.draw.rect(screen, (50, 50, 50), (x, y, width, height), border_radius=10)

            # Draw the HP bar with a gradient
            for i in range(int(displayed_hp_percentage * width)):
                color = self.get_hp_bar_color(displayed_hp_percentage)
                pygame.draw.rect(screen, color, (x + i, y, 1, height), border_radius=10)

            # Add a glow effect around the HP bar
            glow_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (255, 255, 255, 50), (0, 0, width, height), border_radius=10)
            screen.blit(glow_surface, (x - 2, y - 2))

            # Display HP text overlay
            font = pygame.font.Font(None, 18)
            hp_text = font.render(f"{int(self.displayed_hp)}/{self.max_hp}", True, (255, 255, 255))
            screen.blit(hp_text, (x + width // 2 - hp_text.get_width() // 2, y + height // 2 - hp_text.get_height() // 2))

    def get_hp_bar_color(self, hp_percentage):
            # Gradient from green to red based on HP percentage
            if hp_percentage > 0.5:
                return (int(255 * (1 - hp_percentage) * 2), 255, 0)  # Green to yellow
            else:
                return (255, int(255 * hp_percentage * 2), 0)  # Yellow to red

    def take_damage(self, damage):
            self.hp = max(0, self.hp - damage)
            # Trigger a damage flash effect
            self.damage_flash_start = pygame.time.get_ticks()
            
    def animate_attack(self, screen, x_start, y_start):
        """Simple attack animation: shake or jump."""
        for _ in range(3):
            screen.fill((255, 255, 255))  # Clear screen with white background
            offset_x = random.randint(-10, 10)
            offset_y = random.randint(-10, 10)

            # Shake effect: Move sprite slightly left/right/up/down
            screen.blit(self.front_image if x_start > 400 else self.back_image,
                        (x_start + offset_x, y_start + offset_y))

            pygame.display.flip()
            pygame.time.delay(100)

    def flash_red(self, screen, x_start, y_start):
        """Flash red briefly when hit."""
        for _ in range(2):  # Flash twice
            # Red overlay effect
            red_overlay = pygame.Surface((self.front_image.get_width(), self.front_image.get_height()))
            red_overlay.fill((255, 0, 0))  # Red color

            if x_start > 400:  # Opponent's Pokémon (front sprite)
                screen.blit(self.front_image.copy(), (x_start, y_start))
                screen.blit(red_overlay.set_alpha(128), (x_start, y_start))
            else:  # Player's Pokémon (back sprite)
                screen.blit(self.back_image.copy(), (x_start, y_start))
                screen.blit(red_overlay.set_alpha(128), (x_start, y_start))

            pygame.display.flip()
            pygame.time.delay(100)  # Pause briefly between flashes



