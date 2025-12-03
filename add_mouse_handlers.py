#!/usr/bin/env python3
"""
Script pour ajouter la gestion des interactions souris dans handle_input
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def add_mouse_handlers():
    """Ajoute la gestion des clics souris pour les paramètres"""
    main_path = os.path.join(BASE_DIR, "src", "main.py")
    
    with open(main_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Trouver la section MOUSEBUTTONDOWN dans handle_input
    # Ajouter la gestion des clics dans les paramètres
    
    settings_mouse_code = '''
            # Gestion des clics dans les paramètres
            elif game.state == GameState.SETTINGS:
                if hasattr(game, 'settings_controls'):
                    config = get_config_manager()
                    for control in game.settings_controls:
                        control_type = control[0]
                        config_key = control[1]
                        rect = control[2]
                        
                        if rect.collidepoint(pos):
                            if control_type == 'toggle':
                                # Toggle ON/OFF
                                current = config.get(config_key, False)
                                config.set(config_key, not current)
                                
                                # Si c'est la musique, démarrer/arrêter
                                if config_key == 'features.music_enabled':
                                    if not current:  # On vient de l'activer
                                        if os.path.exists(MUSIC_FILE):
                                            try:
                                                pygame.mixer.music.load(MUSIC_FILE)
                                                pygame.mixer.music.set_volume(config.get('features.music_volume', 0.5))
                                                pygame.mixer.music.play(-1)
                                            except: pass
                                    else:  # On vient de la désactiver
                                        pygame.mixer.music.stop()
                            
                            elif control_type == 'cycle':
                                # Cycler entre les options
                                options = control[3]
                                theme_map = {"green": 0, "blue": 1, "red": 2, "black": 3}
                                reverse_map = {0: "green", 1: "blue", 2: "red", 3: "black"}
                                current_theme = config.get(config_key, 'green')
                                current_index = theme_map.get(current_theme, 0)
                                
                                # Déterminer si on a cliqué sur la flèche gauche ou droite
                                if pos[0] < rect.centerx:
                                    # Flèche gauche
                                    new_index = (current_index - 1) % len(options)
                                else:
                                    # Flèche droite
                                    new_index = (current_index + 1) % len(options)
                                
                                new_theme = reverse_map[new_index]
                                config.set(config_key, new_theme)
'''
    
    # Trouver la section MOUSEBUTTONDOWN et ajouter après la gestion du BETTING
    pattern = r'(elif game\.state == GameState\.BETTING:.*?elif event\.button == 3:.*?\n)'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        insert_pos = match.end()
        content = content[:insert_pos] + settings_mouse_code + content[insert_pos:]
    
    # Ajouter la gestion du drag pour les sliders
    # Chercher la section MOUSEMOTION
    if 'pygame.MOUSEMOTION' not in content:
        # Ajouter après MOUSEBUTTONDOWN
        motion_code = '''
        if event.type == pygame.MOUSEMOTION:
            # Gestion du drag pour les sliders
            if game.state == GameState.SETTINGS and hasattr(game, 'settings_controls'):
                if hasattr(game, 'dragging_slider') and game.dragging_slider:
                    config = get_config_manager()
                    control = game.dragging_slider
                    rect = control[2]
                    min_val = control[3]
                    max_val = control[4]
                    config_key = control[1]
                    
                    # Calculer la nouvelle valeur
                    mouse_x = event.pos[0]
                    relative_x = max(0, min(rect.width, mouse_x - rect.x))
                    new_value = min_val + (relative_x / rect.width) * (max_val - min_val)
                    new_value = round(new_value, 2)
                    
                    config.set(config_key, new_value)
                    
                    # Si c'est le volume, l'appliquer immédiatement
                    if config_key == 'features.music_volume':
                        pygame.mixer.music.set_volume(new_value)
'''
        
        # Trouver la fin de la boucle for event
        pattern = r'(if event\.type == pygame\.KEYDOWN:)'
        content = re.sub(pattern, motion_code + r'\n        \1', content)
    
    # Ajouter la gestion du MOUSEBUTTONDOWN pour les sliders
    slider_down_code = '''
                            elif control_type == 'slider':
                                # Commencer le drag
                                game.dragging_slider = control
'''
    
    # Ajouter après la gestion du cycle
    content = content.replace(
        "                                config.set(config_key, new_theme)",
        "                                config.set(config_key, new_theme)" + slider_down_code
    )
    
    # Ajouter la gestion du MOUSEBUTTONUP pour arrêter le drag
    up_code = '''
        if event.type == pygame.MOUSEBUTTONUP:
            if hasattr(game, 'dragging_slider'):
                game.dragging_slider = None
'''
    
    # Ajouter après MOUSEMOTION
    pattern = r'(if event\.type == pygame\.KEYDOWN:)'
    content = re.sub(pattern, up_code + r'\n        \1', content)
    
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ Gestion des interactions souris ajoutée")

if __name__ == "__main__":
    print("Ajout des gestionnaires d'événements souris...")
    add_mouse_handlers()
    print("✅ Gestionnaires ajoutés!")
