# core/game.py

from enum import Enum
from .deck import Deck
from .hand import Hand


class GameState(Enum):
    """États possibles d'une partie."""
    MENU = "menu"                      # Menu principal
    INITIAL_DEAL = "initial_deal"      # Distribution initiale (2 cartes chacun)
    PLAYER_TURN = "player_turn"        # Tour du joueur (choisir action)
    DEALER_REVEAL = "dealer_reveal"    # Révéler la carte cachée du croupier
    DEALER_TURN = "dealer_turn"        # Tour du croupier (règle fixe: hit <=16, stand >=17)
    RESULT_SCREEN = "result_screen"    # Afficher le résultat
    GAME_OVER = "game_over"            # Partie terminée
    WAITING_TO_CONTINUE = "waiting"    # Attente avant la prochaine partie


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
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.state = GameState.MENU
        self.result = None
        self.frame_counter = 0
        self.animation_delay = 0.5  # Délai entre les actions (secondes)
        self.player_action = None  # Action en attente du joueur
        self.player_bet = 0  # Mise du joueur
        self.split_hand = None  # Main secondaire si split
        self.current_hand_index = 0  # 0 = main principale, 1 = split
        self.last_action_time = 0  # Timestamp de la dernière action
    
    def reset(self) -> None:
        """Réinitialise pour une nouvelle partie."""
        self.player_hand.clear()
        self.dealer_hand.clear()
        self.state = GameState.INITIAL_DEAL
        self.result = None
        self.frame_counter = 0
        self.player_action = None
        self.split_hand = None
        self.current_hand_index = 0
        self.last_action_time = 0
    
    def can_hit(self) -> bool:
        """Retourne True si le joueur peut tirer."""
        return self.state == GameState.PLAYER_TURN
    
    def can_stand(self) -> bool:
        """Retourne True si le joueur peut s'arrêter."""
        return self.state == GameState.PLAYER_TURN
    
    def can_double(self) -> bool:
        """Retourne True si le joueur peut doubler (seulement avec 2 cartes initiales)."""
        return self.state == GameState.PLAYER_TURN and len(self.player_hand.cards) == 2
    
    def can_split(self) -> bool:
        """Retourne True si le joueur peut splitter (2 cartes de même valeur, pas encore de split)."""
        if self.state != GameState.PLAYER_TURN or self.split_hand is not None:
            return False
        if len(self.player_hand.cards) != 2:
            return False
        # Vérifier que les deux cartes ont la même valeur
        return self.player_hand.cards[0].value() == self.player_hand.cards[1].value()
    
    def get_status_message(self) -> str:
        """Retourne un message décrivant l'état actuel."""
        if self.state == GameState.MENU:
            return "BLACKJACK"
        elif self.state == GameState.INITIAL_DEAL:
            return "Distribution des cartes..."
        elif self.state == GameState.PLAYER_TURN:
            return f"À vous de jouer (main={self.player_hand.get_value()})"
        elif self.state == GameState.DEALER_REVEAL:
            return "Révélation du croupier..."
        elif self.state == GameState.DEALER_TURN:
            return f"Le croupier joue (votre main={self.player_hand.get_value()})"
        elif self.state == GameState.RESULT_SCREEN:
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
    
    def player_hit(self) -> None:
        """Le joueur tire une carte."""
        if not self.can_hit():
            return
        self.player_hand.add_cards(self.deck.draw(1))
        self.last_action_time = self.frame_counter
        
        if self.player_hand.is_bust():
            self.result = GameResult.DEALER_WIN
            self.state = GameState.RESULT_SCREEN
    
    def player_stand(self) -> None:
        """Le joueur s'arrête et le croupier joue."""
        if not self.can_stand():
            return
        self.state = GameState.DEALER_REVEAL
        self.last_action_time = self.frame_counter
    
    def player_double(self) -> None:
        """Le joueur double sa mise et tire 1 carte."""
        if not self.can_double():
            return
        self.player_bet *= 2
        self.player_hand.add_cards(self.deck.draw(1))
        self.last_action_time = self.frame_counter
        
        if self.player_hand.is_bust():
            self.result = GameResult.DEALER_WIN
            self.state = GameState.RESULT_SCREEN
        else:
            # Après un double, le joueur s'arrête automatiquement
            self.state = GameState.DEALER_REVEAL
    
    def player_split(self) -> None:
        """Le joueur divise sa main (si possible)."""
        if not self.can_split():
            return
        
        # Créer une deuxième main avec la deuxième carte
        self.split_hand = Hand()
        self.split_hand.add_cards([self.player_hand.cards.pop()])
        
        # Donner une nouvelle carte à chaque main
        self.player_hand.add_cards(self.deck.draw(1))
        self.split_hand.add_cards(self.deck.draw(1))
        
        # Jouer la première main
        self.current_hand_index = 0
        self.last_action_time = self.frame_counter
    
    def dealer_play(self) -> None:
        """Le croupier joue selon la règle fixe : tire si < 17, s'arrête sinon."""
        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_cards(self.deck.draw(1))
        
        # Comparer et déterminer le gagnant
        self._determine_winner()
    
    def _determine_winner(self) -> None:
        """Compare les mains et détermine le gagnant."""
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()
        
        # Si le dealer a bust, joueur gagne
        if dealer_value > 21:
            self.result = GameResult.PLAYER_WIN
        # Si le joueur a bust, dealer gagne
        elif player_value > 21:
            self.result = GameResult.DEALER_WIN
        # Sinon comparer les valeurs
        elif player_value > dealer_value:
            self.result = GameResult.PLAYER_WIN
        elif dealer_value > player_value:
            self.result = GameResult.DEALER_WIN
        else:
            self.result = GameResult.PUSH
        
        self.state = GameState.RESULT_SCREEN
    
    def deal_initial_cards(self) -> None:
        """Distribue les 2 cartes initiales au joueur et au croupier."""
        # Donner 1 carte au joueur, 1 au croupier, puis 1 au joueur, 1 au croupier
        self.player_hand.add_cards(self.deck.draw(1))
        self.dealer_hand.add_cards(self.deck.draw(1))
        self.player_hand.add_cards(self.deck.draw(1))
        self.dealer_hand.add_cards(self.deck.draw(1))
        
        # Vérifier les blackjacks initiaux
        player_bj = self.player_hand.is_blackjack()
        dealer_bj = self.dealer_hand.is_blackjack()
        
        if player_bj and dealer_bj:
            # Les deux ont un blackjack = égalité
            self.result = GameResult.PUSH
            self.state = GameState.RESULT_SCREEN
        elif player_bj:
            # Joueur a un blackjack, gagne
            self.result = GameResult.PLAYER_WIN
            self.state = GameState.RESULT_SCREEN
        elif dealer_bj:
            # Croupier a un blackjack, gagne
            self.result = GameResult.DEALER_WIN
            self.state = GameState.RESULT_SCREEN
        else:
            # Pas de blackjack, le joueur commence
            self.state = GameState.PLAYER_TURN
