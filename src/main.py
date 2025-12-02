import sys
import os
import pygame
import json
import math

from core.deck import Deck
from core.card import Card
from core.game import Game, GameState, GameResult
from core.player import Player

#  config graphique 
WIDTH, HEIGHT = 1280, 720
FPS = 60
CARD_W, CARD_H = 100, 145

#  palette de couleurs vip 
COLOR_ROOM_BG = (20, 20, 25)
COLOR_FELT = (0, 100, 110)
COLOR_FELT_DARK = (0, 70, 80)
COLOR_WOOD_RAIL = (60, 30, 10)
COLOR_GOLD = (212, 175, 55)
COLOR_GOLD_LIGHT = (255, 223, 100)
COLOR_TEXT_WHITE = (240, 240, 240)
COLOR_TEXT_GREY = (150, 150, 160)
COLOR_WIN = (50, 205, 50)
COLOR_LOSE = (220, 60, 60)
COLOR_PUSH = (255, 165, 0)

# assets 
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "cards")
CHIPS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "chips")

CHIP_FILES = [
    (5, "chip_5_w85h85.png"),
    (10, "chip_10_w85h85.png"),
    (50, "chip_50_w85h85.png"),
    (100, "chip_100_w85h85.png"),
]

_image_cache: dict[str, pygame.Surface] = {}

# positions des sieges 
SEAT_POSITIONS = []
center_x = WIDTH // 2
center_y = HEIGHT // 2 - 60 
radius = 500 
angles = [160, 130, 90, 50, 20] 

for angle in angles:
    rad = math.radians(angle)
    sx = center_x + radius * math.cos(rad)
    sy = center_y + radius * math.sin(rad) * 0.3 + 50
    
    rect = pygame.Rect(0, 0, 70, 70)
    rect.center = (int(sx), int(sy))
    SEAT_POSITIONS.append({"center": (int(sx), int(sy)), "rect": rect})


# fonctions utilitaires

def init_pygame():
    pygame.init()
    pygame.display.set_caption("Blackjack VIP Lounge")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    return screen, clock

def get_font(name="sans", size=20, bold=False):
    font_name = "arial"
    if name == "serif": font_name = "georgia"
    elif name == "sans": font_name = "verdana"
    elif name == "title": font_name = "impact"
    try: return pygame.font.SysFont(font_name, size, bold=bold)
    except: return pygame.font.SysFont("arial", size, bold=bold)

def draw_shadow_text(screen, text, font, color, x, y, center=False, topleft=False):
    shadow = font.render(text, True, (0, 0, 0))
    surf = font.render(text, True, color)
    pos_x, pos_y = x, y
    if center:
        pos_x = x - surf.get_width() // 2
        pos_y = y - surf.get_height() // 2
    elif topleft:
        pass
        
    screen.blit(shadow, (pos_x + 2, pos_y + 2))
    screen.blit(surf, (pos_x, pos_y))
    return surf.get_rect(topleft=(pos_x, pos_y))

def draw_vip_button(screen, rect, text, is_hover=False, is_active=True):
    color_bg = (30, 30, 30) if is_active else (15, 15, 15)
    color_border = COLOR_GOLD_LIGHT if (is_hover and is_active) else (COLOR_GOLD if is_active else (60, 60, 60))
    text_color = (COLOR_GOLD_LIGHT if is_hover else COLOR_TEXT_WHITE) if is_active else (80, 80, 80)
    
    shadow_rect = rect.copy()
    shadow_rect.y += 4
    pygame.draw.rect(screen, (5, 5, 5), shadow_rect, border_radius=15)
    pygame.draw.rect(screen, color_bg, rect, border_radius=15)
    pygame.draw.rect(screen, color_border, rect, 2, border_radius=15)
    
    font = get_font("sans", 22, bold=True)
    draw_shadow_text(screen, text, font, text_color, rect.centerx, rect.centery, center=True)

# loading assets

def suit_to_word(suit: str) -> str:
    return {"♠": "spades", "♥": "hearts", "♦": "diamonds", "♣": "clubs"}[suit]

def rank_to_word(rank: str) -> str:
    table = {"A": "ace", "J": "jack", "Q": "queen", "K": "king"}
    return table.get(rank, rank)

def card_filename(card: Card) -> str:
    base = f"{rank_to_word(card.rank)}_of_{suit_to_word(card.suit)}"
    return f"{base}.png"

