"""Module de gestion du jeu de Blackjack.

Ce module contient la logique principale du jeu de Blackjack, incluant
les états du jeu, les actions possibles et la gestion des parties.
"""

from enum import Enum
from .deck import Deck
from .hand import Hand


class GameState(Enum):
    """Énumération des états possibles d'une partie de Blackjack.
    
    Attributes:
        MENU (str): Menu principal (Jouer / Paramètres / Statistiques)
        BETTING (str): Écran de mise (sélection place + jetons)
        SETTINGS (str): Écran des paramètres du jeu
        STATS (str): Écran des statistiques détaillées
        CLICKER (str): Écran du mini-jeu clicker pour gagner de l'argent
        INITIAL_DEAL (str): Distribution initiale (2 cartes chacun)
        PLAYER_TURN (str): Tour du joueur (choisir une action)
        DEALER_REVEAL (str): Révélation de la carte cachée du croupier
        DEALER_TURN (str): Tour du croupier (tire jusqu'à 17+)
        RESULT_SCREEN (str): Affichage du résultat de la partie
        GAME_OVER (str): Fin de partie
        WAITING_TO_CONTINUE (str): En attente de continuation
    """
    MENU = "menu"
    BETTING = "betting"
    SETTINGS = "settings"
    STATS = "stats"
    CLICKER = "clicker"
    INITIAL_DEAL = "initial_deal"
    PLAYER_TURN = "player_turn"
    DEALER_REVEAL = "dealer_reveal"
    DEALER_TURN = "dealer_turn"
    RESULT_SCREEN = "result_screen"
    GAME_OVER = "game_over"
    WAITING_TO_CONTINUE = "waiting"


class GameResult(Enum):
    """Énumération des résultats possibles d'une main de Blackjack.
    
    Attributes:
        PLAYER_WIN (str): Victoire du joueur
        DEALER_WIN (str): Victoire du croupier
        PUSH (str): Égalité (pas de gain ni de perte)
    """
    PLAYER_WIN = "player_win"
    DEALER_WIN = "dealer_win"
    PUSH = "push"


class PlayerAction(Enum):
    """Énumération des actions possibles du joueur.
    
    Attributes:
        HIT (str): Tirer une carte supplémentaire
        STAND (str): S'arrêter et garder sa main actuelle
        DOUBLE (str): Doubler la mise et tirer exactement 1 carte
        SPLIT (str): Diviser une paire en deux mains séparées
    """
    HIT = "hit"
    STAND = "stand"
    DOUBLE = "double"
    SPLIT = "split"


