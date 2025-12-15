"""Module de gestion des cartes à jouer.

Ce module définit la classe Card et les constantes associées pour représenter
les cartes à jouer dans un jeu de Blackjack.
"""

from __future__ import annotations

#: Liste de toutes les valeurs possibles des cartes (As à Roi)
RANKS = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]

#: Liste des quatre familles de cartes (Pique, Cœur, Carreau, Trèfle)
SUITS = ["♠", "♥", "♦", "♣"]


class Card:
    """Représente une carte à jouer.
    
    Une carte est définie par sa valeur (rank) et sa famille (suit).
    
    Attributes:
        rank (str): La valeur de la carte (A, 2-10, J, Q, K)
        suit (str): La famille de la carte (♠, ♥, ♦, ♣)
    
    Examples:
        >>> card = Card("A", "♠")
        >>> print(card)
        A♠
        >>> card.value()
        11
    """
    
    def __init__(self, rank: str, suit: str):
        """Initialise une carte avec sa valeur et sa famille.
        
        Args:
            rank (str): La valeur de la carte, doit être dans RANKS
            suit (str): La famille de la carte, doit être dans SUITS
            
        Raises:
            AssertionError: Si la valeur ou la famille n'est pas valide
        """
        assert rank in RANKS and suit in SUITS, "carte invalide"
        self.rank = rank
        self.suit = suit

    def value(self) -> int:
        """Calcule la valeur numérique de la carte pour le Blackjack.
        
        L'As vaut 11 (ajustement à 1 géré par la classe Hand),
        les figures (J, Q, K) valent 10,
        les autres cartes valent leur valeur nominale.
        
        Returns:
            int: La valeur numérique de la carte (1-11)
            
        Examples:
            >>> Card("A", "♠").value()
            11
            >>> Card("K", "♥").value()
            10
            >>> Card("5", "♦").value()
            5
        """
        if self.rank == "A":
            return 11
        if self.rank in ("J", "Q", "K"):
            return 10
        return int(self.rank)

    def __repr__(self) -> str:
        """Retourne une représentation textuelle de la carte.
        
        Returns:
            str: La carte au format "RangFamille" (ex: "A♠")
        """
        return f"{self.rank}{self.suit}"