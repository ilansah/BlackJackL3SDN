#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test rapide des fonctionnalités du blackjack amélioré.
"""

from core.card import Card
from core.deck import Deck
from core.hand import Hand
from core.game import Game, GameState
from core.player import Player


def test_player_stats():
    """Test le système de statistiques."""
    print("=== Test des statistiques du joueur ===")
    
    player = Player("TestPlayer")
    assert player.total_hands == 0
    assert player.get_win_rate() == 0.0
    
    player.win_hand(100)
    assert player.wins == 1
    assert player.total_hands == 1
    assert player.total_money_won == 100
    print(f"✓ Victoire enregistrée: {player.to_dict()}")
    
    player.lose_hand(100)
    assert player.losses == 1
    assert player.total_hands == 2
    print(f"✓ Défaite enregistrée")
    
    player.record_blackjack()
    assert player.blackjacks == 1
    print(f"✓ Blackjack enregistré")
    
    win_rate = player.get_win_rate()
    print(f"✓ Taux de victoire: {win_rate:.1f}%")
    
    net = player.get_net_profit()
    print(f"✓ Bénéfice net: ${net}")


def test_game_states():
    """Test les états du jeu."""
    print("\n=== Test des états du jeu ===")
    
    game = Game(num_decks=1)
    assert game.state == GameState.MENU
    print(f"✓ État initial: {game.state.value}")
    
    # Simuler le début d'une partie
    game.state = GameState.INITIAL_DEAL
    assert game.state == GameState.INITIAL_DEAL
    print(f"✓ État après début: {game.state.value}")
    
    game.deal_initial_cards()
    print(f"✓ Cartes distribuées")
    print(f"  Joueur: {game.player_hand.cards} = {game.player_hand.get_value()}")
    print(f"  Croupier: {game.dealer_hand.cards[0]} + ?")
    
    # Vérifier les actions possibles
    can_hit = game.can_hit()
    can_stand = game.can_stand()
    can_double = game.can_double()
    print(f"✓ Actions possibles: hit={can_hit}, stand={can_stand}, double={can_double}")


def test_animation_timing():
    """Test le système de délais."""
    print("\n=== Test des délais d'animation ===")
    
    game = Game(num_decks=1)
    print(f"✓ Délai d'animation: {game.animation_delay}s")
    
    # Simuler l'écoulement du temps
    dt = 0.1
    for i in range(15):
        game.update(dt)
    
    print(f"✓ Temps écoulé simulé: {game.frame_counter:.1f}s")
    assert game.frame_counter > 1.0
    print(f"✓ Suffisant pour les transitions")


def test_player_persistence():
    """Test la sauvegarde/chargement du joueur."""
    print("\n=== Test de persistance des données ===")
    
    # Créer et sauvegarder
    player1 = Player("SaveTest")
    player1.win_hand(200)
    player1.lose_hand(100)
    player1.record_blackjack()
    player1.save("test_player.json")
    print(f"✓ Joueur sauvegardé")
    
    # Charger
    player2 = Player.load("test_player.json")
    assert player2.name == "SaveTest"
    assert player2.wins == 1
    assert player2.losses == 1
    assert player2.blackjacks == 1
    print(f"✓ Joueur chargé correctement")
    print(f"  Stats: {player2.total_hands} mains, {player2.get_win_rate():.0f}% wins")
    
    # Nettoyage
    import os
    os.remove("test_player.json")


if __name__ == "__main__":
    print("🎴 Tests Blackjack v2.0 - Interface Améliorée\n")
    test_player_stats()
    test_game_states()
    test_animation_timing()
    test_player_persistence()
    print("\n✅ Tous les tests réussis!")
    print("\n💡 Pour lancer le jeu: python src/main.py")
