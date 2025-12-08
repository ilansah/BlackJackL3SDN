import sys
import os

# Lire le fichier main.py
main_path = r"c:\Users\user\OneDrive\Ilan.sahraoui\École (CATHO)\L3_SDN\S1\logicielle\BlackJackL3SDN\src\main.py"

with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Trouver la fonction draw_game_screen
start_marker = "def draw_game_screen(screen: pygame.Surface, game: Game, player: Player, dealer_revealed: bool, chips, seats):"
end_marker = "\n\ndef draw_bet_screen"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker, start_idx)

if start_idx == -1 or end_idx == -1:
    print("Erreur: impossible de trouver la fonction draw_game_screen")
    sys.exit(1)

# Nouvelle version de la fonction
new_function = '''def draw_game_screen(screen: pygame.Surface, game: Game, player: Player, dealer_revealed: bool, chips, seats):
    render_table_bg(screen)
    
    #  Croupier
    DEALER_Y = 60
    spacing = 40
    dealer_hand = game.dealer_hand
    total_w_dealer = len(dealer_hand.cards) * CARD_W - (len(dealer_hand.cards)-1) * (CARD_W - spacing)
    start_dx = WIDTH // 2 - total_w_dealer // 2 + 30 
    
    # Texte Croupier
    d_val = dealer_hand.get_value()
    d_txt = f"CROUPIER : {d_val}"
    if not dealer_revealed and game.state in [GameState.INITIAL_DEAL, GameState.PLAYER_TURN]: d_txt = "CROUPIER"
    elif dealer_hand.is_bust(): d_txt += " (BUST)"
    
    draw_shadow_text(screen, d_txt, get_font("serif", 22), COLOR_TEXT_WHITE, WIDTH//2, DEALER_Y - 30, center=True)

    # Cartes Croupier
    current_dx = start_dx
    for i, card in enumerate(dealer_hand.cards):
        if i == 1 and not dealer_revealed and game.state in [GameState.INITIAL_DEAL, GameState.PLAYER_TURN]:
            draw_back(screen, current_dx, DEALER_Y)
        else:
            draw_card(screen, card, current_dx, DEALER_Y)
        current_dx += spacing

    # Mode multi-places
    if game.active_seats:
        for seat_idx in game.active_seats:
            seat_coords = SEAT_POSITIONS[seat_idx]["center"]
            seat_x, seat_y = seat_coords
            
            hand = game.seat_hands[seat_idx]
            base_hand_y = seat_y - CARD_H // 2 - 20
            
            # Position de départ pour les cartes
            card_spacing = 30
            num_cards = len(hand.cards)
            total_cards_width = num_cards * card_spacing + CARD_W - card_spacing
            hand_x = seat_x - total_cards_width // 2
            
            # Cadre actif pour la place en cours de jeu
            is_active = (game.current_seat_playing < len(game.active_seats) and 
                        game.active_seats[game.current_seat_playing] == seat_idx and 
                        game.state == GameState.PLAYER_TURN)
            if is_active:
                hand_w_px = total_cards_width + 20
                glow_rect = pygame.Rect(hand_x - 10, base_hand_y - 10, hand_w_px, CARD_H + 20)
                pygame.draw.rect(screen, (255, 215, 0, 60), glow_rect, border_radius=12)
                pygame.draw.rect(screen, COLOR_GOLD, glow_rect, 2, border_radius=12)
            
            # Dessiner les cartes
            for c_idx, card in enumerate(hand.cards):
                draw_card(screen, card, hand_x + c_idx * card_spacing, base_hand_y)
            
            # Résultats
            val = hand.get_value()
            res_txt = f"{val}"
            color_res = COLOR_TEXT_WHITE
            
            res = game.seat_results.get(seat_idx)
            if res == GameResult.PLAYER_WIN: color_res = COLOR_WIN; res_txt = f"GAGNÉ {val}"
            elif res == GameResult.DEALER_WIN: color_res = COLOR_LOSE; res_txt = f"PERDU {val}"
            elif res == GameResult.PUSH: color_res = COLOR_PUSH; res_txt = f"ÉGALITÉ"
            elif hand.is_bust(): color_res = COLOR_LOSE; res_txt = f"BUST {val}"
            
            # Étiquette sous la carte
            lbl_y = base_hand_y + CARD_H + 15
            bg_lbl = pygame.Rect(hand_x, lbl_y, 100, 28)
            pygame.draw.rect(screen, (0,0,0,180), bg_lbl, border_radius=10)
            draw_shadow_text(screen, res_txt, get_font("sans", 16, True), color_res, bg_lbl.centerx, bg_lbl.centery, center=True)
            
            bet = game.seat_bets[seat_idx]
            draw_shadow_text(screen, f"${bet}", get_font("sans", 14), COLOR_GOLD, bg_lbl.centerx, bg_lbl.bottom + 10, center=True)
    
    # Mode single-seat (fallback)
    else:
        seat_coords = SEAT_POSITIONS[game.seat_index]["center"]
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
            res_txt = f"{val}"
            color_res = COLOR_TEXT_WHITE
            
            res = game.hand_results[i]
            if res == GameResult.PLAYER_WIN: color_res = COLOR_WIN; res_txt = f"GAGNÉ {val}"
            elif res == GameResult.DEALER_WIN: color_res = COLOR_LOSE; res_txt = f"PERDU {val}"
            elif res == GameResult.PUSH: color_res = COLOR_PUSH; res_txt = f"ÉGALITÉ"
            elif hand.is_bust(): color_res = COLOR_LOSE; res_txt = f"BUST {val}"
            
            # etiquette sous la carte
            lbl_y = base_hand_y + CARD_H + 15
            bg_lbl = pygame.Rect(hand_x, lbl_y, 100, 28)
            pygame.draw.rect(screen, (0,0,0,180), bg_lbl, border_radius=10)
            draw_shadow_text(screen, res_txt, get_font("sans", 16, True), color_res, bg_lbl.centerx, bg_lbl.centery, center=True)
            
            bet = game.hand_bets[i]
            draw_shadow_text(screen, f"${bet}", get_font("sans", 14), COLOR_GOLD, bg_lbl.centerx, bg_lbl.bottom + 10, center=True)


    #  Message Central
    if game.state == GameState.RESULT_SCREEN:
        msg = game.get_status_message()
        font_big = get_font("serif", 48, bold=True)
        s = font_big.render(msg, True, COLOR_GOLD)
        r = s.get_rect(center=(WIDTH//2, HEIGHT//2))
        bg = r.inflate(40, 20)
        pygame.draw.rect(screen, (0,0,0, 220), bg, border_radius=20)
        pygame.draw.rect(screen, COLOR_GOLD, bg, 2, border_radius=20)
        screen.blit(s, r)
        draw_shadow_text(screen, "ESPACE POUR REJOUER", get_font("sans", 20, True), COLOR_GOLD_LIGHT, WIDTH//2, r.bottom + 30, center=True)

    # Barre d'actions 
    if game.state == GameState.PLAYER_TURN:
        panel_rect = pygame.Rect(20, 20, 180, 160)
        pygame.draw.rect(screen, (0, 0, 0, 180), panel_rect, border_radius=10)
        pygame.draw.rect(screen, COLOR_WOOD_RAIL, panel_rect, 2, border_radius=10)
        
        draw_shadow_text(screen, "ACTIONS", get_font("sans", 16, True), COLOR_GOLD, panel_rect.centerx, panel_rect.y + 15, center=True)
        
        # liste des actions dispos
        opts = []
        if game.can_hit(): opts.append("[H] TIRER")
        if game.can_stand(): opts.append("[S] RESTER")
        if game.can_double(): opts.append("[D] DOUBLER")
        if game.can_split(): opts.append("[P] SPLIT")
        if game.can_surrender(): opts.append("[R] ABANDON")
        
        start_y = panel_rect.y + 40
        for opt in opts:
            draw_shadow_text(screen, opt, get_font("sans", 14, True), COLOR_TEXT_WHITE, 35, start_y, topleft=True)
            start_y += 22

    #  Solde 
    panel = pygame.Rect(20, HEIGHT - 50, 200, 40)
    pygame.draw.rect(screen, (20, 25, 30), panel, border_radius=10)
    pygame.draw.rect(screen, COLOR_WOOD_RAIL, panel, 2, border_radius=10)
    draw_shadow_text(screen, f"SOLDE: ${player.balance}", get_font("sans", 18, True), COLOR_GOLD, panel.centerx, panel.centery, center=True)

'''

# Remplacer la fonction
new_content = content[:start_idx] + new_function + content[end_idx:]

# Écrire le fichier
with open(main_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✓ Fonction draw_game_screen mise à jour avec succès!")
print("  - Support du mode multi-places ajouté")
print("  - Compatibilité avec le mode single-seat conservée")
