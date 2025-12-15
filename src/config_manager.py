"""Module de gestion de la configuration de l'application.

Ce module fournit la classe ConfigManager qui gère le chargement,
la sauvegarde et l'accès aux paramètres de configuration du jeu.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict


class ConfigManager:
    """Gestionnaire de configuration pour l'application Blackjack.
    
    Cette classe gère tous les paramètres de configuration du jeu,
    incluant les dimensions de l'écran, les couleurs, les timings,
    et les paramètres de jeu. La configuration est stockée dans un
    fichier JSON et peut être modifiée dynamiquement.
    
    Attributes:
        CONFIG_DIR (str): Répertoire contenant les fichiers de configuration
        CONFIG_FILE (str): Chemin du fichier de configuration principal
        DEFAULT_CONFIG (dict): Configuration par défaut du jeu
        config (dict): Configuration actuelle chargée
        
    Examples:
        >>> config = get_config_manager()
        >>> width = config.get('game.width', 1280)
        >>> config.set('game.fps', 60)
    """
    
    #: Répertoire des fichiers de configuration
    CONFIG_DIR = "config"
    #: Chemin du fichier de configuration principal
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
        """Initialise le gestionnaire de configuration.
        
        Charge la configuration depuis le fichier JSON ou crée
        une configuration par défaut si le fichier n'existe pas.
        """
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Charge la configuration depuis le fichier JSON.
        
        Returns:
            dict: Configuration chargée ou configuration par défaut
        """
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"erreur lors du chargement de la config {e}")
                return self.DEFAULT_CONFIG.copy()
        
        # Créer la config par défaut si elle n'existe pas
        self._save_config(self.DEFAULT_CONFIG)
        return self.DEFAULT_CONFIG.copy()
    
    def _save_config(self, config: Dict[str, Any]) -> None:
        """Sauvegarde la configuration dans le fichier JSON.
        
        Args:
            config (dict): Configuration à sauvegarder
        """
        os.makedirs(self.CONFIG_DIR, exist_ok=True)
        try:
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"erreur lors de la sauvegarde de la config {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Récupère une valeur de configuration.
        
        Utilise la notation pointée pour accéder aux valeurs imbriquées.
        
        Args:
            key (str): Clé de configuration (ex: 'game.width')
            default (Any, optional): Valeur par défaut si la clé n'existe pas
            
        Returns:
            Any: Valeur de configuration ou valeur par défaut
            
        Examples:
            >>> config.get('game.width', 1280)
            1280
            >>> config.get('game.fps')
            60
        """
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
        """Définit une valeur de configuration.
        
        Utilise la notation pointée pour définir des valeurs imbriquées.
        Sauvegarde automatiquement la configuration.
        
        Args:
            key (str): Clé de configuration (ex: 'game.fps')
            value (Any): Nouvelle valeur
            
        Examples:
            >>> config.set('game.fps', 120)
            >>> config.set('features.music_enabled', True)
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self._save_config(self.config)
    
    def get_all(self) -> Dict[str, Any]:
        """Retourne toute la configuration.
        
        Returns:
            dict: Copie complète de la configuration actuelle
        """
        return self.config.copy()
    
    def reset_to_default(self) -> None:
        """Réinitialise la configuration aux valeurs par défaut.
        
        Écrase la configuration actuelle et sauvegarde.
        """
        self.config = self.DEFAULT_CONFIG.copy()
        self._save_config(self.config)
    
    def get_game_settings(self) -> Dict[str, Any]:
        """Retourne les paramètres du jeu.
        
        Returns:
            dict: Paramètres de jeu (dimensions, FPS, nombre de jeux, etc.)
        """
        return self.config.get("game", {})
    
    def get_card_settings(self) -> Dict[str, Any]:
        """Retourne les paramètres des cartes.
        
        Returns:
            dict: Dimensions et espacement des cartes
        """
        return self.config.get("cards", {})
    
    def get_color_settings(self) -> Dict[str, Any]:
        """Retourne les paramètres des couleurs.
        
        Returns:
            dict: Palette de couleurs du jeu
        """
        return self.config.get("colors", {})
    
    def get_timing_settings(self) -> Dict[str, Any]:
        """Retourne les paramètres de timing.
        
        Returns:
            dict: Durées des animations et délais
        """
        return self.config.get("timing", {})
    
    def get_player_settings(self) -> Dict[str, Any]:
        """Retourne les paramètres du joueur.
        
        Returns:
            dict: Solde initial, mises min/max
        """
        return self.config.get("player", {})
    
    def get_features(self) -> Dict[str, Any]:
        """Retourne les paramètres de fonctionnalités.
        
        Returns:
            dict: État des fonctionnalités (son, animations, indices)
        """
        return self.config.get("features", {})
    
    def set_game_settings(self, settings: Dict[str, Any]) -> None:
        """Définit les paramètres du jeu.
        
        Args:
            settings (dict): Nouveaux paramètres de jeu
        """
        self.config["game"].update(settings)
        self._save_config(self.config)
    
    def toggle_feature(self, feature: str) -> bool:
        """Bascule l'état d'une fonctionnalité.
        
        Args:
            feature (str): Nom de la fonctionnalité à basculer
            
        Returns:
            bool: Nouvel état de la fonctionnalité
            
        Examples:
            >>> config.toggle_feature('music_enabled')
            True
        """
        features = self.config.get("features", {})
        current_state = features.get(feature, False)
        new_state = not current_state
        features[feature] = new_state
        self.config["features"] = features
        self._save_config(self.config)
        return new_state
    
    def print_config(self) -> None:
        """Affiche la configuration dans la console.
        
        Utile pour le débogage.
        """
        print(json.dumps(self.config, indent=2))


#: Instance globale du gestionnaire de configuration (singleton)
_config_manager = None


def get_config_manager() -> ConfigManager:
    """Retourne l'instance globale du gestionnaire de configuration.
    
    Utilise le pattern Singleton pour garantir une seule instance.
    
    Returns:
        ConfigManager: Instance unique du gestionnaire
        
    Examples:
        >>> config = get_config_manager()
        >>> fps = config.get('game.fps')
    """
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager