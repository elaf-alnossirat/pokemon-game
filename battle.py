import pygame
import random
import math
from pokemon import Pokemon
import sound_manager  # Pour jouer le son de sélection

class Battle:
    def __init__(self, available_pokemon, opponent_pokemon):
        self.player_pokemon = self.choose_pokemon(available_pokemon)
        self.opponent_pokemon = opponent_pokemon
        self.running = True
        self.player_turn = True
        self.message = ""
        self.message_duration = 3000
        self.message_start_time = 0
        self.battle_over = False
        self.victor = None
        self.result_displayed = False
        self.animation_progress = 0
        self.animation_speed = 0.02
        self.particles = []

    def display_moves(self, screen):
        try:
            font = pygame.font.Font("assets/fonts/Exo2-Medium.ttf", 24)
        except FileNotFoundError:
            font = pygame.font.SysFont("arial", 24)
        
        move_area_rect = pygame.Rect(50, 470, 700, 100)
        move_panel = pygame.Surface((move_area_rect.width, move_area_rect.height), pygame.SRCALPHA)
        move_panel.fill((10, 40, 10, 180))
        screen.blit(move_panel, move_area_rect)
        
        header_font = pygame.font.Font(None, 22)
        header_text = header_font.render("CHOOSE A MOVE", True, (180, 255, 180))
        screen.blit(header_text, (move_area_rect.centerx - header_text.get_width()//2, move_area_rect.y + 8))
        
        button_width = 240
        button_height = 40
        button_spacing = 30
        buttons_start_y = move_area_rect.y + 30
        
        total_width = (button_width * 2) + button_spacing
        start_x = move_area_rect.x + (move_area_rect.width - total_width) // 2
        
        for index, move in enumerate(self.player_pokemon.moves):
            button_x = start_x + (index % 2) * (button_width + button_spacing)
            button_y = buttons_start_y + (index // 2) * (button_height + 10)
            
            mouse_x, mouse_y = pygame.mouse.get_pos()
            is_hovered = button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height
            
            self.draw_neon_button(screen, button_x, button_y, button_width, button_height, move.capitalize(), font, is_hovered)

    def draw_neon_button(self, screen, x, y, width, height, text, font, is_hovered=False):
        if is_hovered:
            for i in range(2, 0, -1):
                glow_alpha = 100 - i * 30
                glow_surf = pygame.Surface((width + i*4, height + i*4), pygame.SRCALPHA)
                glow_color = (50, 255, 50, glow_alpha)
                pygame.draw.rect(glow_surf, glow_color, (0, 0, width + i*4, height + i*4), border_radius=10)
                screen.blit(glow_surf, (x - i*2, y - i*2))
            button_color = (20, 100, 20)
            border_color = (50, 255, 50)
        else:
            button_color = (10, 60, 10)
            border_color = (0, 200, 0)
        
        pygame.draw.rect(screen, button_color, (x, y, width, height), border_radius=10)
        pygame.draw.rect(screen, border_color, (x, y, width, height), width=1, border_radius=10)
        
        highlight_rect = pygame.Rect(x+2, y+2, width-4, (height-4)//2)
        highlight_surf = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
        highlight_color = (255, 255, 255, 20)
        pygame.draw.rect(highlight_surf, highlight_color, (0, 0, highlight_rect.width, highlight_rect.height), border_radius=8)
        screen.blit(highlight_surf, highlight_rect)
        
        text_shadow = font.render(text, True, (0, 0, 0))
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        shadow_rect = text_rect.copy()
        shadow_rect.x += 1
        shadow_rect.y += 1
        
        screen.blit(text_shadow, shadow_rect)
        screen.blit(text_surface, text_rect)
    
    def handle_attack(self, screen, move):
        if self.player_turn:
            self.message = f"{self.player_pokemon.name} used {move}!"
            self.message_start_time = pygame.time.get_ticks()
            
            flash_surface = pygame.Surface((800, 600), pygame.SRCALPHA)
            flash_surface.fill((255, 255, 255, 100))
            screen.blit(flash_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(100)
            
            self.player_pokemon.attack(move, self.opponent_pokemon)
            self.player_turn = False

            if self.opponent_pokemon.is_fainted():
                self.message = f"{self.opponent_pokemon.name} fainted! You win!"
                self.battle_over = True
                self.victor = "player"
                self.initialize_particles()
                return
    
    def opponent_turn(self, screen):
        if pygame.time.get_ticks() - self.message_start_time >= self.message_duration:
            pygame.time.delay(500)
            opponent_move = random.choice(self.opponent_pokemon.moves)
            self.message = f"{self.opponent_pokemon.name} used {opponent_move}!"
            self.message_start_time = pygame.time.get_ticks()
            self.opponent_pokemon.attack(opponent_move, self.player_pokemon)
            if self.player_pokemon.is_fainted():
                self.message = f"{self.player_pokemon.name} fainted! You lose!"
                self.battle_over = True
                self.victor = "opponent"
            else:
                self.player_turn = True

    def choose_pokemon(self, available_pokemon):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        font = pygame.font.Font(None, 36)
        clock = pygame.time.Clock()
        selected_pokemon = None

        grid_x = 50
        grid_y = 100
        image_size = 100
        padding = 20
        grid_cols = 3

        while selected_pokemon is None:
            screen.fill((255, 255, 255))
            title_text = font.render("Choose your Pokémon", True, (0, 0, 0))
            screen.blit(title_text, (300, 50))

            for index, pokemon in enumerate(available_pokemon):
                image_path = f"assets/pokemon/{pokemon.name.lower()}.png"
                try:
                    pokemon_image = pygame.image.load(image_path)
                    pokemon_image = pygame.transform.scale(pokemon_image, (image_size, image_size))
                except FileNotFoundError:
                    pokemon_image = None

                row = index // grid_cols
                col = index % grid_cols
                button_x = grid_x + col * (image_size + padding)
                button_y = grid_y + row * (image_size + padding)

                if pokemon_image:
                    screen.blit(pokemon_image, (button_x, button_y))

                mouse_x, mouse_y = pygame.mouse.get_pos()
                is_hovered = button_x <= mouse_x <= button_x + image_size and button_y <= mouse_y <= button_y + image_size

                button_color = (0, 180, 0) if is_hovered else (0, 255, 0)
                pygame.draw.rect(screen, button_color, (button_x, button_y, image_size, image_size), 3)

            pygame.display.flip()
            clock.tick(30)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for index, pokemon in enumerate(available_pokemon):
                        row = index // grid_cols
                        col = index % grid_cols
                        button_x = grid_x + col * (image_size + padding)
                        button_y = grid_y + row * (image_size + padding)
                        if button_x <= mouse_x <= button_x + image_size and button_y <= mouse_y <= button_y + image_size:
                            sound_manager.play_select_sound()
                            selected_pokemon = pokemon
                            break

        return selected_pokemon

    def initialize_particles(self):
        self.particles = []
        if self.victor == "player":
            for _ in range(100):
                particle = {
                    'x': random.randint(0, 800),
                    'y': random.randint(-50, 0),
                    'size': random.randint(5, 15),
                    'speed': random.uniform(2, 6),
                    'color': random.choice([
                        (255, 215, 0),
                        (255, 255, 255),
                        (0, 255, 255),
                        (255, 105, 180),
                    ])
                }
                self.particles.append(particle)

    def update_particles(self):
        for particle in self.particles[:]:
            particle['y'] += particle['speed']
            if particle['y'] > 600:
                self.particles.remove(particle)
            elif random.random() < 0.02:
                self.particles.remove(particle)

    def draw_particles(self, screen):
        for particle in self.particles:
            pygame.draw.circle(screen, particle['color'], (int(particle['x']), int(particle['y'])), particle['size'])

    def display_modern_result_screen(self, screen):
        self.result_displayed = True
        self.animation_progress = 0
        try:
            font_title = pygame.font.Font("assets/fonts/Exo2-Bold.ttf", 72)
            font_subtitle = pygame.font.Font("assets/fonts/Exo2-SemiBold.ttf", 36)
            font_stats = pygame.font.Font("assets/fonts/Exo2-Medium.ttf", 24)
            font_continue = pygame.font.Font("assets/fonts/Exo2-Regular.ttf", 20)
        except FileNotFoundError:
            font_title = pygame.font.SysFont("arial", 72, bold=True)
            font_subtitle = pygame.font.SysFont("arial", 36, bold=True)
            font_stats = pygame.font.SysFont("arial", 24)
            font_continue = pygame.font.SysFont("arial", 20)
        
        clock = pygame.time.Clock()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and self.animation_progress >= 0.95:
                    done = True
                if event.type == pygame.KEYDOWN and self.animation_progress >= 0.95:
                    done = True
            
            if self.animation_progress < 1.0:
                self.animation_progress += self.animation_speed
                self.animation_progress = min(1.0, self.animation_progress)
            
            screen.blit(pygame.image.load("assets/background/battle_background.jpg"), (0, 0))
            overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            
            if self.victor == "player":
                self.update_particles()
                self.draw_particles(screen)
            
            card_height = int(400 * min(1, self.animation_progress * 3.33))
            card_y = 300 - card_height // 2
            
            if self.victor == "player":
                card_color = (0, 0, 60)
                accent_color = (0, 191, 255)
                text_color = (255, 215, 0)
            else:
                card_color = (60, 0, 0)
                accent_color = (178, 34, 34)
                text_color = (255, 99, 71)
            
            card_rect = pygame.Rect(150, card_y, 500, card_height)
            pygame.draw.rect(screen, card_color, card_rect, border_radius=20)
            
            if self.animation_progress > 0.3:
                border_progress = min(1, (self.animation_progress - 0.3) * 3.33)
                border_width = int(5 * border_progress)
                if border_width > 0:
                    pygame.draw.rect(screen, accent_color, card_rect, width=border_width, border_radius=20)
            
            if self.animation_progress > 0.3:
                title_opacity = min(255, int(255 * min(1, (self.animation_progress - 0.3) * 3.33)))
                if self.victor == "player":
                    title_surface = font_title.render("VICTORY!", True, text_color)
                else:
                    title_surface = font_title.render("DEFEAT", True, text_color)
                title_surface.set_alpha(title_opacity)
                title_rect = title_surface.get_rect(center=(400, card_y + 70))
                screen.blit(title_surface, title_rect)
            
            if self.animation_progress > 0.6:
                stats_opacity = min(255, int(255 * min(1, (self.animation_progress - 0.6) * 5)))
                if self.victor == "player":
                    subtitle = f"{self.player_pokemon.name} defeated {self.opponent_pokemon.name}!"
                    stats1 = f"Your {self.player_pokemon.name} still has {self.player_pokemon.hp}/{self.player_pokemon.max_hp} HP"
                    stats2 = f"Experience gained: {random.randint(50, 150)}"
                else:
                    subtitle = f"{self.opponent_pokemon.name} defeated {self.player_pokemon.name}!"
                    stats1 = f"Opponent's {self.opponent_pokemon.name} has {self.opponent_pokemon.hp}/{self.opponent_pokemon.max_hp} HP left"
                    stats2 = "Better luck next time!"
                
                subtitle_surface = font_subtitle.render(subtitle, True, (255, 255, 255))
                subtitle_surface.set_alpha(stats_opacity)
                subtitle_rect = subtitle_surface.get_rect(center=(400, card_y + 140))
                screen.blit(subtitle_surface, subtitle_rect)
                
                stats1_surface = font_stats.render(stats1, True, (200, 200, 200))
                stats1_surface.set_alpha(stats_opacity)
                stats1_rect = stats1_surface.get_rect(center=(400, card_y + 200))
                screen.blit(stats1_surface, stats1_rect)
                
                stats2_surface = font_stats.render(stats2, True, (200, 200, 200))
                stats2_surface.set_alpha(stats_opacity)
                stats2_rect = stats2_surface.get_rect(center=(400, card_y + 240))
                screen.blit(stats2_surface, stats2_rect)
            
            if self.animation_progress > 0.8:
                button_opacity = min(255, int(255 * min(1, (self.animation_progress - 0.8) * 5)))
                button_rect = pygame.Rect(300, card_y + 300, 200, 50)
                button_color_with_alpha = list(accent_color)
                button_color_with_alpha.append(button_opacity)
                button_surface = pygame.Surface((200, 50), pygame.SRCALPHA)
                pygame.draw.rect(button_surface, button_color_with_alpha, pygame.Rect(0, 0, 200, 50), border_radius=25)
                screen.blit(button_surface, button_rect)
                continue_text = font_continue.render("CONTINUE", True, (255, 255, 255))
                continue_text.set_alpha(button_opacity)
                continue_rect = continue_text.get_rect(center=button_rect.center)
                screen.blit(continue_text, continue_rect)
                if self.animation_progress >= 1.0:
                    pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 0.5
                    pulse_size = int(5 * pulse)
                    if pulse_size > 0:
                        pygame.draw.rect(screen, (255, 255, 255, 100), 
                                        button_rect.inflate(pulse_size, pulse_size), 
                                        width=2, border_radius=25)
            
            pygame.display.flip()
            clock.tick(60)
        
        self.running = False
        return

    def start_battle(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Pokémon Battle")
        background_image = pygame.image.load("assets/background/battle_background.jpg")
        font = pygame.font.Font(None, 36)
        clock = pygame.time.Clock()

        player_pokemon_size = (200, 200)
        opponent_pokemon_size = (200, 200)
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.battle_over and self.player_turn:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        move_area_rect = pygame.Rect(50, 450, 700, 120)
                        buttons_start_y = move_area_rect.y + 35
                        button_width = 320
                        button_height = 60
                        button_spacing = 20
                        
                        for index, move in enumerate(self.player_pokemon.moves):
                            button_x = move_area_rect.x + 20 + (index % 2) * (button_width + button_spacing)
                            button_y = buttons_start_y + (index // 2) * (button_height + 5)
                            
                            if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                                sound_manager.play_select_sound()
                                self.handle_attack(screen, move)
                    elif self.battle_over and self.result_displayed:
                        self.running = False

            screen.blit(background_image, (0, 0))

            player_pokemon_image = pygame.image.load(f"assets/pokemon/{self.player_pokemon.name.lower()}.png")
            player_pokemon_image = pygame.transform.scale(player_pokemon_image, player_pokemon_size)
            screen.blit(player_pokemon_image, (50, 250))

            opponent_pokemon_image = pygame.image.load(f"assets/pokemon/{self.opponent_pokemon.name.lower()}.png")
            opponent_pokemon_image = pygame.transform.scale(opponent_pokemon_image, opponent_pokemon_size)
            screen.blit(opponent_pokemon_image, (500, 100))

            self.player_pokemon.draw_hp_bar(screen, x=50, y=220)
            self.opponent_pokemon.draw_hp_bar(screen, x=500, y=50)

            message_box = pygame.Rect(50, 400, 700, 40)
            pygame.draw.rect(screen, (0, 0, 0, 150), message_box, border_radius=10)
            pygame.draw.rect(screen, (100, 100, 255), message_box, width=2, border_radius=10)
            message_text = font.render(self.message, True, (255, 255, 255))
            screen.blit(message_text, (60, 410))

            if not self.battle_over:
                self.display_moves(screen)

            pygame.display.flip()
            clock.tick(30)

            if self.battle_over and not self.result_displayed:
                pygame.time.delay(1500)
                self.display_modern_result_screen(screen)

            if not self.player_turn and not self.battle_over:
                self.opponent_turn(screen)

        pygame.display.set_caption("Pokémon Game")
        return
