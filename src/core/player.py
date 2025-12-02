import json
import os
from pathlib import Path

# chemin pour eviter les erreurs de fichier non trouve
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
STATS_FILE = os.path.join(BASE_DIR, "player_stats.json")

class Player:
    # gere les statistiques et le profil du joueur
    
    def __init__(self, name: str = "Player"):
        self.name = name
        self.balance = 1000 # solde du joueur ajoute pour fixer l erreur
        self.wins = 0
        self.losses = 0
        self.pushes = 0
        self.blackjacks = 0
        self.total_hands = 0
        self.total_money_won = 0
        self.total_money_lost = 0
        
        # nouvelles statistiques
        self.surrenders = 0
        self.insurances_taken = 0
        self.insurances_won = 0
        self.splits_made = 0
    
    def win_hand(self, amount: int = 100) -> None:
        # enregistre une main gagnee et met a jour le solde
        self.wins += 1
        self.total_hands += 1
        self.total_money_won += amount
        self.balance += amount # ajout du gain au solde
    
    def lose_hand(self, amount: int = 100) -> None:
        # enregistre une main perdue et met a jour le solde
        self.losses += 1
        self.total_hands += 1
        self.total_money_lost += amount
        self.balance -= amount # retrait de la perte du solde
    
    def push_hand(self) -> None:
        # enregistre une egalite
        self.pushes += 1
        self.total_hands += 1
    
    def record_blackjack(self) -> None:
        # enregistre un blackjack
        self.blackjacks += 1
    
    def get_win_rate(self) -> float:
        # retourne le pourcentage de victoires
        if self.total_hands == 0:
            return 0.0
        return (self.wins / self.total_hands) * 100
    
    def get_net_profit(self) -> int:
        # retourne le benefice net gagne moins perdu
        return self.total_money_won - self.total_money_lost
    
    def to_dict(self) -> dict:
        # convertit le profil en dictionnaire pour la sauvegarde
        return {
            "name": self.name,
            "balance": self.balance, # on sauvegarde le solde
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
        # cree un player depuis un dictionnaire charge
        player = Player(data.get("name", "Player"))
        
        # recuperation des sous
        player.total_money_won = data.get("total_money_won", 0)
        player.total_money_lost = data.get("total_money_lost", 0)
        
        # calcul intelligent du solde si absent dans le fichier de sauvegarde
        if "balance" in data:
            player.balance = data["balance"]
        else:
            # si pas de solde on le recalcule base 1000 plus gains moins pertes
            player.balance = 1000 + player.total_money_won - player.total_money_lost
            
        player.wins = data.get("wins", 0)
        player.losses = data.get("losses", 0)
        player.pushes = data.get("pushes", 0)
        player.blackjacks = data.get("blackjacks", 0)
        player.total_hands = data.get("total_hands", 0)
        player.surrenders = data.get("surrenders", 0)
        player.insurances_taken = data.get("insurances_taken", 0)
        player.insurances_won = data.get("insurances_won", 0)
        player.splits_made = data.get("splits_made", 0)
        return player
    
    def save(self, filepath: str = None) -> None:
        # sauvegarde les statistiques dans un fichier json
        if filepath is None:
            filepath = STATS_FILE
            
        try:
            with open(filepath, 'w') as f:
                json.dump(self.to_dict(), f, indent=2)
        except Exception:
            pass
    
    @staticmethod
    def load(filepath: str = None) -> "Player":
        # charge les statistiques depuis un fichier json
        if filepath is None:
            filepath = STATS_FILE
            
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    return Player.from_dict(data)
            except Exception:
                pass
        return Player()