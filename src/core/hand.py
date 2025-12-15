"""Module de gestion des mains de cartes.

Ce module définit la classe Hand qui représente une main de cartes
pour le joueur ou le croupier dans un jeu de Blackjack.
"""

from typing import List
from .card import Card


class Hand:
    """Représente une main de cartes au Blackjack.
    
    Une main contient une liste de cartes et gère automatiquement
    le calcul de la valeur totale en tenant compte des As.
    
    Attributes:
        cards (List[Card]): Liste des cartes dans la main
        seat_index (int): Index de la place du joueur (pour le mode multi-places)
        
    Examples:
        >>> hand = Hand()
        >>> hand.add_card(Card("A", "♠"))
        >>> hand.add_card(Card("K", "♥"))
        >>> hand.is_blackjack()
        True
    """
    
    def __init__(self, seat_index: int = 0):
        """Initialise une main vide.
        
        Args:
            seat_index (int, optional): Index de la place du joueur. Par défaut 0.
        """
        self.cards: List[Card] = []
        self.seat_index = seat_index
    
    def add_card(self, card: Card) -> None:
        """Ajoute une carte à la main.
        
        Args:
            card (Card): La carte à ajouter
        """
        self.cards.append(card)
    
    def add_cards(self, cards: List[Card]) -> None:
        """Ajoute plusieurs cartes à la main.
        
        Args:
            cards (List[Card]): Liste des cartes à ajouter
        """
        self.cards.extend(cards)
    
    def get_value(self) -> int:
        """Calcule la valeur totale de la main au Blackjack.
        
        Les As peuvent valoir 1 ou 11. La méthode optimise automatiquement
        la valeur des As pour obtenir le meilleur score possible sans dépasser 21.
        
        Returns:
            int: La valeur totale de la main (0-31+)
            
        Examples:
            >>> hand = Hand()
            >>> hand.add_cards([Card("A", "♠"), Card("9", "♥")])
            >>> hand.get_value()
            20
            >>> hand.add_card(Card("5", "♦"))
            >>> hand.get_value()  # L'As vaut maintenant 1
            15
        """
        total = 0
        num_aces = 0
        
        # Compte la valeur basique et les As
        for card in self.cards:
            if card.rank == "A":
                num_aces += 1
                total += 11  # On suppose d'abord que l'As vaut 11
            else:
                total += card.value()
        
        # Ajuste les As si nécessaire
        while total > 21 and num_aces > 0:
            total -= 10  # Redéfinir un As de 11 à 1
            num_aces -= 1
        
        return total
    
    def is_blackjack(self) -> bool:
        """Vérifie si la main est un Blackjack naturel.
        
        Un Blackjack est une main de 2 cartes valant exactement 21.
        
        Returns:
            bool: True si c'est un Blackjack, False sinon
        """
        return len(self.cards) == 2 and self.get_value() == 21
    
    def is_bust(self) -> bool:
        """Vérifie si la main a dépassé 21 (bust).
        
        Returns:
            bool: True si la valeur dépasse 21, False sinon
        """
        return self.get_value() > 21
    
    def is_soft_hand(self) -> bool:
        """Vérifie si la main est une main souple.
        
        Une main souple contient un As comptabilisé comme 11.
        
        Returns:
            bool: True si la main contient un As valant 11, False sinon
            
        Examples:
            >>> hand = Hand()
            >>> hand.add_cards([Card("A", "♠"), Card("6", "♥")])
            >>> hand.is_soft_hand()  # As vaut 11, total = 17
            True
        """
        total = 0
        has_ace_as_11 = False
        
        for card in self.cards:
            if card.rank == "A":
                total += 11
                has_ace_as_11 = True
            else:
                total += card.value()
        
        while total > 21 and has_ace_as_11:
            total -= 10
            has_ace_as_11 = False
        
        return has_ace_as_11
    
    def clear(self) -> None:
        """Vide la main de toutes ses cartes."""
        self.cards.clear()
    
    def __repr__(self) -> str:
        """Retourne une représentation textuelle de la main.
        
        Returns:
            str: La main au format "Hand([cartes] = valeur)"
        """
        return f"Hand({self.cards} = {self.get_value()})"