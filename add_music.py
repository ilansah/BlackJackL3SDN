#!/usr/bin/env python3
"""
Script pour appliquer toutes les modifications au jeu Blackjack de manière sûre.
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def add_music_to_main():
    """Ajoute le support de la musique à main.py"""
    main_path = os.path.join(BASE_DIR, "src", "main.py")
    
    with open(main_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Ajouter l'import de config_manager
    if "from config_manager import get_config_manager" not in content:
        content = content.replace(
            "from core.player import Player",
            "from core.player import Player\nfrom config_manager import get_config_manager"
        )
    
    # 2. Ajouter les variables de musique après _image_cache
    if "MUSIC_FILE" not in content:
        music_vars = '''
# Musique
MUSIC_FILE = os.path.join(os.path.dirname(__file__), "..", "Indochine - Jai demandé à la lune (Clip officiel).mp3")
music_enabled = True
music_volume = 0.5
'''
        content = content.replace(
            "_image_cache: dict[str, pygame.Surface] = {}",
            "_image_cache: dict[str, pygame.Surface] = {}" + music_vars
        )
    
    # 3. Modifier init_pygame pour charger la musique
    old_init = """def init_pygame():
    pygame.init()
    pygame.display.set_caption("Blackjack VIP Lounge")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    return screen, clock"""
    
    new_init = """def init_pygame():
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Blackjack VIP Lounge")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    # Charger et jouer la musique
    config = get_config_manager()
    global music_enabled, music_volume
    music_enabled = config.get('features.music_enabled', True)
    music_volume = config.get('features.music_volume', 0.5)
    
    if os.path.exists(MUSIC_FILE) and music_enabled:
        try:
            pygame.mixer.music.load(MUSIC_FILE)
            pygame.mixer.music.set_volume(music_volume)
            pygame.mixer.music.play(-1)  # -1 = loop infiniment
        except Exception as e:
            print(f"Erreur lors du chargement de la musique: {e}")
    
    return screen, clock"""
    
    content = content.replace(old_init, new_init)
    
    # 4. Modifier draw_settings_screen pour afficher le statut de la musique
    old_settings = '''def draw_settings_screen(screen: pygame.Surface, game: Game):
    screen.fill(COLOR_ROOM_BG)
    box = pygame.Rect(WIDTH//2 - 300, 100, 600, 500)
    pygame.draw.rect(screen, (30, 30, 35), box, border_radius=20)
    pygame.draw.rect(screen, COLOR_GOLD, box, 2, border_radius=20)
    
    draw_shadow_text(screen, "PARAMÈTRES", get_font("serif", 40, True), COLOR_GOLD, WIDTH//2, 150, center=True)
    
    lines = ["Son: ON", "Musique: OFF", "Difficulté: Normale", "Vitesse: x1"]
    for i, line in enumerate(lines):
        draw_shadow_text(screen, line, get_font("sans", 24), COLOR_TEXT_WHITE, WIDTH//2, 250 + i*50, center=True)
        
    draw_shadow_text(screen, "ESC pour retour", get_font("sans", 18), COLOR_TEXT_GREY, WIDTH//2, 550, center=True)'''
    
    new_settings = '''def draw_settings_screen(screen: pygame.Surface, game: Game):
    screen.fill(COLOR_ROOM_BG)
    box = pygame.Rect(WIDTH//2 - 300, 100, 600, 500)
    pygame.draw.rect(screen, (30, 30, 35), box, border_radius=20)
    pygame.draw.rect(screen, COLOR_GOLD, box, 2, border_radius=20)
    
    draw_shadow_text(screen, "PARAMÈTRES", get_font("serif", 40, True), COLOR_GOLD, WIDTH//2, 150, center=True)
    
    config = get_config_manager()
    music_status = "ON" if config.get('features.music_enabled', True) else "OFF"
    sound_status = "ON" if config.get('features.sound_enabled', False) else "OFF"
    
    lines = [
        f"Son: {sound_status}",
        f"Musique: {music_status} [M pour changer]",
        "Difficulté: Normale",
        "Vitesse: x1"
    ]
    for i, line in enumerate(lines):
        draw_shadow_text(screen, line, get_font("sans", 24), COLOR_TEXT_WHITE, WIDTH//2, 250 + i*50, center=True)
        
    draw_shadow_text(screen, "ESC pour retour", get_font("sans", 18), COLOR_TEXT_GREY, WIDTH//2, 550, center=True)'''
    
    content = content.replace(old_settings, new_settings)
    
    # 5. Ajouter le toggle de musique dans handle_input
    # Trouver la section KEYDOWN dans handle_input
    keydown_section = '''        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game.state == GameState.MENU: pygame.quit(); sys.exit()
                else: game.state = GameState.MENU'''
    
    new_keydown_section = '''        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game.state == GameState.MENU: pygame.quit(); sys.exit()
                else: game.state = GameState.MENU
            
            # Toggle musique dans les paramètres
            if event.key == pygame.K_m and game.state == GameState.SETTINGS:
                config = get_config_manager()
                new_state = config.toggle_feature('music_enabled')
                if new_state:
                    if os.path.exists(MUSIC_FILE):
                        try:
                            pygame.mixer.music.load(MUSIC_FILE)
                            pygame.mixer.music.set_volume(config.get('features.music_volume', 0.5))
                            pygame.mixer.music.play(-1)
                        except: pass
                else:
                    pygame.mixer.music.stop()'''
    
    content = content.replace(keydown_section, new_keydown_section)
    
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ main.py mis à jour avec support musique")

if __name__ == "__main__":
    print("Application des modifications pour la musique...")
    add_music_to_main()
    print("\n✅ Modifications appliquées avec succès!")
    print("\nInstructions:")
    print("- Appuyez sur M dans les paramètres pour activer/désactiver la musique")
    print("- La musique se lance automatiquement au démarrage si activée")
