# core/game.py

from enum import Enum
from .deck import Deck
from .hand import Hand


class GameState(Enum):
    """États possibles d'une partie."""
    MENU = "menu"                      # Menu principal (Jouer / Settings / Stats)
    BETTING = "betting"                # Écran de mise (place + jetons)
    SETTINGS = "settings"              # Écran des paramètres
    STATS = "stats"                    # Écran des stats détaillées
    INITIAL_DEAL = "initial_deal"      # Distribution initiale (2 cartes chacun)
    PLAYER_TURN = "player_turn"        # Tour du joueur (choisir action)
    DEALER_REVEAL = "dealer_reveal"    # Révéler la carte cachée du croupier
    DEALER_TURN = "dealer_turn"        # Tour du croupier
    RESULT_SCREEN = "result_screen"    # Afficher le résultat
    GAME_OVER = "game_over"
    WAITING_TO_CONTINUE = "waiting"



class GameResult(Enum):
    """Résultats possibles."""
    PLAYER_WIN = "player_win"
    DEALER_WIN = "dealer_win"
    PUSH = "push"                      # Égalité


class PlayerAction(Enum):
    """Actions possibles du joueur."""
    HIT = "hit"                        # Tirer une carte
    STAND = "stand"                    # S'arrêter
    DOUBLE = "double"                  # Doubler la mise (tirer 1 carte supplémentaire)
    SPLIT = "split"                    # Diviser si les 2 cartes ont la même valeur


