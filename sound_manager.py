# Exemple de fonction utilitaire à placer dans un module commun ou en haut de vos fichiers
import pygame
pygame.mixer.init()  # S'assure que le mixer est initialisé

select_sound = pygame.mixer.Sound("assets/sounds/select.mp3")

def play_select_sound():
    select_sound.play()