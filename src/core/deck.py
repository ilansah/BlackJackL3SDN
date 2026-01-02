"""Module de gestion du sabot de cartes.

Ce module définit la classe Deck qui représente un sabot de cartes
pouvant contenir un ou plusieurs jeux de 52 cartes.
"""

import random
from .card import Card, RANKS, SUITS


class Deck:
    """Représente un sabot de cartes pour le Blackjack.
    
    Le sabot peut contenir un ou plusieurs jeux de 52 cartes standard.
    Les cartes sont automatiquement mélangées à la création.
    
    Attributes:
        num_decks (int): Le nombre de jeux de 52 cartes dans le sabot
        cards (List[Card]): Liste des cartes restantes dans le sabot
        
    Examples:
        >>> deck = Deck(num_decks=1)
        >>> len(deck.cards)
        52
        >>> cards = deck.draw(2)
        >>> len(cards)
        2
    """
    
    def __init__(self, num_decks: int = 1):
        """Initialise un sabot avec le nombre spécifié de jeux.
        
        Les cartes sont automatiquement mélangées après création.
        
        Args:
            num_decks (int, optional): Nombre de jeux de 52 cartes. Par défaut 1.
            
        Examples:
            >>> deck = Deck(num_decks=6)  # Sabot de 6 jeux (casino)
            >>> len(deck.cards)
            312
        """
        self.num_decks = num_decks
        # Création des cartes en combinant chaque valeur et chaque famille
        self.cards = [Card(r, s) for _ in range(num_decks) for s in SUITS for r in RANKS]
        self.shuffle()

    def shuffle(self) -> None:
        """Mélange aléatoirement toutes les cartes du sabot.
        
        Utilise l'algorithme de Fisher-Yates via random.shuffle().
        """
        random.shuffle(self.cards)

    def draw(self, n: int = 1) -> list[Card]:
        """Tire n cartes du dessus du sabot.
        
        Le sabot est automatiquement réinitialisé et mélangé quand il est vide,
        créant ainsi un paquet infini.
        
        Args:
            n (int, optional): Nombre de cartes à tirer. Par défaut 1.
            
        Returns:
            List[Card]: Liste des cartes tirées
            
        Examples:
            >>> deck = Deck()
            >>> cards = deck.draw(5)
            >>> len(cards)
            5
            >>> len(deck.cards)
            47
        """
        drawn = []
        for _ in range(n):
            # Si le paquet est vide, on le réinitialise automatiquement
            if not self.cards:
                print("🔄 Le paquet est vide, réinitialisation automatique...")
                self.reset()
            drawn.append(self.cards.pop())
        return drawn

    def burn(self, n: int = 1) -> None:
        """Brûle (défausse) n cartes du dessus sans les utiliser.
        
        Cette pratique est courante dans les casinos pour éviter la triche.
        
        Args:
            n (int, optional): Nombre de cartes à brûler. Par défaut 1.
            
        Examples:
            >>> deck = Deck()
            >>> deck.burn(3)  # Brûle 3 cartes
            >>> len(deck.cards)
            49
        """
        for _ in range(n):
            if self.cards:
                self.cards.pop()

    def reset(self) -> None:
        """Réinitialise le sabot avec un nouveau jeu complet mélangé.
        
        Recrée toutes les cartes et les mélange.
        """
        self.__init__(self.num_decks)