class Game:
    """Gère une partie complète de Blackjack.
    
    Cette classe orchestre tout le déroulement d'une partie de Blackjack,
    incluant la distribution des cartes, les actions des joueurs, les mises,
    le mode multi-places et les fonctionnalités avancées comme le split,
    le double down, l'assurance et l'abandon.
    
    Attributes:
        deck (Deck): Le sabot de cartes utilisé pour la partie
        hands (List[Hand]): Liste des mains du joueur (plusieurs si split)
        hand_bets (List[int]): Mises pour chaque main
        hand_results (List[GameResult]): Résultats pour chaque main
        current_hand_index (int): Index de la main actuellement jouée
        dealer_hand (Hand): Main du croupier
        state (GameState): État actuel du jeu
        result (GameResult): Résultat global de la partie
        frame_counter (float): Compteur pour les animations
        animation_delay (float): Délai entre les actions en secondes
        player_bet (int): Mise initiale du joueur
        seat_index (int): Place choisie par le joueur (0-4)
        insurance_bet (int): Montant de l'assurance
        has_insurance (bool): Indique si le joueur a pris l'assurance
        seat_bets (dict): Dictionnaire {seat_index: bet_amount}
        seat_hands (dict): Dictionnaire {seat_index: Hand}
        seat_results (dict): Dictionnaire {seat_index: GameResult}
        active_seats (List[int]): Liste des indices de places avec mises
        has_surrendered (bool): Indique si le joueur a abandonné
        
    Examples:
        >>> game = Game(num_decks=6)
        >>> game.state = GameState.BETTING
        >>> game.player_bet = 100
        >>> game.deal_initial_cards()
        >>> game.state
        <GameState.PLAYER_TURN: 'player_turn'>
    """
    
    def __init__(self, num_decks: int = 1):
        """Initialise une nouvelle partie de Blackjack.
        
        Args:
            num_decks (int, optional): Nombre de jeux de 52 cartes dans le sabot.
                Par défaut 1. Les casinos utilisent généralement 6 à 8 jeux.
        """
        self.deck = Deck(num_decks)
        
        # Système de mains multiples pour le split
        self.hands = [Hand()]
        self.hand_bets = [0]
        self.hand_results = [None]
        self.current_hand_index = 0
        
        self.dealer_hand = Hand()
        self.state = GameState.MENU
        self.result = None
        self.frame_counter = 0
        self.animation_delay = 0.5
        self.player_action = None
        self.player_bet = 0
        self.seat_index = 0
        self.last_action_time = 0
        
        # Assurance
        self.insurance_bet = 0
        self.has_insurance = False
        self.insurance_offered = False
        
        # Mode multi-places
        self.seat_bets = {}
        self.seat_hands = {}
        self.seat_results = {}
        self.active_seats = []
        self.current_seat_playing = 0
        self.current_seat_for_betting = 0
        
        # Abandon
        self.has_surrendered = False
    
    def reset(self) -> None:
        """Réinitialise l'état du jeu pour une nouvelle partie.
        
        Vide toutes les mains, réinitialise les mises et les résultats,
        mais conserve le sabot et la configuration.
        """
        self.hands = [Hand()]
        self.hand_bets = [0]
        self.hand_results = [None]
        self.current_hand_index = 0
        self.dealer_hand.clear()
        self.result = None
        self.frame_counter = 0
        self.player_action = None
        self.last_action_time = 0
        self.seat_hands = {}
        self.seat_results = {}
        self.active_seats = []
        self.current_seat_playing = 0
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
                return " Vous avez abandonné (50% retourné)"
            if self.result == GameResult.PLAYER_WIN:
                return " Vous avez gagné!"
            elif self.result == GameResult.DEALER_WIN:
                return " Le croupier a gagné"
            else:
                return "Égalité!"
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
    
    def _switch_to_next_seat(self) -> None:
        """Passe à la place suivante dans le jeu multi-places."""
        self.current_seat_playing += 1
        if self.current_seat_playing >= len(self.active_seats):
            # Toutes les places ont été jouées, le croupier joue
            self.state = GameState.DEALER_REVEAL
    
    def player_hit(self) -> None:
        """Le joueur tire une carte."""
        if not self.can_hit():
            return
        
        # Multi-seat: utiliser la place active actuelle
        if self.active_seats:
            seat_idx = self.active_seats[self.current_seat_playing]
            current_hand = self.seat_hands[seat_idx]
            current_hand.add_cards(self.deck.draw(1))
            self.last_action_time = self.frame_counter
            
            # Vérifier si la main a bust
            if current_hand.is_bust():
                self.seat_results[seat_idx] = GameResult.DEALER_WIN
                # Passer à la place suivante
                self._switch_to_next_seat()
        else:
            # Fallback pour le mode single-seat
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
        
        # Multi-seat: passer à la place suivante
        if self.active_seats:
            self._switch_to_next_seat()
        else:
            # Fallback pour le mode single-seat
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
        
        # Multi-seat: calculer le résultat pour chaque place active
        if self.active_seats:
            for seat_idx in self.active_seats:
                if self.seat_results[seat_idx] is not None:
                    # Résultat déjà déterminé (bust ou blackjack)
                    continue
                
                hand = self.seat_hands[seat_idx]
                player_value = hand.get_value()
                
                if dealer_bust:
                    self.seat_results[seat_idx] = GameResult.PLAYER_WIN
                elif player_value > dealer_value:
                    self.seat_results[seat_idx] = GameResult.PLAYER_WIN
                elif dealer_value > player_value:
                    self.seat_results[seat_idx] = GameResult.DEALER_WIN
                else:
                    self.seat_results[seat_idx] = GameResult.PUSH
            
            # Déterminer le résultat global
            wins = sum(1 for r in self.seat_results.values() if r == GameResult.PLAYER_WIN)
            losses = sum(1 for r in self.seat_results.values() if r == GameResult.DEALER_WIN)
            if wins > losses:
                self.result = GameResult.PLAYER_WIN
            elif losses > wins:
                self.result = GameResult.DEALER_WIN
            else:
                self.result = GameResult.PUSH
        elif len(self.hands) > 1:
            # Mode split (fallback)
            for i, hand in enumerate(self.hands):
                if self.hand_results[i] is not None:
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
            wins = sum(1 for r in self.hand_results if r == GameResult.PLAYER_WIN)
            losses = sum(1 for r in self.hand_results if r == GameResult.DEALER_WIN)
            if wins > losses:
                self.result = GameResult.PLAYER_WIN
            elif losses > wins:
                self.result = GameResult.DEALER_WIN
            else:
                self.result = GameResult.PUSH
        else:
            # Une seule main (fallback)
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

    def deal_initial_cards_multiseat(self) -> None:
        """Distribue les 2 cartes initiales à toutes les places actives et au croupier."""
        # Identifier les places actives (celles avec des mises)
        self.active_seats = sorted([seat for seat, bet in self.seat_bets.items() if bet > 0])
        
        if not self.active_seats:
            return
        
        # Initialiser les mains pour chaque place active
        for seat_idx in self.active_seats:
            self.seat_hands[seat_idx] = Hand()
            self.seat_results[seat_idx] = None
        
        # Distribution alternée: 1 carte à chaque place, puis 1 au croupier, puis 2ème carte à chaque place, puis 2ème au croupier
        for seat_idx in self.active_seats:
            self.seat_hands[seat_idx].add_cards(self.deck.draw(1))
        
        self.dealer_hand.add_cards(self.deck.draw(1))
        
        for seat_idx in self.active_seats:
            self.seat_hands[seat_idx].add_cards(self.deck.draw(1))
        
        self.dealer_hand.add_cards(self.deck.draw(1))
        
        # Vérifier les blackjacks
        dealer_bj = self.dealer_hand.is_blackjack()
        
        # Vérifier chaque place pour les blackjacks
        all_done = True
        for seat_idx in self.active_seats:
            player_bj = self.seat_hands[seat_idx].is_blackjack()
            
            if player_bj and dealer_bj:
                self.seat_results[seat_idx] = GameResult.PUSH
            elif player_bj:
                self.seat_results[seat_idx] = GameResult.PLAYER_WIN
            elif dealer_bj:
                self.seat_results[seat_idx] = GameResult.DEALER_WIN
            else:
                all_done = False
        
        # Si tous ont des blackjacks ou le croupier a un blackjack, terminer
        if dealer_bj or all_done:
            self.state = GameState.RESULT_SCREEN
        else:
            # Commencer à jouer la première place
            self.current_seat_playing = 0
            self.state = GameState.PLAYER_TURN
