
from typing import List
from .card import Card


class Hand:
    # represente une main joueur ou croupier
    
    def __init__(self):
        self.cards: List[Card] = []
    
    def add_card(self, card: Card) -> None:
        # ajoute une carte a la main
        self.cards.append(card)
    
    def add_cards(self, cards: List[Card]) -> None:
        # ajoute plusieurs cartes a la main
        self.cards.extend(cards)
    
    def get_value(self) -> int:
        # calcule la valeur de la main au blackjack
        # les as peuvent valoir 1 ou 11
        total = 0
        num_aces = 0
        
        # compte la valeur basique et les as
        for card in self.cards:
            if card.rank == "A":
                num_aces += 1
                total += 11 # on suppose d abord que l as vaut 11
            else:
                total += card.value()
        
        # ajuste les as si necessaire
        while total > 21 and num_aces > 0:
            total -= 10 # redefinir un as de 11 a 1
            num_aces -= 1
        
        return total
    
    def is_blackjack(self) -> bool:
        # retourne true si c est un blackjack 21 avec 2 cartes
        return len(self.cards) == 2 and self.get_value() == 21
    
    def is_bust(self) -> bool:
        # retourne true si la main depasse 21
        return self.get_value() > 21
    
    def is_soft_hand(self) -> bool:
        # retourne true si la main contient un as comptabilise comme 11
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
        # vide la main
        self.cards.clear()
    
    def __repr__(self) -> str:
        return f"Hand({self.cards} = {self.get_value()})"