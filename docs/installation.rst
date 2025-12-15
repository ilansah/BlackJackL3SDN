Installation
============

Prérequis
---------

* Python 3.8 ou supérieur
* pip (gestionnaire de paquets Python)

Installation des dépendances
-----------------------------

.. code-block:: bash

   pip install pygame

Installation du projet
----------------------

1. Clonez le dépôt Git :

   .. code-block:: bash

      git clone https://github.com/ilansah/BlackJackL3SDN.git
      cd BlackJackL3SDN

2. Lancez le jeu :

   .. code-block:: bash

      python src/main.py

Structure du projet
-------------------

.. code-block:: text

   BlackJackL3SDN/
   ├── src/
   │   ├── main.py              # Point d'entrée du jeu
   │   ├── config_manager.py    # Gestion de la configuration
   │   ├── stats_manager.py     # Gestion des statistiques
   │   ├── settings_ui.py       # Interface des paramètres
   │   └── core/
   │       ├── __init__.py
   │       ├── card.py          # Gestion des cartes
   │       ├── deck.py          # Gestion du sabot
   │       ├── hand.py          # Gestion des mains
   │       ├── game.py          # Logique du jeu
   │       └── player.py        # Gestion du joueur
   ├── assets/
   │   ├── cards/               # Images des cartes
   │   └── chips/               # Images des jetons
   ├── config/
   │   └── settings.json        # Configuration du jeu
   ├── docs/                    # Documentation
   └── player_stats.json        # Sauvegarde du joueur

Configuration
-------------

Le fichier ``config/settings.json`` contient tous les paramètres du jeu :

* Dimensions de la fenêtre
* Nombre de jeux dans le sabot
* Délais d'animation
* Couleurs du thème
* Paramètres du joueur (solde initial, mises min/max)
* Fonctionnalités activées (son, animations, indices)
