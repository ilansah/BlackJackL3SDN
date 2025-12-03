#!/usr/bin/env python3
"""
Script pour améliorer les paramètres et implémenter le changement de couleur de table
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def update_settings():
    """Met à jour les paramètres avec des options plus utiles"""
    
    # 1. Mettre à jour settings.json
    settings_path = os.path.join(BASE_DIR, "config", "settings.json")
    with open(settings_path, 'r') as f:
        content = f.read()
    
    # Remplacer les anciens paramètres par de nouveaux
    new_settings = '''{
  "game": {
    "width": 1280,
    "height": 720,
    "fps": 60,
    "num_decks": 1,
    "animation_delay": 0.5
  },
  "cards": {
    "width": 100,
    "height": 145,
    "spacing": 20
  },
  "colors": {
    "bg": [0, 100, 0],
    "bg_dark": [20, 60, 20],
    "menu_bg": [15, 15, 40],
    "text": [255, 255, 255],
    "text_gold": [255, 215, 0],
    "win": [100, 255, 100],
    "lose": [255, 100, 100],
    "push": [255, 255, 100]
  },
  "timing": {
    "initial_deal_duration": 1.0,
    "dealer_reveal_duration": 1.0,
    "result_screen_duration": 3.0,
    "action_delay": 0.5
  },
  "difficulty": {
    "dealer_strategy": "standard"
  },
  "player": {
    "starting_balance": 1000,
    "min_bet": 5,
    "max_bet": 1000
  },
  "features": {
    "sound_enabled": false,
    "animations_enabled": true,
    "music_enabled": true,
    "music_volume": 0.5,
    "auto_save": true,
    "show_probabilities": false
  },
  "ui": {
    "card_back_style": "classic",
    "table_theme": "green",
    "show_balance": true,
    "dealer_speed": 1.0
  }
}'''
    
    with open(settings_path, 'w') as f:
        f.write(new_settings)
    
    print("✓ settings.json mis à jour")
    
    # 2. Mettre à jour draw_settings_screen dans main.py
    main_path = os.path.join(BASE_DIR, "src", "main.py")
    with open(main_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Trouver et remplacer la fonction draw_settings_screen
    new_draw_settings = '''def draw_settings_screen(screen: pygame.Surface, game: Game):
    screen.fill(COLOR_ROOM_BG)
    box = pygame.Rect(WIDTH//2 - 400, 80, 800, 560)
    pygame.draw.rect(screen, (30, 30, 35), box, border_radius=20)
    pygame.draw.rect(screen, COLOR_GOLD, box, 2, border_radius=20)
    
    draw_shadow_text(screen, "PARAMÈTRES", get_font("serif", 40, True), COLOR_GOLD, WIDTH//2, 120, center=True)
    
    config = get_config_manager()
    mouse_pos = pygame.mouse.get_pos()
    
    y_start = 200
    y_spacing = 60
    control_width = 200
    control_height = 40
    x_center = WIDTH//2 + 100
    
    controls = []
    
    # 1. Musique ON/OFF
    music_rect = pygame.Rect(x_center, y_start, control_width, control_height)
    music_on = config.get('features.music_enabled', True)
    music_hover = music_rect.collidepoint(mouse_pos)
    draw_toggle_button(screen, music_rect, music_on, "Musique", music_hover)
    controls.append(('toggle', 'features.music_enabled', music_rect))
    
    # 2. Volume de la musique
    volume_rect = pygame.Rect(x_center, y_start + y_spacing, control_width, control_height)
    volume = config.get('features.music_volume', 0.5)
    volume_hover = volume_rect.collidepoint(mouse_pos)
    draw_slider(screen, volume_rect, volume, 0.0, 1.0, "Volume", False, volume_hover)
    controls.append(('slider', 'features.music_volume', volume_rect, 0.0, 1.0))
    
    # 3. Sauvegarde auto ON/OFF
    auto_save_rect = pygame.Rect(x_center, y_start + y_spacing * 2, control_width, control_height)
    auto_save_on = config.get('features.auto_save', True)
    auto_save_hover = auto_save_rect.collidepoint(mouse_pos)
    draw_toggle_button(screen, auto_save_rect, auto_save_on, "Sauvegarde Auto", auto_save_hover)
    controls.append(('toggle', 'features.auto_save', auto_save_rect))
    
    # 4. Vitesse du croupier
    dealer_speed_rect = pygame.Rect(x_center, y_start + y_spacing * 3, control_width, control_height)
    dealer_speed = config.get('ui.dealer_speed', 1.0)
    dealer_speed_hover = dealer_speed_rect.collidepoint(mouse_pos)
    draw_slider(screen, dealer_speed_rect, dealer_speed, 0.5, 2.0, "Vitesse Croupier", False, dealer_speed_hover)
    controls.append(('slider', 'ui.dealer_speed', dealer_speed_rect, 0.5, 2.0))
    
    # 5. Afficher probabilités
    prob_rect = pygame.Rect(x_center, y_start + y_spacing * 4, control_width, control_height)
    prob_on = config.get('features.show_probabilities', False)
    prob_hover = prob_rect.collidepoint(mouse_pos)
    draw_toggle_button(screen, prob_rect, prob_on, "Probabilités", prob_hover)
    controls.append(('toggle', 'features.show_probabilities', prob_rect))
    
    # 6. Thème de la table
    theme_rect = pygame.Rect(x_center, y_start + y_spacing * 5, control_width, control_height)
    themes = ["Vert", "Bleu", "Rouge", "Noir"]
    current_theme = config.get('ui.table_theme', 'green')
    theme_map = {"green": 0, "blue": 1, "red": 2, "black": 3}
    theme_index = theme_map.get(current_theme, 0)
    theme_hover = theme_rect.collidepoint(mouse_pos)
    draw_cycle_button(screen, theme_rect, themes, theme_index, "Thème Table", theme_hover)
    controls.append(('cycle', 'ui.table_theme', theme_rect, themes))
    
    game.settings_controls = controls
    
    draw_shadow_text(screen, "ESC pour retour", get_font("sans", 18), COLOR_TEXT_GREY, WIDTH//2, 620, center=True)
'''
    
    # Remplacer
    pattern = r'def draw_settings_screen\(.*?\):\s*.*?(?=\ndef draw_stats_screen)'
    content = re.sub(pattern, new_draw_settings + '\n', content, flags=re.DOTALL)
    
    # 3. Ajouter la fonction pour appliquer le thème de couleur
    theme_function = '''
# Fonction pour obtenir les couleurs selon le thème
def get_table_colors():
    """Retourne les couleurs de la table selon le thème sélectionné"""
    config = get_config_manager()
    theme = config.get('ui.table_theme', 'green')
    
    themes = {
        'green': {
            'felt': (0, 100, 110),
            'felt_dark': (0, 70, 80),
            'felt_arc': (0, 120, 130)
        },
        'blue': {
            'felt': (30, 60, 140),
            'felt_dark': (20, 40, 100),
            'felt_arc': (50, 80, 160)
        },
        'red': {
            'felt': (120, 20, 20),
            'felt_dark': (80, 10, 10),
            'felt_arc': (140, 40, 40)
        },
        'black': {
            'felt': (40, 40, 40),
            'felt_dark': (20, 20, 20),
            'felt_arc': (60, 60, 60)
        }
    }
    
    return themes.get(theme, themes['green'])

'''
    
    # Insérer après les constantes de couleur
    insert_pos = content.find("# assets")
    if insert_pos != -1:
        content = content[:insert_pos] + theme_function + content[insert_pos:]
    
    # 4. Modifier render_table_bg pour utiliser les couleurs dynamiques
    old_render = '''def render_table_bg(screen: pygame.Surface):
    screen.fill(COLOR_ROOM_BG)
    # table ellipse large et aplatie
    table_rect = pygame.Rect(-200, HEIGHT // 2 - 120, WIDTH + 400, HEIGHT + 200)
    pygame.draw.ellipse(screen, COLOR_WOOD_RAIL, table_rect)
    felt_rect = table_rect.inflate(-60, -60)
    pygame.draw.ellipse(screen, COLOR_FELT, felt_rect)
    pygame.draw.arc(screen, (0, 120, 130), felt_rect.inflate(-100, -100), 0, 3.14, 2)'''
    
    new_render = '''def render_table_bg(screen: pygame.Surface):
    screen.fill(COLOR_ROOM_BG)
    colors = get_table_colors()
    # table ellipse large et aplatie
    table_rect = pygame.Rect(-200, HEIGHT // 2 - 120, WIDTH + 400, HEIGHT + 200)
    pygame.draw.ellipse(screen, COLOR_WOOD_RAIL, table_rect)
    felt_rect = table_rect.inflate(-60, -60)
    pygame.draw.ellipse(screen, colors['felt'], felt_rect)
    pygame.draw.arc(screen, colors['felt_arc'], felt_rect.inflate(-100, -100), 0, 3.14, 2)'''
    
    content = content.replace(old_render, new_render)
    
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ main.py mis à jour avec nouveaux paramètres et couleurs dynamiques")

if __name__ == "__main__":
    print("Mise à jour des paramètres...")
    update_settings()
    print("✅ Paramètres améliorés!")
    print("\nNouveaux paramètres:")
    print("- Sauvegarde automatique")
    print("- Vitesse du croupier")
    print("- Afficher les probabilités")
    print("- Thème de table (avec couleurs fonctionnelles)")
