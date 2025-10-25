# core/card.py

from __future__ import annotations

# toutes les valeurs possibles des cartes
RANKS = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]

# les quatre familles de cartes pique coeur carreau trefle
SUITS = ["♠", "♥", "♦", "♣"]  # on garde les symboles juste pour debug en console


class Card:
    # quand on cree une carte on donne sa valeur et sa famille
    def __init__(self, rank: str, suit: str):
        # verifie que la carte existe sinon erreur
        assert rank in RANKS and suit in SUITS, "carte invalide"
        self.rank = rank  # exemple "A" ou "10" ou "K"
        self.suit = suit  # exemple "♠" ou "♥"

    # retourne la valeur numerique de la carte
    # l as vaut 11 pour le moment
    # les figures valent 10
    # les autres prennent leur chiffre
    def value(self) -> int:
        if self.rank == "A":
            return 11
        if self.rank in ("J", "Q", "K"):
            return 10
        return int(self.rank)

    # affiche la carte en texte simple pour debug
    # ex print(Card("A","♠")) affiche A♠
    def __repr__(self):
        return f"{self.rank}{self.suit}"

