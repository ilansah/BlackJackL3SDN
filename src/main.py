import sys
import os
import pygame
import json

from core.deck import Deck
from core.card import Card
from core.game import Game, GameState, GameResult
from core.player import Player

# reglages de base de la fenetre
WIDTH, HEIGHT = 1280, 720
FPS = 60

# taille affichage des cartes
CARD_W, CARD_H = 100, 145

# Couleurs
COLOR_BG = (0, 100, 0)
COLOR_BG_DARK = (20, 60, 20)
COLOR_MENU_BG = (15, 15, 40)
COLOR_TEXT = (255, 255, 255)
COLOR_TEXT_GOLD = (255, 215, 0)
COLOR_WIN = (100, 255, 100)
COLOR_LOSE = (255, 100, 100)
COLOR_PUSH = (255, 255, 100)
COLOR_TEXT_DARK = (50, 50, 50)

# dossier ou sont stockees les cartes
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "cards")

# dossier ou sont stockees les images de jetons
CHIPS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "chips")

# valeur et fichier image des jetons
CHIP_FILES = [
    (5, "chip_5_w85h85.png"),
    (10, "chip_10_w85h85.png"),
    (50, "chip_50_w85h85.png"),
    (100, "chip_100_w85h85.png"),
]


# cache pour eviter de recharger les memes images
_image_cache: dict[str, pygame.Surface] = {}


def init_pygame():
    # demarre pygame cree la fenetre et l'horloge
    pygame.init()
    pygame.display.set_caption("Blackjack")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    return screen, clock


def handle_events():
    # gere clavier souris et fermeture
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    return []


def handle_game_input(
    game: Game,
    chips,
    seats,
    play_button_rect,
    settings_button_rect,
    stats_button_rect,
    bet_start_button_rect,
) -> bool:
    """
    Gère tous les inputs.
    Retourne True si on doit lancer une nouvelle manche.
    """
    start_round = False

    for event in pygame.event.get():

        # quitter jeu
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # souris
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            # menu
            if game.state == GameState.MENU:
                if play_button_rect.collidepoint(pos):
                    game.state = GameState.BETTING
                elif settings_button_rect.collidepoint(pos):
                    game.state = GameState.SETTINGS
                elif stats_button_rect.collidepoint(pos):
                    game.state = GameState.STATS

            #ecran mise
            elif game.state == GameState.BETTING:

                #clic place
                if event.button == 1:
                    for seat in seats:
                        if seat["rect"].collidepoint(pos):
                            game.seat_index = seat["index"]

                    #clicl commencer
                    if bet_start_button_rect.collidepoint(pos) and game.player_bet > 0:
                        start_round = True

                #clic jetons 
                for chip in chips:
                    if chip["rect"].collidepoint(pos):
                        if event.button == 1:          # ajouter mise
                            game.player_bet += chip["value"]
                        elif event.button == 3:        # enlever mise
                            game.player_bet = max(0, game.player_bet - chip["value"])

            # ecran resultat
            elif game.state == GameState.RESULT_SCREEN:

                #auroriser jetons 
                for chip in chips:
                    if chip["rect"].collidepoint(pos):
                        if event.button == 1:
                            game.player_bet += chip["value"]
                        elif event.button == 3:
                            game.player_bet = max(0, game.player_bet - chip["value"])

        #clavier
        if event.type == pygame.KEYDOWN:

            #retour menu principal
            if event.key == pygame.K_ESCAPE:
                game.state = GameState.MENU

            #tour joueur
            if game.state == GameState.PLAYER_TURN:
                if event.key == pygame.K_h and game.can_hit():
                    game.player_hit()
                elif event.key == pygame.K_s and game.can_stand():
                    game.player_stand()
                elif event.key == pygame.K_d and game.can_double():
                    game.player_double()
                elif event.key == pygame.K_p and game.can_split():
                    game.player_split()

            #fin manche
            elif game.state == GameState.RESULT_SCREEN:
                if event.key == pygame.K_SPACE:
                    game.reset()
                    game.player_bet = 0
                    game.state = GameState.BETTING

    return start_round



