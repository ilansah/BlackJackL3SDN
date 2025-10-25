# core/deck.py

import random
from .card import Card, RANKS, SUITS


class Deck:
    # creation du paquet de cartes
    # num_decks = combien de jeux on veut (par defaut 1)
    def __init__(self, num_decks: int = 1):
        self.num_decks = num_decks  # garde le nombre de jeux
        # creation des cartes en combinant chaque valeur et chaque famille
        self.cards = [Card(r, s) for _ in range(num_decks) for s in SUITS for r in RANKS]
        self.shuffle()  # on melange des la creation

    # melange les cartes du paquet
    def shuffle(self) -> None:
        random.shuffle(self.cards)

    # tire n cartes du paquet
    def draw(self, n: int = 1):
        drawn = []  # liste des cartes tirees
        for _ in range(n):
            if not self.cards:  # si plus de carte
                raise RuntimeError("le paquet est vide")
            drawn.append(self.cards.pop())  # retire une carte du dessus
        return drawn  # retourne les cartes tirees

    # brule n cartes sans les utiliser
    def burn(self, n: int = 1):
        for _ in range(n):
            if self.cards:
                self.cards.pop()

    # remet le paquet a neuf en recreant toutes les cartes
    def reset(self):
        self.__init__(self.num_decks)

