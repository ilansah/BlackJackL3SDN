# core/player.py

import json
import os
from typing import Optional


class Player:
    """Représente un joueur de Blackjack avec ses statistiques et son solde"""
    
    SAVE_FILE = "player_stats.json"
    
    def __init__(self, balance: int = 1000):
        """
        Initialise un nouveau joueur
        
        Args:
            balance: Solde initial du joueur (par défaut 1000)
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
    
    def win_hand(self, amount: int):
        """
        Enregistre une victoire et met à jour le solde
        
        Args:
            amount: Montant gagné
        """
        self.wins += 1
        self.total_hands += 1
        self.balance += amount
        self.total_won += amount
    
    def lose_hand(self, amount: int):
        """
        Enregistre une défaite et met à jour le solde
        
        Args:
            amount: Montant perdu
        """
        self.losses += 1
        self.total_hands += 1
        self.balance -= amount
        self.total_wagered += amount
    
    def push_hand(self):
        """Enregistre une égalité (push)"""
        self.pushes += 1
        self.total_hands += 1
    
    def record_blackjack(self):
        """Enregistre un blackjack"""
        self.blackjacks += 1
    
    def get_net_profit(self) -> int:
        """
        Calcule le profit net du joueur
        
        Returns:
            Profit net (peut être négatif)
        """
        return self.balance - self.initial_balance
    
    def get_win_rate(self) -> float:
        """
        Calcule le taux de victoire
        
        Returns:
            Taux de victoire en pourcentage (0-100)
        """
        if self.total_hands == 0:
            return 0.0
        return (self.wins / self.total_hands) * 100
    
    def to_dict(self) -> dict:
        """
        Convertit le joueur en dictionnaire pour la sauvegarde
        
        Returns:
            Dictionnaire contenant toutes les données du joueur
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
        """
        Crée un joueur à partir d'un dictionnaire
        
        Args:
            data: Dictionnaire contenant les données du joueur
            
        Returns:
            Instance de Player
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
    
    def save(self, filepath: Optional[str] = None):
        """
        Sauvegarde les données du joueur dans un fichier JSON
        
        Args:
            filepath: Chemin du fichier de sauvegarde (optionnel)
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
        """
        Charge les données du joueur depuis un fichier JSON
        
        Args:
            filepath: Chemin du fichier de sauvegarde (optionnel)
            
        Returns:
            Instance de Player chargée ou nouvelle instance si le fichier n'existe pas
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
    
    def reset_stats(self):
        """Réinitialise toutes les statistiques mais garde le solde"""
        self.total_hands = 0
        self.wins = 0
        self.losses = 0
        self.pushes = 0
        self.blackjacks = 0
        self.total_wagered = 0
        self.total_won = 0
    
    def __repr__(self) -> str:
        return f"Player(balance=${self.balance}, hands={self.total_hands}, wins={self.wins})"
