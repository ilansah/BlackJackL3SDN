Module Game
===========

Le module ``game`` contient la logique principale du jeu de Blackjack,
incluant les états du jeu, les actions possibles et l'orchestration des parties.

.. automodule:: core.game
   :members:
   :undoc-members:
   :show-inheritance:

États du jeu
------------

Le jeu utilise une machine à états pour gérer les différentes phases :

.. autoclass:: core.game.GameState
   :members:
   :undoc-members:

Cycle de vie d'une partie
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **MENU** : Écran principal avec choix Jouer/Paramètres/Stats/Clicker
2. **BETTING** : Sélection des places et placement des mises
3. **INITIAL_DEAL** : Distribution des 2 cartes initiales
4. **PLAYER_TURN** : Le joueur choisit ses actions (Hit, Stand, Double, Split)
5. **DEALER_REVEAL** : Révélation de la carte cachée du croupier
6. **DEALER_TURN** : Le croupier joue selon la règle fixe (tire jusqu'à 17+)
7. **RESULT_SCREEN** : Affichage des résultats et mise à jour des soldes

Résultats possibles
-------------------

.. autoclass:: core.game.GameResult
   :members:
   :undoc-members:

Actions du joueur
-----------------

.. autoclass:: core.game.PlayerAction
   :members:
   :undoc-members:

Actions disponibles
~~~~~~~~~~~~~~~~~~~

* **HIT** : Tirer une carte supplémentaire
* **STAND** : Conserver sa main et passer au croupier
* **DOUBLE** : Doubler la mise et tirer exactement 1 carte
* **SPLIT** : Diviser une paire en deux mains séparées

Classe Game
-----------

.. autoclass:: core.game.Game
   :members:
   :undoc-members:
   :show-inheritance:

Méthodes principales
~~~~~~~~~~~~~~~~~~~~

Vérification des actions
^^^^^^^^^^^^^^^^^^^^^^^^^

* ``can_hit()`` : Vérifie si le joueur peut tirer
* ``can_stand()`` : Vérifie si le joueur peut s'arrêter
* ``can_double()`` : Vérifie si le joueur peut doubler
* ``can_split()`` : Vérifie si le joueur peut splitter
* ``can_take_insurance()`` : Vérifie si l'assurance est disponible
* ``can_surrender()`` : Vérifie si le joueur peut abandonner

Actions du joueur
^^^^^^^^^^^^^^^^^

* ``player_hit()`` : Exécute l'action Hit
* ``player_stand()`` : Exécute l'action Stand
* ``player_double()`` : Exécute l'action Double
* ``player_split()`` : Exécute l'action Split
* ``take_insurance()`` : Prend l'assurance
* ``player_surrender()`` : Abandonne la main

Gestion du jeu
^^^^^^^^^^^^^^

* ``deal_initial_cards()`` : Distribue les cartes initiales
* ``dealer_play()`` : Fait jouer le croupier
* ``reset()`` : Réinitialise pour une nouvelle partie

Exemples d'utilisation
-----------------------

Initialiser une partie
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from core.game import Game, GameState
   from core.player import Player
   
   # Créer une partie avec 6 jeux
   game = Game(num_decks=6)
   player = Player(balance=1000)
   
   # Placer une mise
   game.player_bet = 100
   game.state = GameState.BETTING

Jouer une main
~~~~~~~~~~~~~~

.. code-block:: python

   # Distribuer les cartes
   game.deal_initial_cards()
   game.state = GameState.PLAYER_TURN
   
   # Le joueur tire une carte
   if game.can_hit():
       game.player_hit()
   
   # Le joueur s'arrête
   if game.can_stand():
       game.player_stand()
   
   # Le croupier joue
   game.dealer_play()

Utiliser le split
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Si le joueur a une paire
   if game.can_split():
       game.player_split()
       
   # Jouer la première main
   game.player_hit()
   game.player_stand()
   
   # Jouer la deuxième main (automatique)

Mode multi-places
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Placer des mises sur plusieurs places
   game.seat_bets = {
       0: 100,  # Place 1 : 100$
       2: 50,   # Place 3 : 50$
       4: 200   # Place 5 : 200$
   }
   
   # Distribuer pour toutes les places
   game.deal_initial_cards_multiseat()
   
   # Le jeu gère automatiquement chaque place

Règles du Blackjack
-------------------

Objectif
~~~~~~~~

Obtenir une main dont la valeur est plus proche de 21 que celle du croupier,
sans dépasser 21 (bust).

Valeurs des cartes
~~~~~~~~~~~~~~~~~~

* As : 1 ou 11 (ajustement automatique)
* Figures (J, Q, K) : 10
* Autres cartes : valeur nominale

Blackjack naturel
~~~~~~~~~~~~~~~~~

Un Blackjack est une main de 2 cartes valant 21 (As + Figure/10).
Il bat toute autre main de 21 points et paie 3:2.

Règles du croupier
~~~~~~~~~~~~~~~~~~

Le croupier doit :

* Tirer jusqu'à atteindre au moins 17
* S'arrêter dès qu'il atteint 17 ou plus
* Ne peut pas doubler ni splitter
