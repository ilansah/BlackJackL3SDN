#!/usr/bin/env python3
"""
Script pour intégrer l'interface interactive des paramètres dans main.py
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def integrate_settings_ui():
    """Intègre les composants UI et la nouvelle fonction draw_settings_screen"""
    main_path = os.path.join(BASE_DIR, "src", "main.py")
    
    with open(main_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Ajouter les fonctions UI après draw_vip_button
    ui_functions = '''

# === Composants UI pour les paramètres ===

def draw_toggle_button(screen, rect, is_on, label, is_hover=False):
    """Dessine un bouton toggle ON/OFF"""
    bg_color = (50, 205, 50) if is_on else (220, 60, 60)
    if is_hover:
        bg_color = tuple(min(255, c + 30) for c in bg_color)
    
    pygame.draw.rect(screen, bg_color, rect, border_radius=8)
    pygame.draw.rect(screen, COLOR_GOLD, rect, 2, border_radius=8)
    
    status = "ON" if is_on else "OFF"
    font = get_font("sans", 16, bold=True)
    draw_shadow_text(screen, status, font, COLOR_TEXT_WHITE, rect.centerx, rect.centery, center=True)
    
    label_font = get_font("sans", 18)
    draw_shadow_text(screen, label, label_font, COLOR_TEXT_WHITE, rect.x - 200, rect.centery, center=True)
    
    return rect

def draw_slider(screen, rect, value, min_val, max_val, label, is_dragging=False, is_hover=False):
    """Dessine un slider pour les valeurs continues"""
    bar_rect = pygame.Rect(rect.x, rect.centery - 3, rect.width, 6)
    pygame.draw.rect(screen, (60, 60, 60), bar_rect, border_radius=3)
    
    progress_width = int((value - min_val) / (max_val - min_val) * rect.width)
    progress_rect = pygame.Rect(rect.x, rect.centery - 3, progress_width, 6)
    pygame.draw.rect(screen, COLOR_GOLD, progress_rect, border_radius=3)
    
    handle_x = rect.x + progress_width
    handle_radius = 12 if is_dragging or is_hover else 10
    handle_color = COLOR_GOLD_LIGHT if is_dragging or is_hover else COLOR_GOLD
    pygame.draw.circle(screen, handle_color, (handle_x, rect.centery), handle_radius)
    pygame.draw.circle(screen, COLOR_TEXT_WHITE, (handle_x, rect.centery), handle_radius, 2)
    
    label_font = get_font("sans", 18)
    draw_shadow_text(screen, label, label_font, COLOR_TEXT_WHITE, rect.x - 200, rect.centery, center=True)
    
    value_text = f"{int(value * 100)}%" if max_val == 1.0 else f"{value:.1f}x"
    value_font = get_font("sans", 16)
    draw_shadow_text(screen, value_text, value_font, COLOR_GOLD, rect.right + 40, rect.centery, center=True)
    
    return rect, handle_x

def draw_cycle_button(screen, rect, options, current_index, label, is_hover=False):
    """Dessine un bouton pour cycler entre des options"""
    bg_color = (40, 40, 45) if not is_hover else (60, 60, 65)
    pygame.draw.rect(screen, bg_color, rect, border_radius=8)
    pygame.draw.rect(screen, COLOR_GOLD if is_hover else (100, 100, 100), rect, 2, border_radius=8)
    
    arrow_font = get_font("sans", 18, bold=True)
    draw_shadow_text(screen, "◀", arrow_font, COLOR_TEXT_WHITE, rect.x + 15, rect.centery, center=True)
    draw_shadow_text(screen, "▶", arrow_font, COLOR_TEXT_WHITE, rect.right - 15, rect.centery, center=True)
    
    current_value = options[current_index]
    value_font = get_font("sans", 16, bold=True)
    draw_shadow_text(screen, current_value, value_font, COLOR_GOLD_LIGHT, rect.centerx, rect.centery, center=True)
    
    label_font = get_font("sans", 18)
    draw_shadow_text(screen, label, label_font, COLOR_TEXT_WHITE, rect.x - 200, rect.centery, center=True)
    
    return rect
'''
    
    # Insérer après draw_vip_button
    insert_pos = content.find("# loading assets")
    if insert_pos != -1:
        content = content[:insert_pos] + ui_functions + "\n" + content[insert_pos:]
    
    # 2. Remplacer draw_settings_screen
    new_settings_screen = '''def draw_settings_screen(screen: pygame.Surface, game: Game):
    screen.fill(COLOR_ROOM_BG)
    box = pygame.Rect(WIDTH//2 - 400, 80, 800, 560)
    pygame.draw.rect(screen, (30, 30, 35), box, border_radius=20)
    pygame.draw.rect(screen, COLOR_GOLD, box, 2, border_radius=20)
    
    draw_shadow_text(screen, "PARAMÈTRES", get_font("serif", 40, True), COLOR_GOLD, WIDTH//2, 120, center=True)
    
    config = get_config_manager()
    mouse_pos = pygame.mouse.get_pos()
    
    # Définir les rectangles pour chaque contrôle
    y_start = 200
    y_spacing = 60
    control_width = 200
    control_height = 40
    x_center = WIDTH//2 + 100
    
    # Liste des contrôles
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
    
    # 3. Animations ON/OFF
    anim_rect = pygame.Rect(x_center, y_start + y_spacing * 2, control_width, control_height)
    anim_on = config.get('features.animations_enabled', True)
    anim_hover = anim_rect.collidepoint(mouse_pos)
    draw_toggle_button(screen, anim_rect, anim_on, "Animations", anim_hover)
    controls.append(('toggle', 'features.animations_enabled', anim_rect))
    
    # 4. Vitesse des animations
    speed_rect = pygame.Rect(x_center, y_start + y_spacing * 3, control_width, control_height)
    speed = config.get('features.animation_speed', 1.0)
    speed_hover = speed_rect.collidepoint(mouse_pos)
    draw_slider(screen, speed_rect, speed, 0.5, 2.0, "Vitesse Anim.", False, speed_hover)
    controls.append(('slider', 'features.animation_speed', speed_rect, 0.5, 2.0))
    
    # 5. Afficher les indices
    hints_rect = pygame.Rect(x_center, y_start + y_spacing * 4, control_width, control_height)
    hints_on = config.get('features.show_hints', True)
    hints_hover = hints_rect.collidepoint(mouse_pos)
    draw_toggle_button(screen, hints_rect, hints_on, "Indices", hints_hover)
    controls.append(('toggle', 'features.show_hints', hints_rect))
    
    # 6. Thème de la table
    theme_rect = pygame.Rect(x_center, y_start + y_spacing * 5, control_width, control_height)
    themes = ["Vert", "Bleu", "Rouge", "Noir"]
    current_theme = config.get('ui.table_theme', 'green')
    theme_map = {"green": 0, "blue": 1, "red": 2, "black": 3}
    theme_index = theme_map.get(current_theme, 0)
    theme_hover = theme_rect.collidepoint(mouse_pos)
    draw_cycle_button(screen, theme_rect, themes, theme_index, "Thème Table", theme_hover)
    controls.append(('cycle', 'ui.table_theme', theme_rect, themes))
    
    # Stocker les contrôles dans game pour handle_input
    game.settings_controls = controls
    
    draw_shadow_text(screen, "ESC pour retour", get_font("sans", 18), COLOR_TEXT_GREY, WIDTH//2, 620, center=True)
'''
    
    # Trouver et remplacer l'ancienne fonction
    pattern = r'def draw_settings_screen\(.*?\):\s*.*?(?=\ndef draw_stats_screen)'
    content = re.sub(pattern, new_settings_screen + '\n', content, flags=re.DOTALL)
    
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ main.py mis à jour avec l'interface interactive")

if __name__ == "__main__":
    print("Intégration de l'interface interactive...")
    integrate_settings_ui()
    print("✅ Intégration terminée!")