class Game:
    """Gère une partie de blackjack complète."""
    
    def __init__(self, num_decks: int = 1):
        """
        Initialise une partie.
        
        Args:
            num_decks: Nombre de jeux dans le sabot
        """
        self.deck = Deck(num_decks)
        
        # Système de mains multiples pour le split
        self.hands = [Hand()]  # Liste des mains du joueur (peut contenir plusieurs mains après split)
        self.hand_bets = [0]  # Mise pour chaque main
        self.hand_results = [None]  # Résultat pour chaque main
        self.current_hand_index = 0  # Index de la main actuellement jouée
        
        self.dealer_hand = Hand()
        self.state = GameState.MENU
        self.result = None  # Résultat global (utilisé quand pas de split)
        self.frame_counter = 0
        self.animation_delay = 0.5  # Délai entre les actions (secondes)
        self.player_action = None  # Action en attente du joueur
        self.player_bet = 0  # Mise initiale
        self.seat_index = 0  # Place choisie (0..4) par défaut
        self.last_action_time = 0  # Timestamp de la dernière action
        
        # Insurance (assurance)
        self.insurance_bet = 0
        self.has_insurance = False
        self.insurance_offered = False
        
        # Surrender (abandon)
        self.has_surrendered = False
    
    def reset(self) -> None:
        """Réinitialise pour une nouvelle partie."""
        self.hands = [Hand()]
        self.hand_bets = [0]
        self.hand_results = [None]
        self.current_hand_index = 0
        self.dealer_hand.clear()
        self.result = None
        self.frame_counter = 0
        self.player_action = None
        self.last_action_time = 0
        self.insurance_bet = 0
        self.has_insurance = False
        self.insurance_offered = False
        self.has_surrendered = False
    
    def can_hit(self) -> bool:
        """Retourne True si le joueur peut tirer."""
        return self.state == GameState.PLAYER_TURN
    
    def can_stand(self) -> bool:
        """Retourne True si le joueur peut s'arrêter."""
        return self.state == GameState.PLAYER_TURN
    
    def can_double(self) -> bool:
        """Retourne True si le joueur peut doubler (seulement avec 2 cartes initiales)."""
        if self.state != GameState.PLAYER_TURN:
            return False
        current_hand = self.hands[self.current_hand_index]
        return len(current_hand.cards) == 2
    
    def can_split(self) -> bool:
        """Retourne True si le joueur peut splitter (2 cartes de même valeur, pas encore de split)."""
        if self.state != GameState.PLAYER_TURN:
            return False
        # On ne peut splitter que s'il n'y a qu'une seule main (pas de split déjà effectué)
        if len(self.hands) > 1:
            return False
        current_hand = self.hands[0]
        if len(current_hand.cards) != 2:
            return False
        # Vérifier que les deux cartes ont la même valeur
        return current_hand.cards[0].value() == current_hand.cards[1].value()
    
    def get_status_message(self) -> str:
        """Retourne un message décrivant l'état actuel."""
        if self.state == GameState.MENU:
            return "BLACKJACK"
        elif self.state == GameState.INITIAL_DEAL:
            return "Distribution des cartes..."
        elif self.state == GameState.PLAYER_TURN:
            current_hand = self.hands[self.current_hand_index]
            msg = f"À vous de jouer (main={current_hand.get_value()})"
            if len(self.hands) > 1:
                msg = f"Main {self.current_hand_index + 1}/{len(self.hands)} - {msg}"
            return msg
        elif self.state == GameState.DEALER_REVEAL:
            return "Révélation du croupier..."
        elif self.state == GameState.DEALER_TURN:
            return f"Le croupier joue"
        elif self.state == GameState.RESULT_SCREEN:
            if self.has_surrendered:
                return "🏁 Vous avez abandonné (50% retourné)"
            if self.result == GameResult.PLAYER_WIN:
                return "🎉 Vous avez gagné!"
            elif self.result == GameResult.DEALER_WIN:
                return "😔 Le croupier a gagné"
            else:
                return "⚖️ Égalité!"
        else:
            return "Attente..."
    
    def update(self, dt: float) -> None:
        """Met à jour l'état du jeu (gestion des délais d'animation)."""
        self.frame_counter += dt
    
    # ===== Méthodes utilitaires =====
    
    def get_current_hand(self) -> Hand:
        """Retourne la main actuellement jouée."""
        return self.hands[self.current_hand_index]
    
    def is_playing_split_hands(self) -> bool:
        """Vérifie si on joue des mains splittées."""
        return len(self.hands) > 1
    
    def can_take_insurance(self) -> bool:
        """Retourne True si le joueur peut prendre l'assurance."""
        # L'assurance est proposée quand le croupier a un As visible
        if len(self.dealer_hand.cards) < 1:
            return False
        return self.dealer_hand.cards[0].rank == "A" and not self.insurance_offered
    
    def can_surrender(self) -> bool:
        """Retourne True si le joueur peut abandonner (seulement au début du tour)."""
        if self.state != GameState.PLAYER_TURN:
            return False
        # On peut abandonner seulement avec 2 cartes et pas de split
        current_hand = self.hands[self.current_hand_index]
        return len(current_hand.cards) == 2 and len(self.hands) == 1
    
    def switch_to_next_hand(self) -> bool:
        """
        Passe à la main suivante après stand/bust.
        Retourne True s'il reste des mains à jouer, False sinon.
        """
        self.current_hand_index += 1
        if self.current_hand_index < len(self.hands):
            return True
        else:
            # Toutes les mains ont été jouées
            return False
    
    # ===== Actions du joueur =====
    
    def player_hit(self) -> None:
        """Le joueur tire une carte."""
        if not self.can_hit():
            return
        
        current_hand = self.hands[self.current_hand_index]
        current_hand.add_cards(self.deck.draw(1))
        self.last_action_time = self.frame_counter
        
        # Vérifier si la main a bust
        if current_hand.is_bust():
            self.hand_results[self.current_hand_index] = GameResult.DEALER_WIN
            # Passer à la main suivante ou terminer
            if not self.switch_to_next_hand():
                # Toutes les mains ont été jouées
                self.state = GameState.DEALER_REVEAL

    
    def player_stand(self) -> None:
        """Le joueur s'arrête et passe à la main suivante ou au croupier."""
        if not self.can_stand():
            return
        
        # Passer à la main suivante ou au croupier
        if not self.switch_to_next_hand():
            # Toutes les mains ont été jouées, le croupier joue
            self.state = GameState.DEALER_REVEAL
        
        self.last_action_time = self.frame_counter
    
    def player_double(self) -> None:
        """Le joueur double sa mise et tire 1 carte."""
        if not self.can_double():
            return
        
        # Doubler la mise de la main actuelle
        self.hand_bets[self.current_hand_index] *= 2
        
        current_hand = self.hands[self.current_hand_index]
        current_hand.add_cards(self.deck.draw(1))
        self.last_action_time = self.frame_counter
        
        if current_hand.is_bust():
            self.hand_results[self.current_hand_index] = GameResult.DEALER_WIN
        
        # Après un double, on passe automatiquement à la main suivante ou au croupier
        if not self.switch_to_next_hand():
            self.state = GameState.DEALER_REVEAL
    
    def player_split(self) -> None:
        """Le joueur divise sa main (si possible)."""
        if not self.can_split():
            return
        
        # Créer une deuxième main avec la deuxième carte
        original_hand = self.hands[0]
        second_card = original_hand.cards.pop()
        
        # Créer la nouvelle main
        new_hand = Hand()
        new_hand.add_cards([second_card])
        self.hands.append(new_hand)
        
        # Dupliquer la mise pour la nouvelle main
        self.hand_bets.append(self.hand_bets[0])
        self.hand_results.append(None)
        
        # Donner une nouvelle carte à chaque main
        self.hands[0].add_cards(self.deck.draw(1))
        self.hands[1].add_cards(self.deck.draw(1))
        
        # Jouer la première main
        self.current_hand_index = 0
        self.last_action_time = self.frame_counter
    
    def take_insurance(self) -> None:
        """Le joueur prend l'assurance (max 50% de la mise)."""
        if not self.can_take_insurance():
            return
        
        # L'assurance coûte 50% de la mise initiale
        self.insurance_bet = self.player_bet // 2
        self.has_insurance = True
        self.insurance_offered = True
    
    def decline_insurance(self) -> None:
        """Le joueur refuse l'assurance."""
        self.insurance_offered = True
        self.has_insurance = False
    
    def player_surrender(self) -> None:
        """Le joueur abandonne et récupère 50% de sa mise."""
        if not self.can_surrender():
            return
        
        self.has_surrendered = True
        # Le joueur récupère 50% de sa mise (perd 50%)
        self.result = GameResult.DEALER_WIN  # Techniquement une perte, mais avec remboursement partiel
        self.state = GameState.RESULT_SCREEN
        self.last_action_time = self.frame_counter

    
    def dealer_play(self) -> None:
        """Le croupier joue selon la règle fixe : tire si < 17, s'arrête sinon."""
        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_cards(self.deck.draw(1))
        
        # Comparer et déterminer le gagnant
        self._determine_winner()
    
    def _determine_winner(self) -> None:
        """Compare les mains et détermine le gagnant."""
        dealer_value = self.dealer_hand.get_value()
        dealer_bust = dealer_value > 21
        
        # Si on a plusieurs mains (split), calculer le résultat pour chaque main
        if len(self.hands) > 1:
            for i, hand in enumerate(self.hands):
                if self.hand_results[i] is not None:
                    # Résultat déjà déterminé (bust)
                    continue
                
                player_value = hand.get_value()
                
                if dealer_bust:
                    self.hand_results[i] = GameResult.PLAYER_WIN
                elif player_value > dealer_value:
                    self.hand_results[i] = GameResult.PLAYER_WIN
                elif dealer_value > player_value:
                    self.hand_results[i] = GameResult.DEALER_WIN
                else:
                    self.hand_results[i] = GameResult.PUSH
            
            # Déterminer le résultat global (pour l'affichage)
            wins = sum(1 for r in self.hand_results if r == GameResult.PLAYER_WIN)
            losses = sum(1 for r in self.hand_results if r == GameResult.DEALER_WIN)
            if wins > losses:
                self.result = GameResult.PLAYER_WIN
            elif losses > wins:
                self.result = GameResult.DEALER_WIN
            else:
                self.result = GameResult.PUSH
        else:
            # Une seule main
            player_value = self.hands[0].get_value()
            
            if dealer_bust:
                self.result = GameResult.PLAYER_WIN
            elif player_value > 21:
                self.result = GameResult.DEALER_WIN
            elif player_value > dealer_value:
                self.result = GameResult.PLAYER_WIN
            elif dealer_value > player_value:
                self.result = GameResult.DEALER_WIN
            else:
                self.result = GameResult.PUSH
            
            self.hand_results[0] = self.result
        
        # Gérer l'assurance
        if self.has_insurance and self.dealer_hand.is_blackjack():
            # Le joueur gagne l'assurance (paiement 2:1)
            pass  # Sera géré dans le calcul des gains
        
        self.state = GameState.RESULT_SCREEN
    
    def deal_initial_cards(self) -> None:
        """Distribue les 2 cartes initiales au joueur et au croupier."""
        # Initialiser la mise de la première main
        self.hand_bets[0] = self.player_bet
        
        # Donner 1 carte au joueur, 1 au croupier, puis 1 au joueur, 1 au croupier
        self.hands[0].add_cards(self.deck.draw(1))
        self.dealer_hand.add_cards(self.deck.draw(1))
        self.hands[0].add_cards(self.deck.draw(1))
        self.dealer_hand.add_cards(self.deck.draw(1))
        
        # Vérifier les blackjacks initiaux
        player_bj = self.hands[0].is_blackjack()
        dealer_bj = self.dealer_hand.is_blackjack()
        
        if player_bj and dealer_bj:
            # Les deux ont un blackjack = égalité
            self.result = GameResult.PUSH
            self.hand_results[0] = GameResult.PUSH
            self.state = GameState.RESULT_SCREEN
        elif player_bj:
            # Joueur a un blackjack, gagne
            self.result = GameResult.PLAYER_WIN
            self.hand_results[0] = GameResult.PLAYER_WIN
            self.state = GameState.RESULT_SCREEN
        elif dealer_bj:
            # Croupier a un blackjack, gagne
            self.result = GameResult.DEALER_WIN
            self.hand_results[0] = GameResult.DEALER_WIN
            self.state = GameState.RESULT_SCREEN
        else:
            # Pas de blackjack, le joueur commence
            self.state = GameState.PLAYER_TURN
