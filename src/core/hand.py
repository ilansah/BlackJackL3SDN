# core/hand.py

from typing import List
from .card import Card


class Hand:
    """Représente une main (joueur ou croupier) au blackjack."""
    
    def __init__(self):
        self.cards: List[Card] = []
    
    def add_card(self, card: Card) -> None:
        """Ajoute une carte à la main."""
        self.cards.append(card)
    
    def add_cards(self, cards: List[Card]) -> None:
        """Ajoute plusieurs cartes à la main."""
        self.cards.extend(cards)
    
    def get_value(self) -> int:
        """
        Calcule la valeur de la main au blackjack.
        Les as peuvent valoir 1 ou 11 (on essaie de maximiser sans dépasser 21).
        """
        total = 0
        num_aces = 0
        
        # Compte la valeur basique et les as
        for card in self.cards:
            if card.rank == "A":
                num_aces += 1
                total += 11  # On suppose d'abord que l'as vaut 11
            else:
                total += card.value()
        
        # Ajuste les as si nécessaire (redéfinit certains à 1 si on dépasse 21)
        while total > 21 and num_aces > 0:
            total -= 10  # Redéfinir un as de 11 à 1
            num_aces -= 1
        
        return total
    
    def is_blackjack(self) -> bool:
        """Retourne True si c'est un blackjack (21 avec 2 cartes)."""
        return len(self.cards) == 2 and self.get_value() == 21
    
    def is_bust(self) -> bool:
        """Retourne True si la main dépasse 21."""
        return self.get_value() > 21
    
    def is_soft_hand(self) -> bool:
        """Retourne True si la main contient un as comptabilisé comme 11."""
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
        """Vide la main."""
        self.cards.clear()
    
    def __repr__(self) -> str:
        return f"Hand({self.cards} = {self.get_value()})"