def load_card_image(filename: str) -> pygame.Surface:
    global _image_cache
    key = filename.lower()
    if key in _image_cache: return _image_cache[key]

    candidates = [filename, filename.lower(), filename.replace(".png", ".jpg")]
    img = None
    for name in candidates:
        path = os.path.join(ASSETS_DIR, name)
        if os.path.exists(path):
            try: img = pygame.image.load(path).convert_alpha(); break
            except: pass

    if img is None:
        surf = pygame.Surface((CARD_W, CARD_H), pygame.SRCALPHA)
        surf.fill((230, 230, 230))
        pygame.draw.rect(surf, (50, 50, 50), surf.get_rect(), 2)
        _image_cache[key] = surf
        return surf

    img = pygame.transform.smoothscale(img, (CARD_W, CARD_H))
    _image_cache[key] = img
    return img

def load_chip_image(filename: str) -> pygame.Surface:
    global _image_cache
    key = f"chip_{filename.lower()}"
    if key in _image_cache: return _image_cache[key]
    path = os.path.join(CHIPS_DIR, filename)
    if not os.path.exists(path):
        surf = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.circle(surf, COLOR_GOLD, (40, 40), 38)
        _image_cache[key] = surf
        return surf
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.smoothscale(img, (85, 85))
    _image_cache[key] = img
    return img

def draw_card(screen: pygame.Surface, card: Card, x: int, y: int):
    img = load_card_image(card_filename(card))
    shadow = pygame.Surface((CARD_W, CARD_H), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (0, 0, 0, 80), shadow.get_rect(), border_radius=5)
    screen.blit(shadow, (x + 4, y + 4))
    screen.blit(img, (x, y))

def draw_back(screen: pygame.Surface, x: int, y: int):
    for name in ["back-side.png", "back.png", "BACK.png"]:
        img = load_card_image(name)
        if img is not None:
            screen.blit(img, (x, y))
            return

# rendu decor

