# src/main.py
import sys
import os
import pygame

from core.deck import Deck
from core.card import Card

# reglages de base de la fenetre
WIDTH, HEIGHT = 1280, 720
FPS = 60

# taille affichage des cartes
CARD_W, CARD_H = 100, 145

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


def main():
    screen, clock = init_pygame()

    # cree un paquet et pioche deux cartes a afficher
    deck = Deck(1)
    initial_cards = deck.draw(2)

    # position des cartes du joueur
    start_x = WIDTH // 2 - CARD_W - 20
    y = HEIGHT // 2 + 40
    spacing = CARD_W + 20

    while True:
        _ = handle_events()
        dt = clock.tick(FPS) / 1000.0

        render_table_bg(screen)

        for i, c in enumerate(initial_cards):
            x = start_x + i * spacing
            draw_card(screen, c, x, y)

        # dos du croupier en haut
        draw_back(screen, WIDTH // 2 - CARD_W // 2, 80)

        draw_help_text(screen)

        pygame.display.flip()


# petit texte d aide en bas
def draw_help_text(screen: pygame.Surface):
    pygame.font.init()
    font = pygame.font.SysFont(None, 24)
    txt = "esc pour quitter"
    surf = font.render(txt, True, (255, 255, 255))
    screen.blit(surf, (20, HEIGHT - 36))


if __name__ == "__main__":
    main()
