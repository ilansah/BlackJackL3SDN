import json
import os
from pathlib import Path
from typing import Any, Dict


class ConfigManager:
    # gere les parametres de l application
    
    # chemins
    CONFIG_DIR = "config"
    CONFIG_FILE = os.path.join(CONFIG_DIR, "settings.json")
    
    # configuration par defaut style vip
    DEFAULT_CONFIG = {
        "game": {
            "width": 1280,
            "height": 720,
            "fps": 60,
            "num_decks": 1,
            "animation_delay": 0.5
        },
        "cards": {
            "width": 100,
            "height": 145,
            "spacing": 20
        },
        "colors": {
            "bg": [20, 20, 25],
            "bg_dark": [0, 70, 80],
            "menu_bg": [20, 20, 25],
            "text": [240, 240, 240],
            "text_gold": [212, 175, 55],
            "win": [50, 205, 50],
            "lose": [220, 60, 60],
            "push": [255, 165, 0]
        },
        "timing": {
            "initial_deal_duration": 1.0,
            "dealer_reveal_duration": 1.0,
            "result_screen_duration": 3.0,
            "action_delay": 0.5
        },
        "difficulty": {
            "dealer_strategy": "standard"
        },
        "player": {
            "starting_balance": 1000,
            "min_bet": 5,
            "max_bet": 1000
        },
        "features": {
            "sound_enabled": False,
            "animations_enabled": True,
            "show_hints": True
        }
    }
    
    def __init__(self):
        # initialise le gestionnaire de configuration
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        # charge la configuration depuis le fichier json
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"erreur lors du chargement de la config {e}")
                return self.DEFAULT_CONFIG.copy()
        
        # creer la config par defaut si elle n existe pas
        self._save_config(self.DEFAULT_CONFIG)
        return self.DEFAULT_CONFIG.copy()
    
    def _save_config(self, config: Dict[str, Any]) -> None:
        # sauvegarde la configuration dans le fichier json
        os.makedirs(self.CONFIG_DIR, exist_ok=True)
        try:
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"erreur lors de la sauvegarde de la config {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        # recupere une valeur de configuration
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        # definit une valeur de configuration
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self._save_config(self.config)
    
    def get_all(self) -> Dict[str, Any]:
        # retourne toute la configuration
        return self.config.copy()
    
    def reset_to_default(self) -> None:
        # reinitialise la configuration par defaut
        self.config = self.DEFAULT_CONFIG.copy()
        self._save_config(self.config)
    
    def get_game_settings(self) -> Dict[str, Any]:
        # retourne les parametres du jeu
        return self.config.get("game", {})
    
    def get_card_settings(self) -> Dict[str, Any]:
        # retourne les parametres des cartes
        return self.config.get("cards", {})
    
    def get_color_settings(self) -> Dict[str, Any]:
        # retourne les parametres des couleurs
        return self.config.get("colors", {})
    
    def get_timing_settings(self) -> Dict[str, Any]:
        # retourne les parametres de timing
        return self.config.get("timing", {})
    
    def get_player_settings(self) -> Dict[str, Any]:
        # retourne les parametres du joueur
        return self.config.get("player", {})
    
    def get_features(self) -> Dict[str, Any]:
        # retourne les parametres de fonctionnalites
        return self.config.get("features", {})
    
    def set_game_settings(self, settings: Dict[str, Any]) -> None:
        # definit les parametres du jeu
        self.config["game"].update(settings)
        self._save_config(self.config)
    
    def toggle_feature(self, feature: str) -> bool:
        # bascule l etat d une fonctionnalite
        features = self.config.get("features", {})
        current_state = features.get(feature, False)
        new_state = not current_state
        features[feature] = new_state
        self.config["features"] = features
        self._save_config(self.config)
        return new_state
    
    def print_config(self) -> None:
        # affiche la configuration dans la console
        print(json.dumps(self.config, indent=2))


# instance globale
_config_manager = None


def get_config_manager() -> ConfigManager:
    # retourne l instance globale du gestionnaire de configuration
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager