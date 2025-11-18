# src/main.py
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
# on part du dossier src on remonte d'un cran puis assets cards
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "cards")

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


def handle_game_input(game: Game):
    """Gère les inputs du joueur pendant son tour."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_h and game.can_hit():  # H = Hit
                game.player_hit()
            elif event.key == pygame.K_s and game.can_stand():  # S = Stand
                game.player_stand()
            elif event.key == pygame.K_d and game.can_double():  # D = Double
                game.player_double()
            elif event.key == pygame.K_p and game.can_split():  # P = sPlIt
                game.player_split()
            elif event.key == pygame.K_SPACE and game.state == GameState.GAME_OVER:
                # SPACE pour commencer une nouvelle partie
                game.reset()
                game.deal_initial_cards()


# conversion des symboles en noms utilises par tes fichiers
# exemple pique devient spades coeur devient hearts
def suit_to_word(suit: str) -> str:
    return {"♠": "spades", "♥": "hearts", "♦": "diamonds", "♣": "clubs"}[suit]


# conversion des rangs en mots si besoin
# a devient ace, j devient jack, q devient queen, k devient king sinon chiffre tel quel
def rank_to_word(rank: str) -> str:
    table = {"A": "ace", "J": "jack", "Q": "queen", "K": "king"}
    return table.get(rank, rank)


# construit le nom de fichier selon ton pack
# exemples
# A de pique donne ace_of_spades.png
# 10 de coeur donne 10_of_hearts.png
def card_filename(card: Card) -> str:
    base = f"{rank_to_word(card.rank)}_of_{suit_to_word(card.suit)}"
    return f"{base}.png"


# charge une image en utilisant le cache et la met a l echelle
def load_card_image(filename: str) -> pygame.Surface:
    global _image_cache
    key = filename.lower()
    if key in _image_cache:
        return _image_cache[key]

    # on tente plusieurs extensions au cas ou
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
        # placeholder si le fichier n existe pas
        surf = pygame.Surface((CARD_W, CARD_H), pygame.SRCALPHA)
        surf.fill((230, 230, 230))
        pygame.draw.rect(surf, (50, 50, 50), surf.get_rect(), 2)
        _image_cache[key] = surf
        return surf

    img = pygame.transform.smoothscale(img, (CARD_W, CARD_H))
    _image_cache[key] = img
    return img


# dessine une carte a l ecran
def draw_card(screen: pygame.Surface, card: Card, x: int, y: int):
    img = load_card_image(card_filename(card))
    screen.blit(img, (x, y))


# dessine le dos d une carte
# ton pack utilise back side png on tente aussi back png et BACK png
def draw_back(screen: pygame.Surface, x: int, y: int):
    for name in ["back-side.png", "back.png", "BACK.png"]:
        img = load_card_image(name)
        if img is not None:
            screen.blit(img, (x, y))
            return


# update general pour animations a venir
def update(dt: float):
    pass


# fond de table vert et ligne au milieu
def render_table_bg(screen: pygame.Surface):
    screen.fill((0, 100, 0))
    pygame.draw.line(screen, (20, 60, 20), (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 3)


def draw_player_options(screen: pygame.Surface, game: Game, font: pygame.font.Font):
    """Affiche les options disponibles au joueur."""
    if game.state != GameState.PLAYER_TURN:
        return
    
    options = []
    
    if game.can_hit():
        options.append("H - Hit (Tirer)")
    if game.can_stand():
        options.append("S - Stand (S'arrêter)")
    if game.can_double():
        options.append("D - Double")
    if game.can_split():
        options.append("P - Split (Diviser)")
    
    y_start = HEIGHT - 100
    for i, option in enumerate(options):
        color = (100, 255, 100)
        surf = font.render(option, True, color)
        screen.blit(surf, (WIDTH - 250, y_start + i * 25))



def main():
    screen, clock = init_pygame()

    # Créer une partie interactive
    game = Game(num_decks=1)
    game.deal_initial_cards()  # Distribuer les cartes initiales

    # Position des cartes du joueur
    player_start_x = WIDTH // 2 - CARD_W - 20
    player_y = HEIGHT // 2 + 100
    spacing = CARD_W + 20

    # Position des cartes du croupier
    dealer_start_x = WIDTH // 2 - CARD_W - 20
    dealer_y = 80

    while True:
        # Gérer les inputs du joueur
        if game.state == GameState.PLAYER_TURN:
            handle_game_input(game)
        elif game.state == GameState.INITIAL_DEAL:
            # Attendre un instant puis commencer
            pass
        elif game.state == GameState.DEALER_TURN:
            # Le croupier joue automatiquement
            game.dealer_play()
        elif game.state == GameState.GAME_OVER:
            # Attendre l'entrée du joueur pour continuer
            handle_game_input(game)
        else:
            handle_events()

        dt = clock.tick(FPS) / 1000.0

        # Rendu
        render_table_bg(screen)

        # Affiche les cartes du croupier
        pygame.font.init()
        font_small = pygame.font.SysFont(None, 20)
        font_large = pygame.font.SysFont(None, 36)
        
        # En mode INITIAL_DEAL, on montre le dos d'une carte du croupier (pas vue)
        if game.state == GameState.INITIAL_DEAL:
            draw_back(screen, dealer_start_x, dealer_y)
            if len(game.dealer_hand.cards) > 1:
                draw_card(screen, game.dealer_hand.cards[1], dealer_start_x + spacing, dealer_y)
        else:
            # Après le tour du joueur, on montre toutes les cartes du croupier
            for i, card in enumerate(game.dealer_hand.cards):
                x = dealer_start_x + i * spacing
                draw_card(screen, card, x, dealer_y)
            
            # Affiche la main du croupier
            dealer_text = f"Croupier: {game.dealer_hand.get_value()}"
            surf = font_large.render(dealer_text, True, (255, 255, 100))
            screen.blit(surf, (20, dealer_y - 35))

        # Affiche les cartes du joueur
        for i, card in enumerate(game.player_hand.cards):
            x = player_start_x + i * spacing
            draw_card(screen, card, x, player_y)

        # Affiche la main du joueur
        player_value = game.player_hand.get_value()
        player_text = f"Joueur: {player_value}"
        if game.player_hand.is_bust():
            player_text += " (BUST)"
        elif game.player_hand.is_blackjack():
            player_text += " (BLACKJACK)"
        
        player_color = (255, 100, 100) if game.player_hand.is_bust() else (100, 255, 100)
        surf = font_large.render(player_text, True, player_color)
        screen.blit(surf, (20, player_y - 35))

        # Affiche le statut/résultat
        status_text = game.get_status_message()
        status_color = (255, 255, 255)
        
        if game.state == GameState.GAME_OVER:
            if game.result.value == "player_win":
                status_color = (100, 255, 100)
            elif game.result.value == "dealer_win":
                status_color = (255, 100, 100)
            else:
                status_color = (255, 255, 100)
        
        status_surf = font_large.render(status_text, True, status_color)
        screen.blit(status_surf, (WIDTH // 2 - status_surf.get_width() // 2, HEIGHT // 2 - 100))

        # Afficher les options disponibles
        draw_player_options(screen, game, font_small)

        draw_help_text(screen)

        pygame.display.flip()


# petit texte d aide en bas
def draw_help_text(screen: pygame.Surface):
    pygame.font.init()
    font = pygame.font.SysFont(None, 24)
    txt = "ESC pour quitter | SPACE pour nouvelle partie (en fin)"
    surf = font.render(txt, True, (255, 255, 255))
    screen.blit(surf, (20, HEIGHT - 36))


if __name__ == "__main__":
    main()