def render_table_bg(screen: pygame.Surface):
    screen.fill(COLOR_ROOM_BG)
    # table ellipse large et aplatie
    table_rect = pygame.Rect(-200, HEIGHT // 2 - 120, WIDTH + 400, HEIGHT + 200)
    pygame.draw.ellipse(screen, COLOR_WOOD_RAIL, table_rect)
    felt_rect = table_rect.inflate(-60, -60)
    pygame.draw.ellipse(screen, COLOR_FELT, felt_rect)
    pygame.draw.arc(screen, (0, 120, 130), felt_rect.inflate(-100, -100), 0, 3.14, 2)
    
    font_logo = get_font("serif", 40, bold=True)
    logo_rect = draw_shadow_text(screen, "PRIVÉ LOUNGE", font_logo, (0, 90, 100), WIDTH//2, HEIGHT//2 - 40, center=True)
    font_sub = get_font("sans", 16, bold=True)
    draw_shadow_text(screen, "BLACKJACK PAYS 3 TO 2", font_sub, (0, 140, 150), WIDTH//2, logo_rect.bottom + 5, center=True)

#  ecrans

def draw_main_menu(screen: pygame.Surface, player: Player, play_rect, settings_rect, stats_rect):
    screen.fill(COLOR_ROOM_BG)
    glow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.circle(glow, (30, 30, 60), (WIDTH//2, HEIGHT//2), 450)
    screen.blit(glow, (0,0))

    font_title = get_font("serif", 110, bold=True)
    title = font_title.render("BLACKJACK", True, COLOR_GOLD)
    shad = font_title.render("BLACKJACK", True, (0,0,0))
    screen.blit(shad, (WIDTH//2 - shad.get_width()//2 + 6, 96))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 90))

    if player.total_hands > 0:
        bar_rect = pygame.Rect(WIDTH//2 - 300, 250, 600, 40)
        pygame.draw.rect(screen, (40, 40, 50), bar_rect, border_radius=20)
        pygame.draw.rect(screen, COLOR_GOLD, bar_rect, 1, border_radius=20)
        profit = player.get_net_profit()
        sign = "+" if profit >= 0 else ""
        info = f"Solde: ${player.balance}   |   Net: {sign}${profit}"
        draw_shadow_text(screen, info, get_font("sans", 18), COLOR_TEXT_GREY, WIDTH//2, 270, center=True)

    mouse_pos = pygame.mouse.get_pos()
    draw_vip_button(screen, play_rect, "JOUER", play_rect.collidepoint(mouse_pos))
    draw_vip_button(screen, settings_rect, "PARAMÈTRES", settings_rect.collidepoint(mouse_pos))
    draw_vip_button(screen, stats_rect, "STATISTIQUES", stats_rect.collidepoint(mouse_pos))


def draw_game_screen(screen: pygame.Surface, game: Game, player: Player, dealer_revealed: bool, chips, seats):
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

    # Joueur
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


def draw_bet_screen(screen: pygame.Surface, game: Game, player: Player, chips, seats, start_button_rect):
    render_table_bg(screen)
    draw_shadow_text(screen, "CHOISISSEZ VOTRE PLACE & MISE", get_font("serif", 40, True), COLOR_GOLD, WIDTH//2, 50, center=True)

    mouse_pos = pygame.mouse.get_pos()

    # Sieges 
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
            
        draw_shadow_text(screen, f"P{i+1}", get_font("sans", 20, True), col_txt, cx, cy, center=True)

    # Zone de contrôle bas
    
    # mise un peu plus bas
    draw_shadow_text(screen, f"MISE: ${game.player_bet}", get_font("sans", 28, True), COLOR_TEXT_WHITE, WIDTH//2, HEIGHT - 180, center=True)
    
    # bouton distribuer
    is_valid = game.player_bet > 0
    draw_vip_button(screen, start_button_rect, "DISTRIBUER", start_button_rect.collidepoint(mouse_pos), is_active=is_valid)
    
    # jetons 
    for chip in chips:
        if chip["rect"].collidepoint(mouse_pos):
            glow = pygame.Surface((95, 95), pygame.SRCALPHA)
            pygame.draw.circle(glow, (255, 255, 255, 40), (47, 47), 47)
            screen.blit(glow, (chip["rect"].centerx - 47, chip["rect"].centery - 47))
        screen.blit(chip["image"], chip["rect"])

    draw_shadow_text(screen, f"SOLDE: ${player.balance}", get_font("sans", 18, True), COLOR_GOLD, 60, HEIGHT - 30)


def draw_settings_screen(screen: pygame.Surface, game: Game):
    screen.fill(COLOR_ROOM_BG)
    box = pygame.Rect(WIDTH//2 - 300, 100, 600, 500)
    pygame.draw.rect(screen, (30, 30, 35), box, border_radius=20)
    pygame.draw.rect(screen, COLOR_GOLD, box, 2, border_radius=20)
    
    draw_shadow_text(screen, "PARAMÈTRES", get_font("serif", 40, True), COLOR_GOLD, WIDTH//2, 150, center=True)
    
    lines = ["Son: ON", "Musique: OFF", "Difficulté: Normale", "Vitesse: x1"]
    for i, line in enumerate(lines):
        draw_shadow_text(screen, line, get_font("sans", 24), COLOR_TEXT_WHITE, WIDTH//2, 250 + i*50, center=True)
        
    draw_shadow_text(screen, "ESC pour retour", get_font("sans", 18), COLOR_TEXT_GREY, WIDTH//2, 550, center=True)

def draw_stats_screen(screen: pygame.Surface, player: Player):
    screen.fill(COLOR_ROOM_BG)
    draw_shadow_text(screen, "STATISTIQUES", get_font("serif", 40, True), COLOR_GOLD, WIDTH//2, 80, center=True)
    
    grid_x = WIDTH // 2
    grid_y = HEIGHT // 2 + 20
    spacing_x = 300
    spacing_y = 150
    
    def draw_stat(lbl, val, x, y, col):
        draw_shadow_text(screen, lbl, get_font("sans", 20), (180, 180, 180), x, y - 20, center=True)
        draw_shadow_text(screen, str(val), get_font("serif", 36, True), col, x, y + 20, center=True)

    draw_stat("Mains Jouées", player.total_hands, grid_x - spacing_x//2, grid_y - spacing_y//2, COLOR_TEXT_WHITE)
    draw_stat("Victoires", player.wins, grid_x + spacing_x//2, grid_y - spacing_y//2, COLOR_WIN)
    draw_stat("Bénéfice Net", f"${player.get_net_profit()}", grid_x - spacing_x//2, grid_y + spacing_y//2, COLOR_GOLD)
    draw_stat("Blackjacks", player.blackjacks, grid_x + spacing_x//2, grid_y + spacing_y//2, COLOR_GOLD_LIGHT)

    draw_shadow_text(screen, "ESC pour retour", get_font("sans", 18), COLOR_TEXT_GREY, WIDTH//2, HEIGHT - 50, center=True)


#  main loop

def handle_input(game: Game, chips, play_rect, sett_rect, stat_rect, start_rect) -> bool:
    start_round = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if game.state == GameState.MENU:
                if play_rect.collidepoint(pos): game.state = GameState.BETTING
                elif sett_rect.collidepoint(pos): game.state = GameState.SETTINGS
                elif stat_rect.collidepoint(pos): game.state = GameState.STATS
            
            elif game.state == GameState.BETTING:
                for i, seat in enumerate(SEAT_POSITIONS):
                    if seat["rect"].collidepoint(pos):
                        game.seat_index = i
                
                if start_rect.collidepoint(pos) and game.player_bet > 0:
                    start_round = True
                
                for chip in chips:
                    if chip["rect"].collidepoint(pos):
                        if event.button == 1: game.player_bet += chip["value"]
                        elif event.button == 3: game.player_bet = max(0, game.player_bet - chip["value"])

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game.state == GameState.MENU: pygame.quit(); sys.exit()
                else: game.state = GameState.MENU
            
            if game.state == GameState.PLAYER_TURN:
                if event.key == pygame.K_h and game.can_hit(): game.player_hit()
                elif event.key == pygame.K_s and game.can_stand(): game.player_stand()
                elif event.key == pygame.K_d and game.can_double(): game.player_double()
                elif event.key == pygame.K_p and game.can_split(): game.player_split()
                elif event.key == pygame.K_r and game.can_surrender(): game.player_surrender()
                
            if game.state == GameState.RESULT_SCREEN:
                if event.key == pygame.K_SPACE:
                    game.reset()
                    game.player_bet = 0
                    game.state = GameState.BETTING
    return start_round

def main():
    screen, clock = init_pygame()
    player = Player.load()
    game = Game(num_decks=1)
    
    btn_w, btn_h = 280, 60
    play_rect = pygame.Rect(WIDTH//2 - btn_w//2, 380, btn_w, btn_h)
    sett_rect = pygame.Rect(WIDTH//2 - btn_w//2, 460, btn_w, btn_h)
    stat_rect = pygame.Rect(WIDTH//2 - btn_w//2, 540, btn_w, btn_h)
    
    # jetons bien en bas
    chips = []
    chip_y = HEIGHT - 100
    total_chips_w = len(CHIP_FILES) * 95
    start_cx = WIDTH//2 - total_chips_w//2
    for i, (val, name) in enumerate(CHIP_FILES):
        img = load_chip_image(name)
        r = img.get_rect(topleft=(start_cx + i*95, chip_y))
        chips.append({"value": val, "image": img, "rect": r})
        
    start_rect = pygame.Rect(WIDTH//2 - 120, HEIGHT - 160, 240, 50)

    while True:
        dt = clock.tick(FPS) / 1000.0
        game.update(dt)
        should_start = handle_input(game, chips, play_rect, sett_rect, stat_rect, start_rect)
        
        if should_start:
            game.reset()
            game.state = GameState.INITIAL_DEAL
            game.deal_initial_cards()
            
        ct = game.frame_counter
        if game.state == GameState.INITIAL_DEAL and ct > 1.0: game.state = GameState.PLAYER_TURN
        if game.state == GameState.DEALER_REVEAL and ct - game.last_action_time > 1.0:
            game.state = GameState.DEALER_TURN; game.dealer_play()
        if game.state == GameState.DEALER_TURN and ct - game.last_action_time > 1.0:
            game.state = GameState.RESULT_SCREEN
            
        if game.state == GameState.RESULT_SCREEN and not getattr(game, "money_processed", False):
            game.money_processed = True
            if game.has_surrendered: player.lose_hand(game.player_bet // 2)
            elif len(game.hands) > 1:
                for i, h in enumerate(game.hands):
                    res = game.hand_results[i]; bet = game.hand_bets[i]
                    if res == GameResult.PLAYER_WIN:
                        mult = 1.5 if h.is_blackjack() else 1.0
                        player.win_hand(int(bet * mult))
                    elif res == GameResult.DEALER_WIN: player.lose_hand(bet)
                    else: player.push_hand()
            else:
                res = game.result
                if res == GameResult.PLAYER_WIN:
                    mult = 1.5 if game.hands[0].is_blackjack() else 1.0
                    player.win_hand(int(game.hand_bets[0] * mult))
                elif res == GameResult.DEALER_WIN: player.lose_hand(game.hand_bets[0])
                else: player.push_hand()
            player.save()
            
        if game.state != GameState.RESULT_SCREEN:
            game.money_processed = False

        if game.state == GameState.MENU: draw_main_menu(screen, player, play_rect, sett_rect, stat_rect)
        elif game.state == GameState.BETTING: draw_bet_screen(screen, game, player, chips, SEAT_POSITIONS, start_rect)
        elif game.state == GameState.SETTINGS: draw_settings_screen(screen, game)
        elif game.state == GameState.STATS: draw_stats_screen(screen, player)
        else: draw_game_screen(screen, game, player, game.state in [GameState.DEALER_TURN, GameState.RESULT_SCREEN], chips, SEAT_POSITIONS)
        
        pygame.display.flip()

if __name__ == "__main__":
    main()