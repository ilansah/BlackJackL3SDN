Module Core
===========

Le module ``core`` contient tous les composants de base du jeu de Blackjack.

Vue d'ensemble
--------------

Le package ``core`` est organisé en plusieurs modules spécialisés :

* ``card`` : Représentation des cartes à jouer
* ``deck`` : Gestion du sabot de cartes
* ``hand`` : Gestion des mains de cartes
* ``game`` : Logique principale du jeu
* ``player`` : Gestion du joueur et statistiques

Module card
-----------

.. automodule:: core.card
   :members:
   :undoc-members:
   :show-inheritance:

Module deck
-----------

.. automodule:: core.deck
   :members:
   :undoc-members:
   :show-inheritance:

Module hand
-----------

.. automodule:: core.hand
   :members:
   :undoc-members:
   :show-inheritance:

Module player
-------------

.. automodule:: core.player
   :members:
   :undoc-members:
   :show-inheritance:

Exemples d'utilisation
-----------------------

Créer et manipuler une carte
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from core.card import Card
   
   # Créer un As de pique
   card = Card("A", "♠")
   print(card)  # Affiche: A♠
   print(card.value())  # Affiche: 11

Créer et utiliser un sabot
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from core.deck import Deck
   
   # Créer un sabot de 6 jeux (standard casino)
   deck = Deck(num_decks=6)
   
   # Tirer 5 cartes
   cards = deck.draw(5)
   
   # Brûler 3 cartes
   deck.burn(3)

Gérer une main de cartes
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from core.hand import Hand
   from core.card import Card
   
   hand = Hand()
   hand.add_card(Card("A", "♠"))
   hand.add_card(Card("K", "♥"))
   
   print(hand.get_value())  # 21
   print(hand.is_blackjack())  # True

Gérer un joueur
~~~~~~~~~~~~~~~

.. code-block:: python

   from core.player import Player
   
   # Créer un nouveau joueur
   player = Player(balance=1000)
   
   # Enregistrer une victoire de 100$
   player.win_hand(100)
   
   # Sauvegarder les données
   player.save()
   
   # Charger un joueur existant
   player = Player.load()
