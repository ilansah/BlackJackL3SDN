import sys
import os
import pygame
import json
import math

from core.deck import Deck
from core.card import Card
from core.game import Game, GameState, GameResult
from core.player import Player
from config_manager import get_config_manager

#  config graphique 
WIDTH, HEIGHT = 1600, 900
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
# Musique
MUSIC_FILE = os.path.join(os.path.dirname(__file__), "..", "Indochine - Jai demandé à la lune (Clip officiel).mp3")
music_enabled = True
music_volume = 0.5


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
    colors = get_table_colors()
    # table ellipse large et aplatie
    table_rect = pygame.Rect(-200, HEIGHT // 2 - 120, WIDTH + 400, HEIGHT + 200)
    pygame.draw.ellipse(screen, COLOR_WOOD_RAIL, table_rect)
    felt_rect = table_rect.inflate(-60, -60)
    pygame.draw.ellipse(screen, colors['felt'], felt_rect)
    pygame.draw.arc(screen, colors['felt_arc'], felt_rect.inflate(-100, -100), 0, 3.14, 2)
    
    font_logo = get_font("serif", 40, bold=True)
    logo_rect = draw_shadow_text(screen, "PRIVÉ LOUNGE", font_logo, (0, 90, 100), WIDTH//2, HEIGHT//2 - 40, center=True)
    font_sub = get_font("sans", 16, bold=True)
    draw_shadow_text(screen, "BLACKJACK PAYS 3 TO 2", font_sub, (0, 140, 150), WIDTH//2, logo_rect.bottom + 5, center=True)

#  ecrans

def draw_main_menu(screen: pygame.Surface, player: Player, play_rect, settings_rect, stats_rect, clicker_rect):
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
    draw_vip_button(screen, clicker_rect, "CLICKER", clicker_rect.collidepoint(mouse_pos))


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



def draw_bet_screen(screen: pygame.Surface, game: Game, player: Player, chips, seats, start_button_rect):
    render_table_bg(screen)
    draw_shadow_text(screen, "CHOISISSEZ VOTRE PLACE & MISE", get_font("serif", 40, True), COLOR_GOLD, WIDTH//2, 50, center=True)

    mouse_pos = pygame.mouse.get_pos()

    # Sieges - afficher les mises sur chaque place
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
            draw_shadow_text(screen, f"${game.seat_bets[i]}", get_font("sans", 16, True), COLOR_GOLD, cx, bet_y, center=True)

    # Zone de contrôle bas
    
    # mise totale
    total_bet = sum(game.seat_bets.values())
    active_seats = sum(1 for bet in game.seat_bets.values() if bet > 0)
    if total_bet > 0:
        bet_text = f"MISE TOTALE: ${total_bet} ({active_seats} place{'s' if active_seats > 1 else ''})"
    else:
        bet_text = "Sélectionnez une place et ajoutez des jetons"
    draw_shadow_text(screen, bet_text, get_font("sans", 24, True), COLOR_TEXT_WHITE, WIDTH//2, HEIGHT - 180, center=True)
    
    # bouton distribuer
    is_valid = total_bet > 0
    draw_vip_button(screen, start_button_rect, "DISTRIBUER", start_button_rect.collidepoint(mouse_pos), is_active=is_valid)
    
    # jetons 
    for chip in chips:
        if chip["rect"].collidepoint(mouse_pos):
            glow = pygame.Surface((95, 95), pygame.SRCALPHA)
            pygame.draw.circle(glow, (255, 255, 255, 40), (47, 47), 47)
            screen.blit(glow, (chip["rect"].centerx - 47, chip["rect"].centery - 47))
        screen.blit(chip["image"], chip["rect"])

    # Afficher le solde en haut à gauche pour qu'il soit toujours visible
    solde_panel = pygame.Rect(20, 20, 200, 40)
    pygame.draw.rect(screen, (20, 25, 30), solde_panel, border_radius=10)
    pygame.draw.rect(screen, COLOR_WOOD_RAIL, solde_panel, 2, border_radius=10)
    draw_shadow_text(screen, f"SOLDE: ${player.balance}", get_font("sans", 18, True), COLOR_GOLD, solde_panel.centerx, solde_panel.centery, center=True)


def draw_settings_screen(screen: pygame.Surface, game: Game):
    screen.fill(COLOR_ROOM_BG)
    box = pygame.Rect(WIDTH//2 - 400, 80, 800, 560)
    pygame.draw.rect(screen, (30, 30, 35), box, border_radius=20)
    pygame.draw.rect(screen, COLOR_GOLD, box, 2, border_radius=20)
    
    draw_shadow_text(screen, "PARAMÈTRES", get_font("serif", 40, True), COLOR_GOLD, WIDTH//2, 120, center=True)
    
    config = get_config_manager()
    mouse_pos = pygame.mouse.get_pos()
    
    y_start = 220
    y_spacing = 70
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
    
    # 3. Réinitialiser les statistiques
    reset_rect = pygame.Rect(x_center, y_start + y_spacing * 2, 280, control_height)
    reset_hover = reset_rect.collidepoint(mouse_pos)
    draw_vip_button(screen, reset_rect, "Réinitialiser Stats", reset_hover)
    controls.append(('button', 'reset_stats', reset_rect))
    
    # 4. Thème de la table
    theme_rect = pygame.Rect(x_center, y_start + y_spacing * 3, control_width, control_height)
    themes = ["Vert", "Bleu", "Rouge", "Noir"]
    current_theme = config.get('ui.table_theme', 'green')
    theme_map = {"green": 0, "blue": 1, "red": 2, "black": 3}
    theme_index = theme_map.get(current_theme, 0)
    theme_hover = theme_rect.collidepoint(mouse_pos)
    draw_cycle_button(screen, theme_rect, themes, theme_index, "Thème Table", theme_hover)
    controls.append(('cycle', 'ui.table_theme', theme_rect, themes))
    
    game.settings_controls = controls
    
    draw_shadow_text(screen, "ESC pour retour", get_font("sans", 18), COLOR_TEXT_GREY, WIDTH//2, 620, center=True)


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


def draw_clicker_screen(screen: pygame.Surface, player: Player, click_button_rect, total_clicks):
    """Écran du clicker pour gagner de l'argent"""
    screen.fill(COLOR_ROOM_BG)
    
    # Titre
    draw_shadow_text(screen, "CLICKER", get_font("serif", 60, True), COLOR_GOLD, WIDTH//2, 80, center=True)
    draw_shadow_text(screen, "Cliquez pour gagner de l'argent!", get_font("sans", 24), COLOR_TEXT_WHITE, WIDTH//2, 150, center=True)
    
    # Affichage du solde actuel
    balance_text = f"Solde: ${player.balance}"
    draw_shadow_text(screen, balance_text, get_font("serif", 40, True), COLOR_GOLD_LIGHT, WIDTH//2, 220, center=True)
    
    # Affichage du nombre de clics
    clicks_text = f"Clics: {total_clicks}"
    draw_shadow_text(screen, clicks_text, get_font("sans", 28), COLOR_TEXT_WHITE, WIDTH//2, 280, center=True)
    
    # Bouton de clic géant
    mouse_pos = pygame.mouse.get_pos()
    is_hover = click_button_rect.collidepoint(mouse_pos)
    
    # Effet de hover
    button_color = COLOR_GOLD_LIGHT if is_hover else COLOR_GOLD
    shadow_offset = 6 if not is_hover else 3
    
    # Ombre du bouton
    shadow_center = (click_button_rect.centerx, click_button_rect.centery + shadow_offset)
    pygame.draw.circle(screen, (5, 5, 5), shadow_center, click_button_rect.width // 2)
    
    # Bouton principal
    pygame.draw.circle(screen, button_color, click_button_rect.center, click_button_rect.width // 2)
    pygame.draw.circle(screen, COLOR_GOLD_LIGHT if is_hover else COLOR_TEXT_WHITE, click_button_rect.center, click_button_rect.width // 2, 5)
    
    # Texte sur le bouton
    button_text = "+$1"
    draw_shadow_text(screen, button_text, get_font("serif", 60, True), (0, 0, 0), click_button_rect.centerx, click_button_rect.centery, center=True)
    
    # Instructions
    draw_shadow_text(screen, "Cliquez sur le bouton pour gagner 1$ par clic!", get_font("sans", 20), COLOR_TEXT_GREY, WIDTH//2, HEIGHT - 120, center=True)
    draw_shadow_text(screen, "ESC pour retour au menu", get_font("sans", 18), COLOR_TEXT_GREY, WIDTH//2, HEIGHT - 50, center=True)


#  main loop

def handle_input(game: Game, player: Player, chips, play_rect, sett_rect, stat_rect, clicker_rect, start_rect, click_button_rect, total_clicks) -> tuple[bool, int]:
    start_round = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if game.state == GameState.MENU:
                if play_rect.collidepoint(pos): game.state = GameState.BETTING
                elif sett_rect.collidepoint(pos): game.state = GameState.SETTINGS
                elif stat_rect.collidepoint(pos): game.state = GameState.STATS
                elif clicker_rect.collidepoint(pos): game.state = GameState.CLICKER
            
            elif game.state == GameState.CLICKER:
                # Gestion du clic sur le bouton du clicker
                if click_button_rect.collidepoint(pos):
                    player.earn_money(1)
                    total_clicks += 1
                    player.save()  # Sauvegarder après chaque clic
            
            elif game.state == GameState.BETTING:
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
                            # Calculer la mise totale actuelle
                            current_total_bet = sum(game.seat_bets.values())
                            # Vérifier si le joueur a assez d'argent pour ajouter ce jeton
                            if current_total_bet + chip["value"] <= player.balance:
                                if game.current_seat_for_betting not in game.seat_bets:
                                    game.seat_bets[game.current_seat_for_betting] = 0
                                game.seat_bets[game.current_seat_for_betting] += chip["value"]
                        elif event.button == 3:
                            if game.current_seat_for_betting in game.seat_bets:
                                game.seat_bets[game.current_seat_for_betting] = max(0, game.seat_bets[game.current_seat_for_betting] - chip["value"])

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
                            elif control_type == 'slider':
                                # Commencer le drag
                                game.dragging_slider = control
                            
                            elif control_type == 'button':
                                # Gérer les boutons spéciaux
                                if config_key == 'reset_stats':
                                    # Réinitialiser les statistiques du joueur
                                    player.reset_stats()
                                    player.save()


        
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

        
        if event.type == pygame.MOUSEBUTTONUP:
            if hasattr(game, 'dragging_slider'):
                game.dragging_slider = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game.state == GameState.MENU: pygame.quit(); sys.exit()
                elif game.state == GameState.CLICKER: 
                    game.state = GameState.MENU
                    player.save()  # Sauvegarder avant de quitter le clicker
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
                    pygame.mixer.music.stop()
            
            if game.state == GameState.PLAYER_TURN:
                if event.key == pygame.K_h and game.can_hit(): game.player_hit()
                elif event.key == pygame.K_s and game.can_stand(): game.player_stand()
                elif event.key == pygame.K_d and game.can_double(): game.player_double()
                elif event.key == pygame.K_p and game.can_split(): game.player_split()
                elif event.key == pygame.K_r and game.can_surrender(): game.player_surrender()
                
            if game.state == GameState.RESULT_SCREEN:
                if event.key == pygame.K_SPACE:
                    game.reset()
                    game.seat_bets = {}
                    game.state = GameState.BETTING
    return start_round, total_clicks

def main():
    screen, clock = init_pygame()
    player = Player.load()
    game = Game(num_decks=1)
    
    btn_w, btn_h = 280, 60
    play_rect = pygame.Rect(WIDTH//2 - btn_w//2, 380, btn_w, btn_h)
    sett_rect = pygame.Rect(WIDTH//2 - btn_w//2, 460, btn_w, btn_h)
    stat_rect = pygame.Rect(WIDTH//2 - btn_w//2, 540, btn_w, btn_h)
    clicker_rect = pygame.Rect(WIDTH//2 - btn_w//2, 620, btn_w, btn_h)
    
    # Bouton du clicker (bouton circulaire géant)
    click_button_size = 200
    click_button_rect = pygame.Rect(WIDTH//2 - click_button_size//2, HEIGHT//2 - click_button_size//2 + 50, click_button_size, click_button_size)
    total_clicks = 0
    
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
        should_start, total_clicks = handle_input(game, player, chips, play_rect, sett_rect, stat_rect, clicker_rect, start_rect, click_button_rect, total_clicks)
        
        if should_start:
            game.reset()
            game.state = GameState.INITIAL_DEAL
            # Utiliser le dealing multi-places si des mises sont placées sur plusieurs sièges
            if game.seat_bets:
                game.deal_initial_cards_multiseat()
            else:
                game.deal_initial_cards()
            
        ct = game.frame_counter
        if game.state == GameState.INITIAL_DEAL and ct > 1.0: game.state = GameState.PLAYER_TURN
        if game.state == GameState.DEALER_REVEAL and ct - game.last_action_time > 1.0:
            game.state = GameState.DEALER_TURN; game.dealer_play()
        if game.state == GameState.DEALER_TURN and ct - game.last_action_time > 1.0:
            game.state = GameState.RESULT_SCREEN
            
        if game.state == GameState.RESULT_SCREEN and not getattr(game, "money_processed", False):
            game.money_processed = True
            
            # Multi-seat: traiter chaque place active
            if game.active_seats:
                for seat_idx in game.active_seats:
                    res = game.seat_results[seat_idx]
                    bet = game.seat_bets[seat_idx]
                    hand = game.seat_hands[seat_idx]
                    
                    if res == GameResult.PLAYER_WIN:
                        mult = 1.5 if hand.is_blackjack() else 1.0
                        player.win_hand(int(bet * mult))
                    elif res == GameResult.DEALER_WIN:
                        player.lose_hand(bet)
                    else:
                        player.push_hand()
            elif game.has_surrendered:
                player.lose_hand(game.player_bet // 2)
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

        if game.state == GameState.MENU: draw_main_menu(screen, player, play_rect, sett_rect, stat_rect, clicker_rect)
        elif game.state == GameState.CLICKER: draw_clicker_screen(screen, player, click_button_rect, total_clicks)
        elif game.state == GameState.BETTING: draw_bet_screen(screen, game, player, chips, SEAT_POSITIONS, start_rect)
        elif game.state == GameState.SETTINGS: draw_settings_screen(screen, game)
        elif game.state == GameState.STATS: draw_stats_screen(screen, player)
        else: draw_game_screen(screen, game, player, game.state in [GameState.DEALER_TURN, GameState.RESULT_SCREEN], chips, SEAT_POSITIONS)
        
        pygame.display.flip()

if __name__ == "__main__":
    main()