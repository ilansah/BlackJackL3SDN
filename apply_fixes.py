#!/usr/bin/env python3
"""Script to apply fixes to the Blackjack game"""

import re

# Read the file
with open(r"c:\Users\user\OneDrive\Ilan.sahraoui\École (CATHO)\L3_SDN\S1\logicielle\BlackJackL3SDN\src\main.py", 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Hide dealer card value when second card is face down
old_dealer_text = """    # Texte Croupier
    d_val = dealer_hand.get_value()
    d_txt = f"CROUPIER : {d_val}"
    if not dealer_revealed and game.state in [GameState.INITIAL_DEAL, GameState.PLAYER_TURN]: d_txt = "CROUPIER"
    elif dealer_hand.is_bust(): d_txt += " (BUST)"
    """

new_dealer_text = """    # Texte Croupier
    # Ne pas afficher la valeur quand la deuxième carte est cachée
    if not dealer_revealed and game.state in [GameState.INITIAL_DEAL, GameState.PLAYER_TURN]:
        d_txt = "CROUPIER"
    else:
        d_val = dealer_hand.get_value()
        d_txt = f"CROUPIER : {d_val}"
        if dealer_hand.is_bust(): d_txt += " (BUST)"
    """

content = content.replace(old_dealer_text, new_dealer_text)

# Fix 2: Disable seat selection
old_seat_code = """    # Sieges 
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

new_seat_code = """    # Sieges - désactivé pour empêcher l'utilisation de plusieurs places
    # Toujours utiliser le siège central (index 2)
    game.seat_index = 2
    for i, seat in enumerate(SEAT_POSITIONS):
        cx, cy = seat["center"]
        rect = seat["rect"]
        
        is_sel = (i == game.seat_index)
        
        rad = 38
        if is_sel:
            pygame.draw.circle(screen, COLOR_GOLD, (cx, cy), rad, 4)
            pygame.draw.circle(screen, (255, 215, 0, 50), (cx, cy), rad)
            col_txt = COLOR_GOLD
        else:
            # Sièges non sélectionnés - grisés et non interactifs
            pygame.draw.circle(screen, (60, 60, 60), (cx, cy), rad, 2)
            col_txt = (80, 80, 80)
            
        draw_shadow_text(screen, f"P{i+1}", get_font("sans", 20, True), col_txt, cx, cy, center=True)"""

content = content.replace(old_seat_code, new_seat_code)

# Fix 3: Validate bet button with balance check
old_bet_button = """    # bouton distribuer
    is_valid = game.player_bet > 0
    draw_vip_button(screen, start_button_rect, "DISTRIBUER", start_button_rect.collidepoint(mouse_pos), is_active=is_valid)"""

new_bet_button = """    # bouton distribuer - vérifier aussi que le joueur a assez d'argent
    is_valid = game.player_bet > 0 and player.balance >= game.player_bet
    draw_vip_button(screen, start_button_rect, "DISTRIBUER", start_button_rect.collidepoint(mouse_pos), is_active=is_valid)"""

content = content.replace(old_bet_button, new_bet_button)

# Fix 4: Prevent betting with negative balance and disable seat selection in handle_input
old_betting_input = """            elif game.state == GameState.BETTING:
                for i, seat in enumerate(SEAT_POSITIONS):
                    if seat["rect"].collidepoint(pos):
                        game.seat_index = i
                
                if start_rect.collidepoint(pos) and game.player_bet > 0:
                    start_round = True
                
                for chip in chips:
                    if chip["rect"].collidepoint(pos):
                        if event.button == 1: game.player_bet += chip["value"]
                        elif event.button == 3: game.player_bet = max(0, game.player_bet - chip["value"])"""

new_betting_input = """            elif game.state == GameState.BETTING:
                # Sélection de siège désactivée - toujours utiliser le siège central
                # for i, seat in enumerate(SEAT_POSITIONS):
                #     if seat["rect"].collidepoint(pos):
                #         game.seat_index = i
                
                if start_rect.collidepoint(pos) and game.player_bet > 0 and player.balance >= game.player_bet:
                    start_round = True
                
                for chip in chips:
                    if chip["rect"].collidepoint(pos):
                        # Empêcher les mises si le solde est négatif ou insuffisant
                        if event.button == 1:
                            if player.balance > 0:
                                game.player_bet += chip["value"]
                        elif event.button == 3:
                            game.player_bet = max(0, game.player_bet - chip["value"])"""

content = content.replace(old_betting_input, new_betting_input)

# Write the modified content back
with open(r"c:\Users\user\OneDrive\Ilan.sahraoui\École (CATHO)\L3_SDN\S1\logicielle\BlackJackL3SDN\src\main.py", 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixes applied successfully!")
