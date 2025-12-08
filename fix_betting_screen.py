#!/usr/bin/env python3
"""Script to fix betting screen for multi-seat"""

# Read the file
with open(r"c:\Users\user\OneDrive\Ilan.sahraoui\École (CATHO)\L3_SDN\S1\logicielle\BlackJackL3SDN\src\main.py", 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Update betting input to use seat_bets
old_betting = """            elif game.state == GameState.BETTING:
                for i, seat in enumerate(SEAT_POSITIONS):
                    if seat["rect"].collidepoint(pos):
                        game.seat_index = i
                
                if start_rect.collidepoint(pos) and game.player_bet > 0:
                    start_round = True
                
                for chip in chips:
                    if chip["rect"].collidepoint(pos):
                        if event.button == 1: game.player_bet += chip["value"]
                        elif event.button == 3: game.player_bet = max(0, game.player_bet - chip["value"])"""

new_betting = """            elif game.state == GameState.BETTING:
                # Sélection de siège pour placer les mises
                for i, seat in enumerate(SEAT_POSITIONS):
                    if seat["rect"].collidepoint(pos):
                        if event.button == 1:
                            # Clic gauche: sélectionner cette place pour miser
                            game.current_seat_for_betting = i
                        elif event.button == 3:
                            # Clic droit: retirer la mise de cette place
                            if i in game.seat_bets:
                                game.seat_bets[i] = 0
                
                # Calculer la mise totale
                total_bet = sum(game.seat_bets.values())
                
                if start_rect.collidepoint(pos) and total_bet > 0:
                    start_round = True
                
                for chip in chips:
                    if chip["rect"].collidepoint(pos):
                        # Ajouter/retirer des jetons à la place sélectionnée
                        if event.button == 1:
                            if game.current_seat_for_betting not in game.seat_bets:
                                game.seat_bets[game.current_seat_for_betting] = 0
                            game.seat_bets[game.current_seat_for_betting] += chip["value"]
                        elif event.button == 3:
                            if game.current_seat_for_betting in game.seat_bets:
                                game.seat_bets[game.current_seat_for_betting] = max(0, game.seat_bets[game.current_seat_for_betting] - chip["value"])"""

content = content.replace(old_betting, new_betting)

# Fix 2: Update draw_bet_screen to show seat_bets
old_bet_display = """    # mise un peu plus bas
    draw_shadow_text(screen, f"MISE: ${game.player_bet}", get_font("sans", 28, True), COLOR_TEXT_WHITE, WIDTH//2, HEIGHT - 180, center=True)
    
    # bouton distribuer
    is_valid = game.player_bet > 0
    draw_vip_button(screen, start_button_rect, "DISTRIBUER", start_button_rect.collidepoint(mouse_pos), is_active=is_valid)"""

new_bet_display = """    # mise totale
    total_bet = sum(game.seat_bets.values())
    active_seats = sum(1 for bet in game.seat_bets.values() if bet > 0)
    if total_bet > 0:
        bet_text = f"MISE TOTALE: ${total_bet} ({active_seats} place{'s' if active_seats > 1 else ''})"
    else:
        bet_text = "Sélectionnez une place et ajoutez des jetons"
    draw_shadow_text(screen, bet_text, get_font("sans", 24, True), COLOR_TEXT_WHITE, WIDTH//2, HEIGHT - 180, center=True)
    
    # bouton distribuer
    is_valid = total_bet > 0
    draw_vip_button(screen, start_button_rect, "DISTRIBUER", start_button_rect.collidepoint(mouse_pos), is_active=is_valid)"""

content = content.replace(old_bet_display, new_bet_display)

# Fix 3: Update seat display to show bets
old_seat_display = """    # Sieges 
    for i, seat in enumerate(SEAT_POSITIONS):
        cx, cy = seat["center"]
        rect = seat["rect"]
        
        is_sel = (i == game.seat_index)
        is_hov = rect.collidepoint(mouse_pos)
        
        rad = 38
        if is_sel:
            pygame.draw.circle(screen, COLOR_GOLD, (cx, cy), rad, 4)
            pygame.draw.circle(screen, (255, 215, 0, 50), (cx, cy), rad)
            col_txt = COLOR_GOLD
        elif is_hov:
            pygame.draw.circle(screen, COLOR_TEXT_WHITE, (cx, cy), rad, 2)
            col_txt = COLOR_TEXT_WHITE
        else:
            pygame.draw.circle(screen, (80, 80, 80), (cx, cy), rad, 2)
            col_txt = (100, 100, 100)
            
        draw_shadow_text(screen, f"P{i+1}", get_font("sans", 20, True), col_txt, cx, cy, center=True)"""

new_seat_display = """    # Sieges - afficher les mises sur chaque place
    for i, seat in enumerate(SEAT_POSITIONS):
        cx, cy = seat["center"]
        rect = seat["rect"]
        
        # Vérifier si cette place a une mise
        has_bet = i in game.seat_bets and game.seat_bets[i] > 0
        is_sel = (i == game.current_seat_for_betting)
        is_hov = rect.collidepoint(mouse_pos)
        
        rad = 38
        if has_bet:
            # Place avec mise - afficher en doré
            pygame.draw.circle(screen, COLOR_GOLD, (cx, cy), rad, 4)
            pygame.draw.circle(screen, (255, 215, 0, 50), (cx, cy), rad)
            col_txt = COLOR_GOLD
        elif is_sel:
            # Place sélectionnée pour miser
            pygame.draw.circle(screen, COLOR_GOLD_LIGHT, (cx, cy), rad, 3)
            col_txt = COLOR_GOLD_LIGHT
        elif is_hov:
            pygame.draw.circle(screen, COLOR_TEXT_WHITE, (cx, cy), rad, 2)
            col_txt = COLOR_TEXT_WHITE
        else:
            pygame.draw.circle(screen, (80, 80, 80), (cx, cy), rad, 2)
            col_txt = (100, 100, 100)
            
        draw_shadow_text(screen, f"P{i+1}", get_font("sans", 20, True), col_txt, cx, cy, center=True)
        
        # Afficher la mise sur cette place
        if has_bet:
            bet_y = cy + 50
            draw_shadow_text(screen, f"${game.seat_bets[i]}", get_font("sans", 16, True), COLOR_GOLD, cx, bet_y, center=True)"""

content = content.replace(old_seat_display, new_seat_display)

# Fix 4: Reset seat_bets on result screen
old_reset = """            if game.state == GameState.RESULT_SCREEN:
                if event.key == pygame.K_SPACE:
                    game.reset()
                    game.player_bet = 0
                    game.state = GameState.BETTING"""

new_reset = """            if game.state == GameState.RESULT_SCREEN:
                if event.key == pygame.K_SPACE:
                    game.reset()
                    game.seat_bets = {}
                    game.state = GameState.BETTING"""

content = content.replace(old_reset, new_reset)

# Write back
with open(r"c:\Users\user\OneDrive\Ilan.sahraoui\École (CATHO)\L3_SDN\S1\logicielle\BlackJackL3SDN\src\main.py", 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed betting screen for multi-seat!")
