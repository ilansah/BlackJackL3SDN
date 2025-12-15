"""Module de gestion du joueur et de ses statistiques.

Ce module définit la classe Player qui gère le profil du joueur,
son solde, ses statistiques de jeu et la persistance des données.
"""

import json
import os
from typing import Optional


class Player:
    """Représente un joueur de Blackjack avec ses statistiques et son solde.
    
    Cette classe gère toutes les informations relatives au joueur :
    son solde, ses statistiques de jeu (victoires, défaites, etc.),
    et la sauvegarde/chargement de ces données.
    
    Attributes:
        balance (int): Solde actuel du joueur en dollars
        total_hands (int): Nombre total de mains jouées
        wins (int): Nombre de victoires
        losses (int): Nombre de défaites
        pushes (int): Nombre d'égalités
        blackjacks (int): Nombre de Blackjacks obtenus
        total_wagered (int): Montant total misé
        total_won (int): Montant total gagné
        initial_balance (int): Solde de départ du joueur
        
    Examples:
        >>> player = Player(balance=1000)
        >>> player.win_hand(100)
        >>> player.balance
        1100
        >>> player.wins
        1
    """
    
    #: Nom du fichier de sauvegarde des statistiques
    SAVE_FILE = "player_stats.json"
    
    def __init__(self, balance: int = 1000):
        """Initialise un nouveau joueur.
        
        Args:
            balance (int, optional): Solde initial du joueur. Par défaut 1000.
        """
        self.balance = balance
        self.total_hands = 0
        self.wins = 0
        self.losses = 0
        self.pushes = 0
        self.blackjacks = 0
        self.total_wagered = 0
        self.total_won = 0
        self.initial_balance = balance
    
    def win_hand(self, amount: int) -> None:
        """Enregistre une victoire et met à jour le solde.
        
        Args:
            amount (int): Montant gagné (inclut la mise initiale + gains)
        """
        self.wins += 1
        self.total_hands += 1
        self.balance += amount
        self.total_won += amount
    
    def lose_hand(self, amount: int) -> None:
        """Enregistre une défaite et met à jour le solde.
        
        Args:
            amount (int): Montant perdu (mise)
        """
        self.losses += 1
        self.total_hands += 1
        self.balance -= amount
        self.total_wagered += amount
    
    def push_hand(self) -> None:
        """Enregistre une égalité (push).
        
        En cas de push, le joueur récupère sa mise sans gain ni perte.
        """
        self.pushes += 1
        self.total_hands += 1
    
    def record_blackjack(self) -> None:
        """Enregistre qu'un Blackjack naturel a été obtenu."""
        self.blackjacks += 1
    
    def earn_money(self, amount: int) -> None:
        """Ajoute de l'argent au solde du joueur (pour le clicker).
        
        Args:
            amount (int): Montant à ajouter au solde
        """
        self.balance += amount
    
    def get_net_profit(self) -> int:
        """Calcule le profit net du joueur depuis le début.
        
        Returns:
            int: Profit net (peut être négatif en cas de pertes)
            
        Examples:
            >>> player = Player(balance=1000)
            >>> player.balance = 1500
            >>> player.get_net_profit()
            500
        """
        return self.balance - self.initial_balance
    
    def get_win_rate(self) -> float:
        """Calcule le taux de victoire du joueur.
        
        Returns:
            float: Taux de victoire en pourcentage (0-100)
            
        Examples:
            >>> player = Player()
            >>> player.wins = 7
            >>> player.total_hands = 10
            >>> player.get_win_rate()
            70.0
        """
        if self.total_hands == 0:
            return 0.0
        return (self.wins / self.total_hands) * 100
    
    def to_dict(self) -> dict:
        """Convertit le joueur en dictionnaire pour la sauvegarde.
        
        Returns:
            dict: Dictionnaire contenant toutes les données du joueur
        """
        return {
            "balance": self.balance,
            "total_hands": self.total_hands,
            "wins": self.wins,
            "losses": self.losses,
            "pushes": self.pushes,
            "blackjacks": self.blackjacks,
            "total_wagered": self.total_wagered,
            "total_won": self.total_won,
            "initial_balance": self.initial_balance
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        """Crée un joueur à partir d'un dictionnaire.
        
        Args:
            data (dict): Dictionnaire contenant les données du joueur
            
        Returns:
            Player: Instance de Player restaurée depuis le dictionnaire
        """
        player = cls(balance=data.get("balance", 1000))
        player.total_hands = data.get("total_hands", 0)
        player.wins = data.get("wins", 0)
        player.losses = data.get("losses", 0)
        player.pushes = data.get("pushes", 0)
        player.blackjacks = data.get("blackjacks", 0)
        player.total_wagered = data.get("total_wagered", 0)
        player.total_won = data.get("total_won", 0)
        player.initial_balance = data.get("initial_balance", 1000)
        return player
    
    def save(self, filepath: Optional[str] = None) -> None:
        """Sauvegarde les données du joueur dans un fichier JSON.
        
        Args:
            filepath (str, optional): Chemin du fichier de sauvegarde.
                Si None, utilise le chemin par défaut.
                
        Examples:
            >>> player = Player()
            >>> player.save()  # Sauvegarde dans player_stats.json
        """
        if filepath is None:
            # Sauvegarder dans le répertoire parent de src
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            filepath = os.path.join(base_dir, "..", self.SAVE_FILE)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
    
    @classmethod
    def load(cls, filepath: Optional[str] = None) -> "Player":
        """Charge les données du joueur depuis un fichier JSON.
        
        Args:
            filepath (str, optional): Chemin du fichier de sauvegarde.
                Si None, utilise le chemin par défaut.
            
        Returns:
            Player: Instance de Player chargée ou nouvelle instance 
                si le fichier n'existe pas
                
        Examples:
            >>> player = Player.load()
            >>> print(player.balance)
            1000
        """
        if filepath is None:
            # Chercher dans le répertoire parent de src
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            filepath = os.path.join(base_dir, "..", cls.SAVE_FILE)
        
        if not os.path.exists(filepath):
            print(f"Fichier de sauvegarde non trouvé, création d'un nouveau joueur")
            return cls()
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return cls.from_dict(data)
        except Exception as e:
            print(f"Erreur lors du chargement: {e}, création d'un nouveau joueur")
            return cls()
    
    def reset_stats(self) -> None:
        """Réinitialise toutes les statistiques mais garde le solde actuel."""
        self.total_hands = 0
        self.wins = 0
        self.losses = 0
        self.pushes = 0
        self.blackjacks = 0
        self.total_wagered = 0
        self.total_won = 0
    
    def __repr__(self) -> str:
        """Retourne une représentation textuelle du joueur.
        
        Returns:
            str: Représentation du joueur avec solde et statistiques
        """
        return f"Player(balance=${self.balance}, hands={self.total_hands}, wins={self.wins})"
