#!/usr/bin/env python3
"""
Script pour appliquer les modifications nécessaires au jeu Blackjack:
1. Support des mains multiples (plusieurs sièges)
2. Musique de fond avec contrôle dans les paramètres
"""

import os
import json

# Chemin de base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
CORE_DIR = os.path.join(SRC_DIR, "core")
CONFIG_DIR = os.path.join(BASE_DIR, "config")

def update_settings_json():
    """Ajoute les paramètres de musique au fichier settings.json"""
    settings_path = os.path.join(CONFIG_DIR, "settings.json")
    
    with open(settings_path, 'r') as f:
        settings = json.load(f)
    
    # Ajouter les paramètres de musique
    if "features" in settings:
        settings["features"]["music_enabled"] = True
        settings["features"]["music_volume"] = 0.5
    
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)
    
    print("✓ settings.json mis à jour")

def update_hand_py():
    """Ajoute seat_index à la classe Hand"""
    hand_path = os.path.join(CORE_DIR, "hand.py")
    
    with open(hand_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remplacer __init__
    old_init = "    def __init__(self):\n        self.cards: List[Card] = []"
    new_init = "    def __init__(self, seat_index: int = 0):\n        self.cards: List[Card] = []\n        self.seat_index = seat_index"
    
    content = content.replace(old_init, new_init)
    
    with open(hand_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ hand.py mis à jour")

if __name__ == "__main__":
    print("Application des modifications...")
    update_settings_json()
    update_hand_py()
    print("\n✅ Toutes les modifications ont été appliquées avec succès!")
