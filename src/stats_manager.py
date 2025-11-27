"""
Gestionnaire de statistiques avancées pour le Blackjack.
Permet d'enregistrer, analyser et exporter les stats du joueur.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any


class StatsManager:
    """Gère les statistiques détaillées du joueur."""
    
    STATS_FILE = "player_stats.json"
    HISTORY_FILE = "player_history.json"
    
    @staticmethod
    def load_stats() -> Dict[str, Any]:
        """Charge les statistiques du fichier JSON."""
        if os.path.exists(StatsManager.STATS_FILE):
            try:
                with open(StatsManager.STATS_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erreur lors du chargement des stats: {e}")
                return StatsManager.get_default_stats()
        return StatsManager.get_default_stats()
    
    @staticmethod
    def get_default_stats() -> Dict[str, Any]:
        """Retourne les statistiques par défaut."""
        return {
            "name": "Player",
            "wins": 0,
            "losses": 0,
            "pushes": 0,
            "blackjacks": 0,
            "total_hands": 0,
            "total_money_won": 0,
            "total_money_lost": 0,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
    
    @staticmethod
    def save_stats(stats: Dict[str, Any]) -> None:
        """Sauvegarde les statistiques dans le fichier JSON."""
        stats["updated_at"] = datetime.now().isoformat()
        try:
            with open(StatsManager.STATS_FILE, 'w') as f:
                json.dump(stats, f, indent=2)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des stats: {e}")
    
    @staticmethod
    def load_history() -> List[Dict[str, Any]]:
        """Charge l'historique des mains jouées."""
        if os.path.exists(StatsManager.HISTORY_FILE):
            try:
                with open(StatsManager.HISTORY_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erreur lors du chargement de l'historique: {e}")
                return []
        return []
    
    @staticmethod
    def add_to_history(hand_data: Dict[str, Any]) -> None:
        """Ajoute une main à l'historique."""
        history = StatsManager.load_history()
        hand_data["timestamp"] = datetime.now().isoformat()
        history.append(hand_data)
        
        # Garder seulement les 1000 dernières mains
        if len(history) > 1000:
            history = history[-1000:]
        
        try:
            with open(StatsManager.HISTORY_FILE, 'w') as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de l'historique: {e}")
    
    @staticmethod
    def get_stats_summary(stats: Dict[str, Any]) -> Dict[str, Any]:
        """Calcule les statistiques récapitulatives."""
        total_hands = stats.get("total_hands", 0)
        wins = stats.get("wins", 0)
        losses = stats.get("losses", 0)
        pushes = stats.get("pushes", 0)
        money_won = stats.get("total_money_won", 0)
        money_lost = stats.get("total_money_lost", 0)
        blackjacks = stats.get("blackjacks", 0)
        
        win_rate = (wins / total_hands * 100) if total_hands > 0 else 0.0
        loss_rate = (losses / total_hands * 100) if total_hands > 0 else 0.0
        push_rate = (pushes / total_hands * 100) if total_hands > 0 else 0.0
        net_profit = money_won - money_lost
        avg_per_hand = (net_profit // total_hands) if total_hands > 0 else 0
        w_l_ratio = (wins / losses) if losses > 0 else 0
        
        return {
            "total_hands": total_hands,
            "wins": wins,
            "losses": losses,
            "pushes": pushes,
            "blackjacks": blackjacks,
            "win_rate": round(win_rate, 2),
            "loss_rate": round(loss_rate, 2),
            "push_rate": round(push_rate, 2),
            "total_money_won": money_won,
            "total_money_lost": money_lost,
            "net_profit": net_profit,
            "avg_per_hand": avg_per_hand,
            "w_l_ratio": round(w_l_ratio, 2)
        }
    
    @staticmethod
    def export_stats(filename: str = "blackjack_stats_export.json") -> bool:
        """Exporte les statistiques dans un fichier."""
        stats = StatsManager.load_stats()
        summary = StatsManager.get_stats_summary(stats)
        
        export_data = {
            "player_name": stats.get("name"),
            "exported_at": datetime.now().isoformat(),
            "stats": stats,
            "summary": summary
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            print(f"Statistiques exportées vers: {filename}")
            return True
        except Exception as e:
            print(f"Erreur lors de l'export: {e}")
            return False
    
    @staticmethod
    def reset_stats() -> None:
        """Réinitialise les statistiques."""
        default_stats = StatsManager.get_default_stats()
        StatsManager.save_stats(default_stats)
        
        # Effacer l'historique aussi
        try:
            if os.path.exists(StatsManager.HISTORY_FILE):
                os.remove(StatsManager.HISTORY_FILE)
        except Exception as e:
            print(f"Erreur lors de la suppression de l'historique: {e}")
    
    @staticmethod
    def get_session_stats(history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calcule les stats pour la session actuelle (dernières N mains)."""
        if not history:
            return {}
        
        session_wins = sum(1 for h in history if h.get("result") == "win")
        session_losses = sum(1 for h in history if h.get("result") == "loss")
        session_pushes = sum(1 for h in history if h.get("result") == "push")
        session_money = sum(h.get("amount", 0) for h in history)
        
        return {
            "hands": len(history),
            "wins": session_wins,
            "losses": session_losses,
            "pushes": session_pushes,
            "total_money": session_money,
            "win_rate": (session_wins / len(history) * 100) if history else 0
        }
