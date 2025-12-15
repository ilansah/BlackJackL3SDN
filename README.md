# Blackjack VIP Lounge 🎰

Un jeu de Blackjack complet en Python avec Pygame, offrant une interface graphique élégante de style VIP, des statistiques détaillées et de nombreuses fonctionnalités avancées.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Fonctionnalités

### Jeu complet
- ✅ Règles officielles du Blackjack
- ✅ Mode multi-places (jusqu'à 5 places simultanées)
- ✅ Actions avancées : **Split**, **Double Down**, **Assurance**, **Abandon**
- ✅ Système de mises avec jetons (5$, 10$, 50$, 100$)
- ✅ Détection automatique des Blackjacks naturels

### Interface graphique VIP
- 🎨 Design élégant style casino de luxe
- 🎨 4 thèmes de table (Vert, Bleu, Rouge, Noir)
- 🎨 Animations fluides et effets visuels
- 🎨 Interface responsive et intuitive
- 🎨 Effets de hover et feedback visuel

### Gestion du joueur
- 💰 Système de solde et de mises
- 💰 Mini-jeu **Clicker** pour gagner de l'argent
- 💰 Statistiques détaillées (victoires, défaites, taux de réussite)
- 💰 Sauvegarde automatique de la progression
- 💰 Historique des parties

### Paramètres personnalisables
- ⚙️ Thèmes de table
- ⚙️ Musique et volume
- ⚙️ Vitesse des animations
- ⚙️ Nombre de jeux dans le sabot
- ⚙️ Affichage des indices

## 🚀 Installation rapide

```bash
# Installer les dépendances
pip install pygame

# Lancer le jeu
python src/main.py
```

## 🎮 Contrôles du jeu

### Menu principal
- **Clic** sur les boutons pour naviguer
- **ESC** - Quitter le jeu

### Placement des mises
- **Clic gauche** sur un siège pour le sélectionner
- **Clic** sur les jetons pour placer une mise
- **Clic droit** sur un siège pour retirer la mise
- **COMMENCER** - Lancer la partie

### Pendant le jeu
- **H** - Hit (tirer une carte)
- **S** - Stand (s'arrêter)
- **D** - Double Down (doubler la mise)
- **P** - Split (diviser une paire)
- **R** - Surrender (abandonner)
- **SPACE** - Nouvelle partie (après résultats)
- **ESC** - Retour au menu

### Paramètres
- **M** - Toggle musique
- **Clic** sur sliders pour ajuster les valeurs
- **Clic** sur boutons pour cycler les options

## 📖 Comment jouer

1. **Placement des mises** - Sélectionnez une ou plusieurs places et placez vos mises
2. **Distribution** - Vous et le croupier recevez 2 cartes chacun (une carte du croupier est cachée)
3. **Votre tour** - Choisissez **Hit** (tirer), **Stand** (rester), **Double** (doubler) ou **Split** (diviser)
4. **Tour du croupier** - Le croupier joue automatiquement (tire jusqu'à 17 minimum)
5. **Résultat** - Comparez vos mains : le plus proche de 21 gagne !
6. **Nouvelle partie** - Appuyez sur **SPACE** pour rejouer

## 🎲 Règles du Blackjack

### Valeurs des cartes
- **Cartes 2-10** : Valeur nominale
- **Figures (J, Q, K)** : 10 points
- **As** : 11 ou 1 (ajustement automatique)

### Objectif
Obtenir une main plus proche de 21 que le croupier sans dépasser 21.

### Blackjack naturel
21 avec exactement 2 cartes (As + Figure/10) - Paie 3:2

### Actions disponibles
- **Hit** : Tirer une carte supplémentaire
- **Stand** : Conserver sa main et passer
- **Double Down** : Doubler la mise et tirer exactement 1 carte
- **Split** : Diviser une paire en 2 mains (nécessite une mise supplémentaire)
- **Insurance** : Assurance contre un Blackjack du croupier (si As visible)
- **Surrender** : Abandonner et récupérer 50% de la mise

### Règle du croupier
- Tire jusqu'à atteindre au moins 17
- S'arrête dès 17 ou plus
- Ne peut ni doubler ni splitter

## 📁 Structure du projet

```
BlackJackL3SDN/
├── src/
│   ├── main.py              # Point d'entrée et interface graphique
│   ├── config_manager.py    # Gestion de la configuration
│   ├── stats_manager.py     # Gestion des statistiques
│   ├── settings_ui.py       # Composants UI des paramètres
│   └── core/
│       ├── __init__.py      # Package core
│       ├── card.py          # Classe Card (cartes)
│       ├── deck.py          # Classe Deck (sabot)
│       ├── hand.py          # Classe Hand (mains)
│       ├── game.py          # Classe Game (logique du jeu)
│       └── player.py        # Classe Player (joueur et stats)
├── assets/
│   ├── cards/               # Images des cartes (52 cartes)
│   └── chips/               # Images des jetons
├── config/
│   └── settings.json        # Configuration du jeu
├── docs/                    # Documentation Sphinx
│   ├── conf.py
│   ├── index.rst
│   └── modules/
├── player_stats.json        # Sauvegarde du joueur
└── README.md

```

## 📚 Documentation

Une documentation complète est disponible au format HTML et PDF.

### Générer la documentation HTML

```bash
cd docs
pip install sphinx sphinx-rtd-theme
make html
# Ou sous Windows : make.bat html
```

La documentation sera dans `docs/_build/html/index.html`

### Générer la documentation PDF

Nécessite LaTeX (MiKTeX ou TeXLive).

```bash
cd docs
make latexpdf
# Ou sous Windows : make.bat latexpdf
```

Le PDF sera dans `docs/_build/latex/BlackjackL3SDN.pdf`

## 🛠️ Technologies utilisées

- **Python 3.8+**
- **Pygame 2.0+** - Graphismes et interface
- **JSON** - Sauvegarde des données
- **Sphinx** - Génération de documentation

## 📊 Fonctionnalités avancées

### Mode multi-places
Jouez sur plusieurs places simultanément (jusqu'à 5) pour augmenter vos gains.

### Mini-jeu Clicker
Gagnez de l'argent en cliquant sur le bouton +$1 pour reconstituer votre solde.

### Statistiques détaillées
- Nombre total de mains jouées
- Taux de victoire
- Profit/Perte net
- Nombre de Blackjacks
- Historique des parties

### Thèmes personnalisables
- **Green** (Vert classique) - Par défaut
- **Blue** (Bleu royal)
- **Red** (Rouge élégant)
- **Black** (Noir luxueux)

## 🤝 Contribution

Ce projet a été développé dans le cadre du cours de Conception Logicielle L3 SDN.

### Équipe
- Développeurs : Équipe Blackjack L3 SDN
- Université : [Votre université]
- Année : 2025

## 📝 License

MIT License - Voir le fichier LICENSE pour plus de détails.

## 🐛 Bugs connus et support

Pour signaler un bug ou demander une fonctionnalité, ouvrez une issue sur GitHub.

## 🎯 Roadmap

- [ ] Multijoueur en ligne
- [ ] Tournois
- [ ] Système d'achievements
- [ ] Classement global
- [ ] Support mobile

---

**Bon jeu et bonne chance ! 🍀**
└── core/
    ├── card.py          # Card class
    ├── deck.py          # Deck management
    ├── hand.py          # Hand calculation
    ├── game.py          # Game logic
    └── player.py        # Stats tracking
```

## Statistics

Your stats are saved automatically to `player_stats.json`:
- Total hands played
- Wins / Losses / Ties
- Win percentage
- Net profit/loss
- Blackjack count

## Requirements

- Python 3.11+
- Pygame 2.x

## Card Images

Place card images in `assets/cards/` (optional - game works with placeholders if missing).

Expected filenames: `ace_of_spades.png`, `king_of_hearts.png`, etc.

## License

MIT License
