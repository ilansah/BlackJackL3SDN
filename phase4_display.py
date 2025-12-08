#!/usr/bin/env python3
"""Script to update draw_game_screen for multi-seat display"""

# Read the file
with open(r"c:\Users\user\OneDrive\Ilan.sahraoui\École (CATHO)\L3_SDN\S1\logicielle\BlackJackL3SDN\src\main.py", 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the player display section
old_player = """    #  Joueur
    seat_coords = SEAT_POSITIONS[game.seat_index][\"center\"]
    seat_x, seat_y = seat_coords
    
    base_hand_y = seat_y - CARD_H // 2 - 20
    
    num_hands = len(game.hands)
    HAND_OFFSET = 120 
    
    # centrage du groupe de mains autour du siege
    total_group_width = (num_hands - 1) * HAND_OFFSET
    start_hx = seat_x - total_group_width // 2 - CARD_W // 2

    for i, hand in enumerate(game.hands):
        hand_x = start_hx + i * HAND_OFFSET
        card_spacing = 30
        
        # cadre actif
        is_active = (i == game.current_hand_index and game.state == GameState.PLAYER_TURN)
        if is_active:
            hand_w_px = len(hand.cards) * card_spacing + CARD_W
            glow_rect = pygame.Rect(hand_x - 10, base_hand_y - 10, hand_w_px + 20, CARD_H + 20)
            pygame.draw.rect(screen, (255, 215, 0, 60), glow_rect, border_radius=12)
            pygame.draw.rect(screen, COLOR_GOLD, glow_rect, 2, border_radius=12)

        # cartes
        for c_idx, card in enumerate(hand.cards):
            draw_card(screen, card, hand_x + c_idx * card_spacing, base_hand_y)
        
        # resultats
        val = hand.get_value()
        res_txt = f\"{val}\"
        color_res = COLOR_TEXT_WHITE
        
        res = game.hand_results[i]
        if res == GameResult.PLAYER_WIN: color_res = COLOR_WIN; res_txt = f\"GAGNÉ {val}\"
        elif res == GameResult.DEALER_WIN: color_res = COLOR_LOSE; res_txt = f\"PERDU {val}\"
        elif res == GameResult.PUSH: color_res = COLOR_PUSH; res_txt = f\"ÉGALITÉ\"
        elif hand.is_bust(): color_res = COLOR_LOSE; res_txt = f\"BUST {val}\"
        
        # etiquette sous la carte
        lbl_y = base_hand_y + CARD_H + 15
        bg_lbl = pygame.Rect(hand_x, lbl_y, 100, 28)
        pygame.draw.rect(screen, (0,0,0,180), bg_lbl, border_radius=10)
        draw_shadow_text(screen, res_txt, get_font(\"sans\", 16, True), color_res, bg_lbl.centerx, bg_lbl.centery, center=True)
        
        bet = game.hand_bets[i]
        draw_shadow_text(screen, f\"${bet}\", get_font(\"sans\", 14), COLOR_GOLD, bg_lbl.centerx, bg_lbl.bottom + 10, center=True)"""

new_player = """    #  Joueur - afficher toutes les places actives
    if game.active_seats:
        # Mode multi-places
        for seat_idx in game.active_seats:
            seat_coords = SEAT_POSITIONS[seat_idx][\"center\"]
            seat_x, seat_y = seat_coords
            base_hand_y = seat_y - CARD_H // 2 - 20
            
            hand = game.seat_hands[seat_idx]
            card_spacing = 30
            hand_x = seat_x - CARD_W // 2
            
            # Cadre actif si c'est la place en cours de jeu
            is_active = (game.active_seats.index(seat_idx) == game.current_seat_playing and game.state == GameState.PLAYER_TURN)
            if is_active:
                hand_w_px = len(hand.cards) * card_spacing + CARD_W
                glow_rect = pygame.Rect(hand_x - 10, base_hand_y - 10, hand_w_px + 20, CARD_H + 20)
                pygame.draw.rect(screen, (255, 215, 0, 60), glow_rect, border_radius=12)
                pygame.draw.rect(screen, COLOR_GOLD, glow_rect, 2, border_radius=12)
            
            # Cartes
            for c_idx, card in enumerate(hand.cards):
                draw_card(screen, card, hand_x + c_idx * card_spacing, base_hand_y)
            
            # Résultats
            val = hand.get_value()
            res_txt = f\"{val}\"
            color_res = COLOR_TEXT_WHITE
            
            res = game.seat_results.get(seat_idx)
            if res == GameResult.PLAYER_WIN: color_res = COLOR_WIN; res_txt = f\"GAGNÉ {val}\"
            elif res == GameResult.DEALER_WIN: color_res = COLOR_LOSE; res_txt = f\"PERDU {val}\"
            elif res == GameResult.PUSH: color_res = COLOR_PUSH; res_txt = f\"ÉGALITÉ\"
            elif hand.is_bust(): color_res = COLOR_LOSE; res_txt = f\"BUST {val}\"
            
            # Étiquette sous la carte
            lbl_y = base_hand_y + CARD_H + 15
            bg_lbl = pygame.Rect(hand_x, lbl_y, 100, 28)
            pygame.draw.rect(screen, (0,0,0,180), bg_lbl, border_radius=10)
            draw_shadow_text(screen, res_txt, get_font(\"sans\", 16, True), color_res, bg_lbl.centerx, bg_lbl.centery, center=True)
            
            bet = game.seat_bets[seat_idx]
            draw_shadow_text(screen, f\"${bet}\", get_font(\"sans\", 14), COLOR_GOLD, bg_lbl.centerx, bg_lbl.bottom + 10, center=True)
    else:
        # Fallback mode single-place
        seat_coords = SEAT_POSITIONS[game.seat_index][\"center\"]
        seat_x, seat_y = seat_coords
        base_hand_y = seat_y - CARD_H // 2 - 20
        num_hands = len(game.hands)
        HAND_OFFSET = 120
        total_group_width = (num_hands - 1) * HAND_OFFSET
        start_hx = seat_x - total_group_width // 2 - CARD_W // 2

        for i, hand in enumerate(game.hands):
            hand_x = start_hx + i * HAND_OFFSET
            card_spacing = 30
            is_active = (i == game.current_hand_index and game.state == GameState.PLAYER_TURN)
            if is_active:
                hand_w_px = len(hand.cards) * card_spacing + CARD_W
                glow_rect = pygame.Rect(hand_x - 10, base_hand_y - 10, hand_w_px + 20, CARD_H + 20)
                pygame.draw.rect(screen, (255, 215, 0, 60), glow_rect, border_radius=12)
                pygame.draw.rect(screen, COLOR_GOLD, glow_rect, 2, border_radius=12)
            for c_idx, card in enumerate(hand.cards):
                draw_card(screen, card, hand_x + c_idx * card_spacing, base_hand_y)
            val = hand.get_value()
            res_txt = f\"{val}\"
            color_res = COLOR_TEXT_WHITE
            res = game.hand_results[i]
            if res == GameResult.PLAYER_WIN: color_res = COLOR_WIN; res_txt = f\"GAGNÉ {val}\"
            elif res == GameResult.DEALER_WIN: color_res = COLOR_LOSE; res_txt = f\"PERDU {val}\"
            elif res == GameResult.PUSH: color_res = COLOR_PUSH; res_txt = f\"ÉGALITÉ\"
            elif hand.is_bust(): color_res = COLOR_LOSE; res_txt = f\"BUST {val}\"
            lbl_y = base_hand_y + CARD_H + 15
            bg_lbl = pygame.Rect(hand_x, lbl_y, 100, 28)
            pygame.draw.rect(screen, (0,0,0,180), bg_lbl, border_radius=10)
            draw_shadow_text(screen, res_txt, get_font(\"sans\", 16, True), color_res, bg_lbl.centerx, bg_lbl.centery, center=True)
            bet = game.hand_bets[i]
            draw_shadow_text(screen, f\"${bet}\", get_font(\"sans\", 14), COLOR_GOLD, bg_lbl.centerx, bg_lbl.bottom + 10, center=True)"""

content = content.replace(old_player, new_player)

# Write back
with open(r"c:\Users\user\OneDrive\Ilan.sahraoui\École (CATHO)\L3_SDN\S1\logicielle\BlackJackL3SDN\src\main.py", 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated display for multi-seat!")
