#!/usr/bin/env python3
"""
Script pour réinitialiser toutes les statistiques du jeu à 0.
"""

import os
import sys

# Ajouter le répertoire src au path pour importer les modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from stats_manager import StatsManager


def main():
    """Réinitialise toutes les statistiques."""
    print("🔄 Réinitialisation de toutes les statistiques...")
    
    # Réinitialiser les stats
    StatsManager.reset_stats()
    
    print("✅ Statistiques réinitialisées avec succès!")
    print("\nStatistiques actuelles:")
    
    # Afficher les stats par défaut
    stats = StatsManager.load_stats()
    print(f"  - Nom: {stats['name']}")
    print(f"  - Victoires: {stats['wins']}")
    print(f"  - Défaites: {stats['losses']}")
    print(f"  - Égalités: {stats['pushes']}")
    print(f"  - Blackjacks: {stats['blackjacks']}")
    print(f"  - Total mains: {stats['total_hands']}")
    print(f"  - Argent gagné: {stats['total_money_won']}")
    print(f"  - Argent perdu: {stats['total_money_lost']}")
    
    # Vérifier si les fichiers de stats existent
    if os.path.exists(StatsManager.STATS_FILE):
        print(f"\n📁 Fichier de stats: {StatsManager.STATS_FILE}")
    if os.path.exists(StatsManager.HISTORY_FILE):
        print(f"📁 Fichier d'historique: {StatsManager.HISTORY_FILE} (supprimé)")
    else:
        print(f"📁 Fichier d'historique: aucun")


if __name__ == "__main__":
    main()
