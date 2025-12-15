Modules utilitaires
===================

Le projet contient plusieurs modules utilitaires pour gérer
la configuration, l'interface et les statistiques.

Module config_manager
---------------------

.. automodule:: config_manager
   :members:
   :undoc-members:
   :show-inheritance:

Exemples d'utilisation
~~~~~~~~~~~~~~~~~~~~~~~

Configuration de base
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from config_manager import get_config_manager
   
   # Obtenir l'instance du gestionnaire
   config = get_config_manager()
   
   # Lire une valeur
   fps = config.get('game.fps', 60)
   width = config.get('game.width')
   
   # Modifier une valeur
   config.set('game.fps', 120)
   config.set('features.music_enabled', True)

Gestion des thèmes
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Obtenir le thème actuel
   theme = config.get('ui.table_theme', 'green')
   
   # Changer le thème
   config.set('ui.table_theme', 'blue')

Fonctionnalités
^^^^^^^^^^^^^^^

.. code-block:: python

   # Activer/désactiver la musique
   new_state = config.toggle_feature('music_enabled')
   
   # Obtenir toutes les fonctionnalités
   features = config.get_features()
   print(features)  # {'music_enabled': True, 'animations_enabled': True, ...}

Réinitialisation
^^^^^^^^^^^^^^^^

.. code-block:: python

   # Réinitialiser tous les paramètres
   config.reset_to_default()

Module settings_ui
------------------

.. automodule:: settings_ui
   :members:
   :undoc-members:
   :show-inheritance:

Composants UI disponibles
~~~~~~~~~~~~~~~~~~~~~~~~~~

Bouton Toggle
^^^^^^^^^^^^^

.. code-block:: python

   import pygame
   from settings_ui import draw_toggle_button
   
   # Créer un bouton ON/OFF
   rect = pygame.Rect(400, 300, 100, 40)
   is_on = True
   is_hover = False
   
   draw_toggle_button(screen, rect, is_on, "Musique", is_hover)

Slider
^^^^^^

.. code-block:: python

   from settings_ui import draw_slider
   
   # Créer un slider pour le volume (0-1)
   rect = pygame.Rect(400, 350, 300, 40)
   volume = 0.75
   
   draw_slider(screen, rect, volume, 0.0, 1.0, "Volume", 
               is_dragging=False, is_hover=False)

Bouton de cycle
^^^^^^^^^^^^^^^

.. code-block:: python

   from settings_ui import draw_cycle_button
   
   # Créer un bouton pour cycler entre des thèmes
   rect = pygame.Rect(400, 400, 250, 40)
   themes = ['Green', 'Blue', 'Red', 'Black']
   current = 0  # 'Green'
   
   draw_cycle_button(screen, rect, themes, current, "Thème")

Module stats_manager
--------------------

.. automodule:: stats_manager
   :members:
   :undoc-members:
   :show-inheritance:

Gestion des statistiques
~~~~~~~~~~~~~~~~~~~~~~~~~

Chargement et sauvegarde
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from stats_manager import StatsManager
   
   # Charger les statistiques
   stats = StatsManager.load_stats()
   
   # Enregistrer une partie
   StatsManager.record_hand(
       result='win',
       bet=100,
       profit=150,
       player_value=20,
       dealer_value=19
   )
   
   # Sauvegarder
   StatsManager.save_stats(stats)

Analyse des statistiques
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Obtenir les statistiques globales
   total_hands = stats.get('total_hands', 0)
   win_rate = stats.get('win_rate', 0.0)
   total_profit = stats.get('total_profit', 0)
   
   # Historique des parties
   history = StatsManager.load_history()
   last_10 = history[-10:]  # 10 dernières parties

Structure de configuration
---------------------------

Le fichier ``config/settings.json`` contient :

.. code-block:: json

   {
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
     "player": {
       "starting_balance": 1000,
       "min_bet": 5,
       "max_bet": 1000
     },
     "features": {
       "sound_enabled": false,
       "music_enabled": true,
       "music_volume": 0.5,
       "animations_enabled": true,
       "show_hints": true
     },
     "ui": {
       "table_theme": "green"
     }
   }

Thèmes disponibles
~~~~~~~~~~~~~~~~~~

Le jeu propose 4 thèmes de table :

* **Green** (Vert classique) - Par défaut
* **Blue** (Bleu royal)
* **Red** (Rouge élégant)
* **Black** (Noir luxueux)

Chaque thème modifie les couleurs du feutre de la table.
