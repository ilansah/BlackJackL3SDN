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
    assert Card("2", "♠").value() == 2
    assert Card("10", "♥").value() == 10
    assert Card("J", "♦").value() == 10
    assert Card("K", "♣").value() == 10
    assert Card("A", "♠").value() == 11
    print("✓ Valeurs des cartes correctes")


def test_hand_value():
    """Test le calcul de la valeur d'une main."""
    print("\n=== Test de la valeur de main ===")
    
    hand = Hand()
    hand.add_cards([Card("5", "♠"), Card("6", "♥")])
    assert hand.get_value() == 11
    print(f"✓ 5 + 6 = {hand.get_value()}")
    
    hand2 = Hand()
    hand2.add_cards([Card("A", "♠"), Card("K", "♥")])
    assert hand2.is_blackjack()
    assert hand2.get_value() == 21
    print(f"✓ A + K = {hand2.get_value()} (BLACKJACK)")
    
    hand3 = Hand()
    hand3.add_cards([Card("A", "♠"), Card("5", "♥"), Card("6", "♣")])
    assert hand3.get_value() == 12  # A vaut 1 ici
    print(f"✓ A + 5 + 6 = {hand3.get_value()} (As comme 1)")


def test_bust():
    """Test la détection du bust."""
    print("\n=== Test du bust ===")
    
    hand = Hand()
    hand.add_cards([Card("K", "♠"), Card("Q", "♥"), Card("5", "♣")])
    assert hand.is_bust()
    assert hand.get_value() > 21
    print(f"✓ K + Q + 5 = {hand.get_value()} (BUST)")


def test_deck():
    """Test le paquet de cartes."""
    print("\n=== Test du deck ===")
    
    deck = Deck(1)
    assert len(deck.cards) == 52
    print(f"✓ Deck avec 52 cartes")
    
    drawn = deck.draw(5)
    assert len(drawn) == 5
    assert len(deck.cards) == 47
    print(f"✓ Tiré 5 cartes, {len(deck.cards)} restantes")


def test_game_flow():
    """Test le flux complet d'une partie."""
    print("\n=== Test du flux de jeu ===")
    
    game = Game(num_decks=1)
    print(f"État initial: {game.state.value}")
    
    # Distribuer les cartes
    game.deal_initial_cards()
    assert game.state.value == "player_turn"
    print(f"✓ Après distribution: état = {game.state.value}")
    print(f"  Joueur: {game.player_hand.cards} = {game.player_hand.get_value()}")
    print(f"  Croupier: {game.dealer_hand.cards} (2ème carte cachée)")
    
    # Le joueur peut tirer
    assert game.can_hit()
    print(f"✓ Le joueur peut tirer")
    
    # Le joueur peut s'arrêter
    assert game.can_stand()
    print(f"✓ Le joueur peut s'arrêter")
    
    # Joueur s'arrête
    game.player_stand()
    assert game.state.value == "dealer_turn"
    print(f"✓ Après stand: état = {game.state.value}")
    
    # Le croupier joue
    game.dealer_play()
    assert game.state.value == "game_over"
    print(f"✓ Après dealer_play: état = {game.state.value}")
    print(f"  Résultat: {game.result.value}")
    print(f"  Joueur final: {game.player_hand.get_value()}")
    print(f"  Croupier final: {game.dealer_hand.get_value()}")


if __name__ == "__main__":
    print("🎴 Tests du Blackjack\n")
    test_card_values()
    test_hand_value()
    test_bust()
    test_deck()
    test_game_flow()
    print("\n✅ Tous les tests réussis!")
