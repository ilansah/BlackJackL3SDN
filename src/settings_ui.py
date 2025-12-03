
# Fonctions pour l'interface interactive des paramètres

def draw_toggle_button(screen, rect, is_on, label, is_hover=False):
    """Dessine un bouton toggle ON/OFF"""
    # Couleurs
    bg_color = (50, 205, 50) if is_on else (220, 60, 60)  # Vert si ON, Rouge si OFF
    if is_hover:
        bg_color = tuple(min(255, c + 30) for c in bg_color)
    
    # Fond du bouton
    pygame.draw.rect(screen, bg_color, rect, border_radius=8)
    pygame.draw.rect(screen, COLOR_GOLD, rect, 2, border_radius=8)
    
    # Texte
    status = "ON" if is_on else "OFF"
    font = get_font("sans", 18, bold=True)
    draw_shadow_text(screen, status, font, COLOR_TEXT_WHITE, rect.centerx, rect.centery, center=True)
    
    # Label à gauche
    label_font = get_font("sans", 20)
    draw_shadow_text(screen, label, label_font, COLOR_TEXT_WHITE, rect.x - 10, rect.centery, topleft=False)
    
    return rect

def draw_slider(screen, rect, value, min_val, max_val, label, is_dragging=False, is_hover=False):
    """Dessine un slider pour les valeurs continues (0-1)"""
    # Barre de fond
    bar_rect = pygame.Rect(rect.x, rect.centery - 3, rect.width, 6)
    pygame.draw.rect(screen, (60, 60, 60), bar_rect, border_radius=3)
    
    # Barre de progression
    progress_width = int((value - min_val) / (max_val - min_val) * rect.width)
    progress_rect = pygame.Rect(rect.x, rect.centery - 3, progress_width, 6)
    pygame.draw.rect(screen, COLOR_GOLD, progress_rect, border_radius=3)
    
    # Handle (poignée)
    handle_x = rect.x + progress_width
    handle_radius = 12 if is_dragging or is_hover else 10
    handle_color = COLOR_GOLD_LIGHT if is_dragging or is_hover else COLOR_GOLD
    pygame.draw.circle(screen, handle_color, (handle_x, rect.centery), handle_radius)
    pygame.draw.circle(screen, COLOR_TEXT_WHITE, (handle_x, rect.centery), handle_radius, 2)
    
    # Label
    label_font = get_font("sans", 20)
    draw_shadow_text(screen, label, label_font, COLOR_TEXT_WHITE, rect.x - 10, rect.y - 5, topleft=False)
    
    # Valeur actuelle
    value_text = f"{int(value * 100)}%" if max_val == 1.0 else f"{value:.1f}x"
    value_font = get_font("sans", 16)
    draw_shadow_text(screen, value_text, value_font, COLOR_GOLD, rect.right + 10, rect.centery, topleft=False)
    
    return rect, handle_x

def draw_cycle_button(screen, rect, options, current_index, label, is_hover=False):
    """Dessine un bouton pour cycler entre des options"""
    # Fond
    bg_color = (40, 40, 45) if not is_hover else (60, 60, 65)
    pygame.draw.rect(screen, bg_color, rect, border_radius=8)
    pygame.draw.rect(screen, COLOR_GOLD if is_hover else (100, 100, 100), rect, 2, border_radius=8)
    
    # Flèches
    arrow_font = get_font("sans", 20, bold=True)
    draw_shadow_text(screen, "◀", arrow_font, COLOR_TEXT_WHITE, rect.x + 15, rect.centery, center=True)
    draw_shadow_text(screen, "▶", arrow_font, COLOR_TEXT_WHITE, rect.right - 15, rect.centery, center=True)
    
    # Valeur actuelle
    current_value = options[current_index]
    value_font = get_font("sans", 18, bold=True)
    draw_shadow_text(screen, current_value, value_font, COLOR_GOLD_LIGHT, rect.centerx, rect.centery, center=True)
    
    # Label
    label_font = get_font("sans", 20)
    draw_shadow_text(screen, label, label_font, COLOR_TEXT_WHITE, rect.x - 10, rect.centery, topleft=False)
    
    return rect