# conversion des symboles en noms utilises par tes fichiers
def suit_to_word(suit: str) -> str:
    return {"♠": "spades", "♥": "hearts", "♦": "diamonds", "♣": "clubs"}[suit]


# conversion des rangs en mots si besoin
def rank_to_word(rank: str) -> str:
    table = {"A": "ace", "J": "jack", "Q": "queen", "K": "king"}
    return table.get(rank, rank)


# construit le nom de fichier selon ton pack
def card_filename(card: Card) -> str:
    base = f"{rank_to_word(card.rank)}_of_{suit_to_word(card.suit)}"
    return f"{base}.png"


# charge une image en utilisant le cache et la met a l echelle
def load_card_image(filename: str) -> pygame.Surface:
    global _image_cache
    key = filename.lower()
    if key in _image_cache:
        return _image_cache[key]

    #ca tente plusieurs extensions au cas ou
    candidates = [
        filename,
        filename.lower(),
        filename.replace(".png", ".jpg"),
        filename.replace(".png", ".jpeg"),
        filename.replace(".png", ".webp"),
    ]

    img = None
    for name in candidates:
        path = os.path.join(ASSETS_DIR, name)
        if os.path.exists(path):
            try:
                img = pygame.image.load(path).convert_alpha()
                break
            except Exception:
                pass

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
    if key in _image_cache:
        return _image_cache[key]

    path = os.path.join(CHIPS_DIR, filename)
    if not os.path.exists(path):
        # petit placeholder si l'image manque
        surf = pygame.Surface((70, 70), pygame.SRCALPHA)
        pygame.draw.circle(surf, (220, 220, 220), (35, 35), 34, 2)
        _image_cache[key] = surf
        return surf

    img = pygame.image.load(path).convert_alpha()
    _image_cache[key] = img
    return img

# dessine une carte a l ecran
def draw_card(screen: pygame.Surface, card: Card, x: int, y: int):
    img = load_card_image(card_filename(card))
    screen.blit(img, (x, y))


# dessine le dos d une carte
def draw_back(screen: pygame.Surface, x: int, y: int):
    for name in ["back-side.png", "back.png", "BACK.png"]:
        img = load_card_image(name)
        if img is not None:
            screen.blit(img, (x, y))
            return


# fond de table vert
def render_table_bg(screen: pygame.Surface):
    screen.fill(COLOR_BG)
    pygame.draw.line(screen, COLOR_BG_DARK, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 3)


