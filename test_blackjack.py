#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test rapide des fonctionnalités du blackjack sans l'interface graphique.
"""

from core.card import Card
from core.deck import Deck
from core.hand import Hand
from core.game import Game


def test_card_values():
    """Test les valeurs des cartes."""
    print("=== Test des valeurs des cartes ===")
    assert Card("2", "S").value() == 2
    assert Card("10", "H").value() == 10
    assert Card("J", "D").value() == 10
    assert Card("K", "C").value() == 10
    assert Card("A", "S").value() == 11
    print("[OK] Valeurs des cartes correctes")


def test_hand_value():
    """Test le calcul de la valeur d'une main."""
    print("\n=== Test de la valeur de main ===")
    
    hand = Hand()
    hand.add_cards([Card("5", "S"), Card("6", "H")])
    assert hand.get_value() == 11
    print(f"[OK] 5 + 6 = {hand.get_value()}")
    
    hand2 = Hand()
    hand2.add_cards([Card("A", "S"), Card("K", "H")])
    assert hand2.is_blackjack()
    assert hand2.get_value() == 21
    print(f"[OK] A + K = {hand2.get_value()} (BLACKJACK)")
    
    hand3 = Hand()
    hand3.add_cards([Card("A", "S"), Card("5", "H"), Card("6", "C")])
    assert hand3.get_value() == 12  # A vaut 1 ici
    print(f"[OK] A + 5 + 6 = {hand3.get_value()} (As comme 1)")


def test_bust():
    """Test la détection du bust."""
    print("\n=== Test du bust ===")
    
    hand = Hand()
    hand.add_cards([Card("K", "S"), Card("Q", "H"), Card("5", "C")])
    assert hand.is_bust()
    assert hand.get_value() > 21
    print(f"[OK] K + Q + 5 = {hand.get_value()} (BUST)")


def test_deck():
    """Test le paquet de cartes."""
    print("\n=== Test du deck ===")
    
    deck = Deck(1)
    assert len(deck.cards) == 52
    print(f"[OK] Deck avec 52 cartes")
    
    drawn = deck.draw(5)
    assert len(drawn) == 5
    assert len(deck.cards) == 47
    print(f"[OK] Tire 5 cartes, {len(deck.cards)} restantes")


def test_game_flow():
    """Test le flux complet d'une partie."""
    print("\n=== Test du flux de jeu ===")
    
    game = Game(num_decks=1)
    print(f"État initial: {game.state.value}")
    
    # Distribuer les cartes
    game.deal_initial_cards()
    assert game.state.value == "player_turn"
    print(f"[OK] Apres distribution: etat = {game.state.value}")
    print(f"  Joueur: {game.player_hand.cards} = {game.player_hand.get_value()}")
    print(f"  Croupier: {game.dealer_hand.cards} (2eme carte cachee)")
    
    # Le joueur peut tirer
    assert game.can_hit()
    print(f"[OK] Le joueur peut tirer")
    
    # Le joueur peut s'arreter
    assert game.can_stand()
    print(f"[OK] Le joueur peut s'arreter")
    
    # Joueur s'arrete
    game.player_stand()
    assert game.state.value == "dealer_turn"
    print(f"[OK] Apres stand: etat = {game.state.value}")
    
    # Le croupier joue
    game.dealer_play()
    assert game.state.value == "game_over"
    print(f"[OK] Apres dealer_play: etat = {game.state.value}")
    print(f"  Résultat: {game.result.value}")
    print(f"  Joueur final: {game.player_hand.get_value()}")
    print(f"  Croupier final: {game.dealer_hand.get_value()}")


if __name__ == "__main__":
    print("Tests du Blackjack\n")
    test_card_values()
    test_hand_value()
    test_bust()
    test_deck()
    test_game_flow()
    print("\nTous les tests réussis!")
