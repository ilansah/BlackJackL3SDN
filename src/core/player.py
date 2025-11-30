import json
import os
from pathlib import Path


class Player:
    """gere les statistiques et le profil du joueur"""
    
    def __init__(self, name: str = "Player"):
        self.name = name
        self.wins = 0
        self.losses = 0
        self.pushes = 0
        self.blackjacks = 0
        self.total_hands = 0
        self.total_money_won = 0
        self.total_money_lost = 0
        
        # Nouvelles statistiques
        self.surrenders = 0
        self.insurances_taken = 0
        self.insurances_won = 0
        self.splits_made = 0
    
    def win_hand(self, amount: int = 100) -> None:
        """enregistre une main gagnee."""
        self.wins += 1
        self.total_hands += 1
        self.total_money_won += amount
    
    def lose_hand(self, amount: int = 100) -> None:
        """Enregistre une main perdue."""
        self.losses += 1
        self.total_hands += 1
        self.total_money_lost += amount
    
    def push_hand(self) -> None:
        """Enregistre une égalité."""
        self.pushes += 1
        self.total_hands += 1
    
    def record_blackjack(self) -> None:
        """Enregistre un blackjack."""
        self.blackjacks += 1
    
    def get_win_rate(self) -> float:
        """Retourne le pourcentage de victoires."""
        if self.total_hands == 0:
            return 0.0
        return (self.wins / self.total_hands) * 100
    
    def get_net_profit(self) -> int:
        """Retourne le bénéfice net (gagne - perdu)."""
        return self.total_money_won - self.total_money_lost
    
    def to_dict(self) -> dict:
        """Convertit le profil en dictionnaire."""
        return {
            "name": self.name,
            "wins": self.wins,
            "losses": self.losses,
            "pushes": self.pushes,
            "blackjacks": self.blackjacks,
            "total_hands": self.total_hands,
            "total_money_won": self.total_money_won,
            "total_money_lost": self.total_money_lost,
            "surrenders": self.surrenders,
            "insurances_taken": self.insurances_taken,
            "insurances_won": self.insurances_won,
            "splits_made": self.splits_made,
        }
    
    @staticmethod
    def from_dict(data: dict) -> "Player":
        """Crée un Player depuis un dictionnaire."""
        player = Player(data.get("name", "Player"))
        player.wins = data.get("wins", 0)
        player.losses = data.get("losses", 0)
        player.pushes = data.get("pushes", 0)
        player.blackjacks = data.get("blackjacks", 0)
        player.total_hands = data.get("total_hands", 0)
        player.total_money_won = data.get("total_money_won", 0)
        player.total_money_lost = data.get("total_money_lost", 0)
        player.surrenders = data.get("surrenders", 0)
        player.insurances_taken = data.get("insurances_taken", 0)
        player.insurances_won = data.get("insurances_won", 0)
        player.splits_made = data.get("splits_made", 0)
        return player
    
    def save(self, filepath: str = "player_stats.json") -> None:
        """Sauvegarde les statistiques dans un fichier JSON."""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @staticmethod
    def load(filepath: str = "player_stats.json") -> "Player":
        """Charge les statistiques depuis un fichier JSON."""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)
                return Player.from_dict(data)
        return Player()