def draw_main_menu(screen: pygame.Surface, player: Player,
                   play_rect, settings_rect, stats_rect):
    screen.fill(COLOR_MENU_BG)

    pygame.font.init()
    font_title = pygame.font.SysFont("arial", 80, bold=True)
    font_button = pygame.font.SysFont("arial", 36)
    font_small = pygame.font.SysFont("arial", 20)

    # titre
    title = font_title.render("BLACKJACK", True, COLOR_TEXT_GOLD)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

    # stats rapides
    if player.total_hands > 0:
        stats_text = (
            f"Mains: {player.total_hands} | "
            f"Victoires: {player.wins} | "
            f"Taux: {player.get_win_rate():.1f}% | "
            f"Bénéfice: ${player.get_net_profit()}"
        )
        surf = font_small.render(stats_text, True, COLOR_TEXT)
        screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, 150))

    # fonction utilitaire pour dessiner un bouton
    def draw_button(rect, text):
        pygame.draw.rect(screen, COLOR_BG_DARK, rect, border_radius=10)
        pygame.draw.rect(screen, COLOR_TEXT_GOLD, rect, 2, border_radius=10)
        txt = font_button.render(text, True, COLOR_TEXT)
        screen.blit(
            txt,
            (rect.centerx - txt.get_width() // 2,
             rect.centery - txt.get_height() // 2)
        )

    draw_button(play_rect, "Jouer")
    draw_button(settings_rect, "Settings")
    draw_button(stats_rect, "Stats")



def draw_game_screen(screen: pygame.Surface, game: Game, player: Player, dealer_revealed: bool, chips, seats):

    """Affiche l'écran de jeu."""
    render_table_bg(screen)
    
    pygame.font.init()
    font_small = pygame.font.SysFont("arial", 20)
    font_medium = pygame.font.SysFont("arial", 28)
    font_large = pygame.font.SysFont("arial", 40)

    # placement
    TABLE_LINE_Y = HEIGHT // 2              # ligne de séparation
    DEALER_CARDS_Y = 150                    # cartes du croupier
    PLAYER_CARDS_Y = TABLE_LINE_Y + 70      # cartes du joueur
    STATUS_Y = TABLE_LINE_Y - 40            # message central
    DEALER_TEXT_Y = DEALER_CARDS_Y - 60
    PLAYER_TEXT_Y = PLAYER_CARDS_Y - 60

    # pos cartes
    player_start_x = WIDTH // 2 - CARD_W - 20
    dealer_start_x = WIDTH // 2 - CARD_W - 20
    spacing = CARD_W + 20

    # carte croupier
    if not dealer_revealed and game.state in [GameState.INITIAL_DEAL, GameState.PLAYER_TURN]:
        draw_back(screen, dealer_start_x, DEALER_CARDS_Y)
        if len(game.dealer_hand.cards) > 1:
            draw_card(screen, game.dealer_hand.cards[1], dealer_start_x + spacing, DEALER_CARDS_Y)
    else:
        for i, card in enumerate(game.dealer_hand.cards):
            draw_card(screen, card, dealer_start_x + i * spacing, DEALER_CARDS_Y)

    # mess croupier
    dealer_value = game.dealer_hand.get_value()
    dealer_text = f"Croupier: {dealer_value}"
    if game.state not in (GameState.INITIAL_DEAL, GameState.PLAYER_TURN):
        if game.dealer_hand.is_bust():
            dealer_text += " (BUST!)"
        elif game.dealer_hand.is_blackjack():
            dealer_text += " (BLACKJACK)"
    surf = font_large.render(dealer_text, True, COLOR_TEXT_GOLD)
    screen.blit(surf, (20, DEALER_TEXT_Y))

    # carte joueur
    for i, card in enumerate(game.player_hand.cards):
        draw_card(screen, card, player_start_x + i * spacing, PLAYER_CARDS_Y)

    # Texte joueur
    player_value = game.player_hand.get_value()
    player_text = f"Votre main: {player_value}"
    if game.player_hand.is_bust():
        player_text += " (BUST!)"
        player_color = COLOR_LOSE
    elif game.player_hand.is_blackjack():
        player_text += " (BLACKJACK!)"
        player_color = COLOR_WIN
    else:
        player_color = COLOR_WIN

    surf = font_large.render(player_text, True, player_color)
    screen.blit(surf, (20, PLAYER_TEXT_Y))

    # mess principal
    status_text = game.get_status_message()
    status_color = COLOR_TEXT
    if game.state == GameState.RESULT_SCREEN:
        if game.result == GameResult.PLAYER_WIN:
            status_color = COLOR_WIN
        elif game.result == GameResult.DEALER_WIN:
            status_color = COLOR_LOSE
        else:
            status_color = COLOR_PUSH

    status = font_large.render(status_text, True, status_color)
    screen.blit(status, (WIDTH // 2 - status.get_width() // 2, STATUS_Y))

    # options clavier
    if game.state == GameState.PLAYER_TURN:
        options = []
        if game.can_hit():
            options.append("H - Hit")
        if game.can_stand():
            options.append("S - Stand")
        if game.can_double():
            options.append("D - Double")
        if game.can_split():
            options.append("P - Split")
        
        opt_text = " | ".join(options)
        surf = font_medium.render(opt_text, True, COLOR_TEXT_GOLD)
        screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, HEIGHT - 150))

    if game.state == GameState.RESULT_SCREEN:
        space_text = font_medium.render("SPACE pour nouvelle partie", True, COLOR_TEXT_GOLD)
        screen.blit(space_text, (WIDTH // 2 - space_text.get_width() // 2, HEIGHT - 150))

    # barre des stats
    stats_bar_text = (
        f"Joueur: {player.name} | Mains: {player.total_hands} | "
        f"Victoires: {player.wins} | Défaites: {player.losses} | "
        f"Taux: {player.get_win_rate():.1f}% | Bénéfice: ${player.get_net_profit()}"
    )
    surf = font_small.render(stats_bar_text, True, COLOR_TEXT_GOLD)
    rect = surf.get_rect()
    rect.topleft = (10, 5)
    pygame.draw.rect(screen, COLOR_BG_DARK, rect.inflate(20, 10))
    screen.blit(surf, (20, 10))

    # mise et conseils
    bet_text = f"Mise: ${game.player_bet}"
    surf = font_small.render(bet_text, True, COLOR_TEXT)
    screen.blit(surf, (20, HEIGHT - 30))

    help_text = "SPACE - Nouvelle partie | ESC - Quitter"
    surf = font_small.render(help_text, True, COLOR_TEXT)
    screen.blit(surf, (WIDTH - surf.get_width() - 20, HEIGHT - 30))

    # jetons
    # on n'affiche pas les jetons sur ecran de jeu
    pass



def draw_bet_screen(screen: pygame.Surface, game: Game, player: Player,
                    chips, seats, start_button_rect):
    screen.fill(COLOR_MENU_BG)

    pygame.font.init()
    font_title = pygame.font.SysFont("arial", 60, bold=True)
    font_large = pygame.font.SysFont("arial", 32)
    font_medium = pygame.font.SysFont("arial", 24)
    font_small = pygame.font.SysFont("arial", 18)

    #titre
    title = font_title.render("Placez votre mise", True, COLOR_TEXT_GOLD)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

    #siege
    label = font_medium.render("Choisissez votre place :", True, COLOR_TEXT)
    screen.blit(label, (20, 120))

    for seat in seats:
        idx = seat["index"]
        cx, cy = seat["center"]

        if idx == game.seat_index:
            color = COLOR_TEXT_GOLD
            thickness = 0
        else:
            color = COLOR_TEXT
            thickness = 2

        pygame.draw.circle(screen, color, (cx, cy), 35, thickness)

        txt = font_small.render(f"Place {idx + 1}", True, COLOR_TEXT)
        screen.blit(txt, (cx - txt.get_width() // 2, cy + 40))

    #jetons
    for chip in chips:
        screen.blit(chip["image"], chip["rect"].topleft)

    bet_text = font_large.render(f"Mise actuelle : ${game.player_bet}", True, COLOR_TEXT)
    screen.blit(bet_text, (20, HEIGHT - 150))


    # Bouton démarrer
    if game.player_bet > 0:
        btn_color = (0, 150, 0)
        btn_text = "Commencer la partie"
    else:
        btn_color = (80, 80, 80)
        btn_text = "Choisissez d'abord une mise"

    pygame.draw.rect(screen, btn_color, start_button_rect, border_radius=10)
    txt = font_medium.render(btn_text, True, COLOR_TEXT)
    screen.blit(
        txt,
        (
            start_button_rect.centerx - txt.get_width() // 2,
            start_button_rect.centery - txt.get_height() // 2,
        ),
    )


def draw_settings_screen(screen: pygame.Surface, game: Game):
    """Affiche l'écran des paramètres."""
    screen.fill(COLOR_MENU_BG)

    pygame.font.init()
    font_title = pygame.font.SysFont("arial", 60, bold=True)
    font_large = pygame.font.SysFont("arial", 32)
    font_medium = pygame.font.SysFont("arial", 24)
    font_small = pygame.font.SysFont("arial", 18)

    # Titre
    title = font_title.render("PARAMÈTRES", True, COLOR_TEXT_GOLD)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

    # Charger les settings
    try:
        with open("config/settings.json", "r") as f:
            settings = json.load(f)
    except:
        settings = {}

    # Colonnes
    col1_x = 40
    col2_x = WIDTH // 2 + 20
    y_start = 130
    line_height = 40

    # ===== COLONNE 1 =====
    
    # Section Jeu
    game_title = font_large.render("Paramètres du Jeu", True, COLOR_TEXT_GOLD)
    screen.blit(game_title, (col1_x, y_start))

    game_settings = settings.get("game", {})
    y_pos = y_start + 50
    game_items = [
        ("Résolution", f"{game_settings.get('width', 1280)}x{game_settings.get('height', 720)}"),
        ("FPS", str(game_settings.get('fps', 60))),
        ("Nombre de decks", str(game_settings.get('num_decks', 1))),
    ]

    for label, value in game_items:
        text = font_medium.render(f"{label}: {value}", True, COLOR_TEXT)
        screen.blit(text, (col1_x + 20, y_pos))
        y_pos += line_height

    # Section Cartes
    y_pos += 20
    cards_title = font_large.render("Affichage Cartes", True, COLOR_TEXT_GOLD)
    screen.blit(cards_title, (col1_x, y_pos))

    cards_settings = settings.get("cards", {})
    y_pos += 50
    card_items = [
        ("Largeur", str(cards_settings.get('width', 100))),
        ("Hauteur", str(cards_settings.get('height', 145))),
        ("Espacement", str(cards_settings.get('spacing', 20))),
    ]

    for label, value in card_items:
        text = font_medium.render(f"{label}: {value}", True, COLOR_TEXT)
        screen.blit(text, (col1_x + 20, y_pos))
        y_pos += line_height

    # ===== COLONNE 2 =====

    # Section Timing
    y_pos_col2 = y_start
    timing_title = font_large.render("Timing (secondes)", True, COLOR_TEXT_GOLD)
    screen.blit(timing_title, (col2_x, y_pos_col2))

    timing_settings = settings.get("timing", {})
    y_pos_col2 += 50
    timing_items = [
        ("Distribution", timing_settings.get('initial_deal_duration', 1.0)),
        ("Révélation", timing_settings.get('dealer_reveal_duration', 1.0)),
        ("Résultats", timing_settings.get('result_screen_duration', 3.0)),
    ]

    for label, value in timing_items:
        text = font_medium.render(f"{label}: {value}s", True, COLOR_TEXT)
        screen.blit(text, (col2_x + 20, y_pos_col2))
        y_pos_col2 += line_height

    # Section Joueur
    y_pos_col2 += 20
    player_title = font_large.render("Paramètres Joueur", True, COLOR_TEXT_GOLD)
    screen.blit(player_title, (col2_x, y_pos_col2))

    player_settings = settings.get("player", {})
    y_pos_col2 += 50
    player_items = [
        ("Solde initial", f"${player_settings.get('starting_balance', 1000)}"),
        ("Mise min", f"${player_settings.get('min_bet', 5)}"),
        ("Mise max", f"${player_settings.get('max_bet', 1000)}"),
    ]

    for label, value in player_items:
        text = font_medium.render(f"{label}: {value}", True, COLOR_TEXT)
        screen.blit(text, (col2_x + 20, y_pos_col2))
        y_pos_col2 += line_height

    # Section Fonctionnalités
    y_pos_col2 += 20
    features_title = font_large.render("Fonctionnalités", True, COLOR_TEXT_GOLD)
    screen.blit(features_title, (col2_x, y_pos_col2))

    features_settings = settings.get("features", {})
    y_pos_col2 += 50
    features_items = [
        ("Son", "Activé" if features_settings.get('sound_enabled', False) else "Désactivé"),
        ("Animations", "Activées" if features_settings.get('animations_enabled', True) else "Désactivées"),
        ("Conseils", "Activés" if features_settings.get('show_hints', True) else "Désactivés"),
    ]

    for label, value in features_items:
        color = COLOR_WIN if "Activé" in value else COLOR_LOSE
        text = font_medium.render(f"{label}: {value}", True, color)
        screen.blit(text, (col2_x + 20, y_pos_col2))
        y_pos_col2 += line_height

    # Indication
    esc_text = font_small.render("ESC pour retour au menu", True, COLOR_TEXT_GOLD)
    screen.blit(esc_text, (WIDTH // 2 - esc_text.get_width() // 2, HEIGHT - 40))


def draw_stats_screen(screen: pygame.Surface, player: Player):
    """Affiche l'écran des statistiques détaillées."""
    screen.fill(COLOR_MENU_BG)

    pygame.font.init()
    font_title = pygame.font.SysFont("arial", 60, bold=True)
    font_large = pygame.font.SysFont("arial", 32)
    font_medium = pygame.font.SysFont("arial", 24)
    font_small = pygame.font.SysFont("arial", 18)

    # Titre
    title = font_title.render("STATISTIQUES DÉTAILLÉES", True, COLOR_TEXT_GOLD)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))

    # Nom du joueur
    player_name = font_large.render(f"Joueur: {player.name}", True, COLOR_TEXT_GOLD)
    screen.blit(player_name, (40, 110))

    # Colonnes
    col1_x = 40
    col2_x = WIDTH // 2 + 20
    y_start = 180
    line_height = 45

    # ===== COLONNE 1 : RÉSULTATS =====
    
    results_title = font_large.render("RÉSULTATS", True, COLOR_TEXT_GOLD)
    screen.blit(results_title, (col1_x, y_start))

    y_pos = y_start + 60
    
    # Total de mains
    text = font_medium.render(f"Total mains: {player.total_hands}", True, COLOR_TEXT)
    screen.blit(text, (col1_x + 20, y_pos))
    y_pos += line_height

    # Victoires
    text = font_medium.render(f"Victoires: {player.wins}", True, COLOR_WIN)
    screen.blit(text, (col1_x + 20, y_pos))
    y_pos += line_height

    # Défaites
    text = font_medium.render(f"Défaites: {player.losses}", True, COLOR_LOSE)
    screen.blit(text, (col1_x + 20, y_pos))
    y_pos += line_height

    # Égalités
    text = font_medium.render(f"Égalités: {player.pushes}", True, COLOR_PUSH)
    screen.blit(text, (col1_x + 20, y_pos))
    y_pos += line_height

    # Blackjacks
    text = font_medium.render(f"Blackjacks: {player.blackjacks}", True, COLOR_TEXT_GOLD)
    screen.blit(text, (col1_x + 20, y_pos))

    # ===== COLONNE 2 : PERFORMANCES =====
    
    perf_title = font_large.render("PERFORMANCES", True, COLOR_TEXT_GOLD)
    screen.blit(perf_title, (col2_x, y_start))

    y_pos_col2 = y_start + 60
    
    # Taux de victoire
    win_rate = player.get_win_rate()
    if player.total_hands > 0:
        win_rate_color = COLOR_WIN if win_rate >= 50 else COLOR_TEXT
    else:
        win_rate_color = COLOR_TEXT
    text = font_medium.render(f"Taux victoire: {win_rate:.1f}%", True, win_rate_color)
    screen.blit(text, (col2_x + 20, y_pos_col2))
    y_pos_col2 += line_height

    # Moyenne par main
    avg_per_hand = 0 if player.total_hands == 0 else player.get_net_profit() // player.total_hands
    text = font_medium.render(f"Moy/main: ${avg_per_hand:+d}", True, COLOR_TEXT)
    screen.blit(text, (col2_x + 20, y_pos_col2))
    y_pos_col2 += line_height

    # Bénéfice net
    net_profit = player.get_net_profit()
    profit_color = COLOR_WIN if net_profit >= 0 else COLOR_LOSE
    text = font_medium.render(f"Bénéfice net: ${net_profit:+d}", True, profit_color)
    screen.blit(text, (col2_x + 20, y_pos_col2))
    y_pos_col2 += line_height

    # Ratio W/L
    if player.losses > 0:
        ratio = player.wins / player.losses
        ratio_color = COLOR_WIN if ratio > 1 else COLOR_LOSE
    else:
        ratio = 0
        ratio_color = COLOR_TEXT
    text = font_medium.render(f"Ratio W/L: {ratio:.2f}", True, ratio_color)
    screen.blit(text, (col2_x + 20, y_pos_col2))

    # ===== COLONNE GAUCHE : MONNAIE =====
    
    y_pos += line_height + 30
    money_title = font_large.render("MONNAIE", True, COLOR_TEXT_GOLD)
    screen.blit(money_title, (col1_x, y_pos))

    y_pos += 60
    
    # Argent gagné
    text = font_medium.render(f"Argent gagné: ${player.total_money_won}", True, COLOR_WIN)
    screen.blit(text, (col1_x + 20, y_pos))
    y_pos += line_height

    # Argent perdu
    text = font_medium.render(f"Argent perdu: ${player.total_money_lost}", True, COLOR_LOSE)
    screen.blit(text, (col1_x + 20, y_pos))

    # ===== COLONNE DROITE : POURCENTAGES =====
    
    y_pos_col2_stats = y_pos - line_height + 30
    stats_title = font_large.render("POURCENTAGES", True, COLOR_TEXT_GOLD)
    screen.blit(stats_title, (col2_x, y_pos_col2_stats))

    y_pos_col2_stats += 60
    
    # % victoires
    if player.total_hands > 0:
        pct_wins = (player.wins / player.total_hands) * 100
        pct_losses = (player.losses / player.total_hands) * 100
        pct_pushes = (player.pushes / player.total_hands) * 100
    else:
        pct_wins = pct_losses = pct_pushes = 0

    text = font_medium.render(f"Victoires: {pct_wins:.1f}%", True, COLOR_WIN)
    screen.blit(text, (col2_x + 20, y_pos_col2_stats))
    y_pos_col2_stats += line_height

    text = font_medium.render(f"Défaites: {pct_losses:.1f}%", True, COLOR_LOSE)
    screen.blit(text, (col2_x + 20, y_pos_col2_stats))
    y_pos_col2_stats += line_height

    text = font_medium.render(f"Égalités: {pct_pushes:.1f}%", True, COLOR_PUSH)
    screen.blit(text, (col2_x + 20, y_pos_col2_stats))

    # Indication et conseil
    esc_text = font_small.render("ESC pour retour au menu", True, COLOR_TEXT_GOLD)
    screen.blit(esc_text, (WIDTH // 2 - esc_text.get_width() // 2, HEIGHT - 40))



def main():
    screen, clock = init_pygame()
    
    # Charger ou créer le profil du joueur
    player = Player.load()
    
    # Démarrer directement une partie
    game = Game(num_decks=1)
    game.state = GameState.MENU
    game.player_bet = 0
    dealer_revealed = False
    state_changed_time = 0


    # bouton menu
    menu_button_width = 300
    menu_button_height = 60
    menu_button_x = WIDTH // 2 - menu_button_width // 2
    menu_start_y = 220
    menu_button_margin = 20

    play_button_rect = pygame.Rect(
        menu_button_x, menu_start_y, menu_button_width, menu_button_height
    )
    settings_button_rect = pygame.Rect(
        menu_button_x, menu_start_y + (menu_button_height + menu_button_margin),
        menu_button_width, menu_button_height
    )
    stats_button_rect = pygame.Rect(
        menu_button_x, menu_start_y + 2 * (menu_button_height + menu_button_margin),
        menu_button_width, menu_button_height
    )

    # sieges
    NUM_SEATS = 5
    seats = []
    seat_y = HEIGHT // 2 + 120
    seat_radius = 35
    seat_spacing = WIDTH // (NUM_SEATS + 1)

    for i in range(NUM_SEATS):
        center_x = (i + 1) * seat_spacing
        rect = pygame.Rect(center_x - seat_radius, seat_y - seat_radius,
                           seat_radius * 2, seat_radius * 2)
        seats.append({"index": i, "center": (center_x, seat_y), "rect": rect})

    game.seat_index = NUM_SEATS // 2  

    # jetons
    chips = []
    chip_margin = 20
    chip_y = HEIGHT - 110

    sample_img = load_chip_image(CHIP_FILES[0][1])
    chip_w, chip_h = sample_img.get_size()
    total_width = len(CHIP_FILES) * chip_w + (len(CHIP_FILES) - 1) * chip_margin
    start_x = WIDTH // 2 - total_width // 2

    for i, (value, filename) in enumerate(CHIP_FILES):
        img = load_chip_image(filename)
        rect = img.get_rect()
        rect.topleft = (start_x + i * (chip_w + chip_margin), chip_y)
        chips.append({"value": value, "image": img, "rect": rect})

    #bouton commencer
    bet_start_button_rect = pygame.Rect(
        WIDTH // 2 - 150,
        HEIGHT - 200,
        300,
        50
    )


    while True:

        dt = clock.tick(FPS) / 1000.0
        game.update(dt)

        # gere inputs
        start_round = handle_game_input(
            game,
            chips,
            seats,
            play_button_rect,
            settings_button_rect,
            stats_button_rect,
            bet_start_button_rect,
        )

        # lance nouvelle manche
        if start_round:
            game.reset()                   
            dealer_revealed = False
            state_changed_time = 0
            game.state = GameState.INITIAL_DEAL
            game.deal_initial_cards()      

        # gestion des transi auto
        current_time = game.frame_counter

        #transition INITIAL_DEAL vers PLAYER_TURN
        if game.state == GameState.INITIAL_DEAL and current_time > 1.0:
            game.state = GameState.PLAYER_TURN

        #transition DEALER_REVEAL vers DEALER_TURN
        if game.state == GameState.DEALER_REVEAL and current_time - game.last_action_time > 1.0:
            dealer_revealed = True
            game.state = GameState.DEALER_TURN
            game.dealer_play()

        #transition DEALER_TURN vers RESULT_SCREEN
        if game.state == GameState.DEALER_TURN and current_time - game.last_action_time > 1.0:
            game.state = GameState.RESULT_SCREEN

        # qd  partie finie enregistrer stats une fois
        if game.state == GameState.RESULT_SCREEN and state_changed_time == 0:
            state_changed_time = current_time

            if game.result == GameResult.PLAYER_WIN:
                player.win_hand(game.player_bet)
                if game.player_hand.is_blackjack():
                    player.record_blackjack()

            elif game.result == GameResult.DEALER_WIN:
                player.lose_hand(game.player_bet)

            else:
                player.push_hand()

            player.save()

        #affiche selon etat
        if game.state == GameState.MENU:
            draw_main_menu(
                screen,
                player,
                play_button_rect,
                settings_button_rect,
                stats_button_rect
            )

        elif game.state == GameState.BETTING:
            draw_bet_screen(
                screen,
                game,
                player,
                chips,
                seats,
                bet_start_button_rect
            )

        elif game.state == GameState.SETTINGS:
            draw_settings_screen(screen, game)

        elif game.state == GameState.STATS:
            draw_stats_screen(screen, player)

        else:
            # ecran jeu nrml
            draw_game_screen(
                screen,
                game,
                player,
                dealer_revealed,
                chips,
                seats
            )

        pygame.display.flip()



if __name__ == "__main__":
    main()
