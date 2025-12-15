Guide d'utilisation
===================

Ce guide explique comment utiliser le jeu de Blackjack.

Lancement du jeu
----------------

Pour lancer le jeu, exécutez :

.. code-block:: bash

   python src/main.py

Menu principal
--------------

Le menu principal offre 4 options :

* **JOUER** : Commencer une nouvelle partie
* **PARAMÈTRES** : Modifier les réglages du jeu
* **STATISTIQUES** : Consulter vos statistiques
* **CLICKER** : Mini-jeu pour gagner de l'argent

Jouer une partie
----------------

Placement des mises
~~~~~~~~~~~~~~~~~~~

1. Sélectionnez une place en cliquant sur un des 5 sièges disponibles
2. Cliquez sur les jetons pour placer votre mise (5$, 10$, 50$, 100$)
3. Vous pouvez miser sur plusieurs places simultanément
4. Clic droit sur une place pour retirer la mise
5. Cliquez sur **COMMENCER** quand vous êtes prêt

Distribution initiale
~~~~~~~~~~~~~~~~~~~~~

Le jeu distribue automatiquement :

* 2 cartes pour chaque place avec mise
* 2 cartes pour le croupier (une cachée)

Actions disponibles
~~~~~~~~~~~~~~~~~~~

Pendant votre tour, vous pouvez :

* **H** (Hit) : Tirer une carte supplémentaire
* **S** (Stand) : Conserver votre main
* **D** (Double) : Doubler la mise et tirer 1 carte (uniquement avec 2 cartes)
* **P** (Split) : Diviser une paire en 2 mains (uniquement avec 2 cartes identiques)
* **R** (Surrender) : Abandonner et récupérer 50% de la mise

Assurance
~~~~~~~~~

Si le croupier a un As visible :

* Vous pouvez prendre une assurance (50% de la mise)
* Si le croupier a un Blackjack, l'assurance paie 2:1
* Sinon, vous perdez l'assurance

Résultats
~~~~~~~~~

À la fin de la partie :

* **Victoire** : Vous gagnez 1:1 (ou 3:2 pour un Blackjack)
* **Défaite** : Vous perdez votre mise
* **Égalité** : Vous récupérez votre mise

Appuyez sur **ESPACE** pour revenir aux mises.

Paramètres
----------

Personnalisez votre expérience :

Visuels
~~~~~~~

* **Thème de table** : Green, Blue, Red, Black
* **Animations** : Activer/Désactiver
* **Indices** : Afficher/Masquer les suggestions

Audio
~~~~~

* **Musique** : ON/OFF
* **Volume** : 0% à 100%

Jeu
~~~

* **Vitesse des animations** : 0.1x à 3.0x
* **Nombre de jeux** : 1 à 8 jeux dans le sabot

Statistiques
------------

Consultez vos performances :

* **Mains jouées** : Nombre total de mains
* **Victoires** : Nombre de victoires
* **Bénéfice net** : Profit ou perte global
* **Blackjacks** : Nombre de Blackjacks naturels obtenus
* **Taux de victoire** : Pourcentage de victoires

Mini-jeu Clicker
----------------

Le Clicker permet de gagner de l'argent en cliquant :

1. Accédez au Clicker depuis le menu principal
2. Cliquez sur le bouton **+$1**
3. Gagnez 1$ par clic
4. Votre solde est sauvegardé automatiquement
5. Appuyez sur **ESC** pour revenir au menu

Raccourcis clavier
------------------

Menu et navigation
~~~~~~~~~~~~~~~~~~

* **ESC** : Retour au menu principal / Quitter
* **ESPACE** : Nouvelle partie (après résultats)

Actions en jeu
~~~~~~~~~~~~~~

* **H** : Hit (tirer)
* **S** : Stand (rester)
* **D** : Double (doubler)
* **P** : Split (diviser)
* **R** : Surrender (abandonner)

Paramètres
~~~~~~~~~~

* **M** : Toggle musique
* **Clic sur sliders** : Ajuster les valeurs
* **Clic sur boutons** : Cycler les options

Conseils stratégiques
---------------------

Stratégie de base
~~~~~~~~~~~~~~~~~

* **Toujours splitter les As et les 8**
* **Ne jamais splitter les 10 et les 5**
* **Doubler sur 11 si le croupier a 10 ou moins**
* **Tirer jusqu'à 17+ si le croupier montre 7 ou plus**
* **Rester sur 17+ si le croupier montre 6 ou moins**

Gestion de la bankroll
~~~~~~~~~~~~~~~~~~~~~~~

* Ne misez pas plus de 5% de votre solde par main
* Fixez-vous des limites de gains et de pertes
* Utilisez le Clicker pour regagner de l'argent si nécessaire

Assurance
~~~~~~~~~

* Statistiquement désavantageuse
* Seulement recommandée si vous comptez les cartes
* Évitez de la prendre en temps normal

Dépannage
---------

Le jeu ne démarre pas
~~~~~~~~~~~~~~~~~~~~~

Vérifiez que pygame est installé :

.. code-block:: bash

   pip install pygame

Les images ne s'affichent pas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assurez-vous que le dossier ``assets/`` contient :

* ``assets/cards/`` avec les images des cartes
* ``assets/chips/`` avec les images des jetons

Le son ne fonctionne pas
~~~~~~~~~~~~~~~~~~~~~~~~~

* Vérifiez que la musique est activée dans les paramètres
* Assurez-vous que le fichier audio existe
* Réglez le volume dans les paramètres

Problèmes de sauvegarde
~~~~~~~~~~~~~~~~~~~~~~~~

Si les données ne se sauvegardent pas :

* Vérifiez les permissions du dossier
* Le fichier ``player_stats.json`` doit être accessible en écriture
* Le fichier ``config/settings.json`` doit exister
