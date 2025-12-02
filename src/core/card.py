
from __future__ import annotations

# toutes les valeurs possibles des cartes
RANKS = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]

# les quatre familles de cartes
SUITS = ["♠", "♥", "♦", "♣"]


class Card:
    # quand on cree une carte on donne sa valeur et sa famille
    def __init__(self, rank: str, suit: str):
        # verifie que la carte existe sinon erreur
        assert rank in RANKS and suit in SUITS, "carte invalide"
        self.rank = rank
        self.suit = suit

    # retourne la valeur numerique de la carte
    # l as vaut 11 pour le moment
    # les figures valent 10
    def value(self) -> int:
        if self.rank == "A":
            return 11
        if self.rank in ("J", "Q", "K"):
            return 10
        return int(self.rank)

    # affiche la carte en texte simple pour debug
    def __repr__(self):
        return f"{self.rank}{self.suit}"