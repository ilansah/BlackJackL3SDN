# Guide de contribution

Merci de votre intérêt pour contribuer au projet Blackjack VIP Lounge !

## Code de conduite

Soyez respectueux et professionnel dans toutes vos interactions.

## Comment contribuer

### Signaler un bug

1. Vérifiez que le bug n'a pas déjà été signalé
2. Créez une issue avec :
   - Un titre descriptif
   - Les étapes pour reproduire
   - Le comportement attendu vs réel
   - Votre environnement (OS, Python version)

### Proposer une fonctionnalité

1. Créez une issue décrivant la fonctionnalité
2. Expliquez pourquoi elle serait utile
3. Attendez les retours avant de commencer à coder

### Soumettre des modifications

1. Forkez le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Pushez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## Standards de code

### Python

- Suivez PEP 8
- Utilisez des docstrings format Google/Sphinx
- Commentez le code complexe
- Gardez les fonctions courtes et focalisées

### Documentation

- Documentez toutes les classes et fonctions publiques
- Utilisez le format Google docstring
- Incluez des exemples quand pertinent
- Mettez à jour la documentation Sphinx si nécessaire

### Tests

- Ajoutez des tests pour les nouvelles fonctionnalités
- Assurez-vous que tous les tests passent
- Visez une couverture de code élevée

## Structure des commits

Format recommandé :

```
<type>: <description courte>

[description détaillée optionnelle]

[footer optionnel]
```

Types :
- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation
- `style`: Formatage, point-virgules manquants, etc.
- `refactor`: Refactorisation du code
- `test`: Ajout de tests
- `chore`: Maintenance

Exemples :
```
feat: Ajouter le support du double down

Implémente la fonctionnalité de double down
avec validation des conditions et mise à jour du solde.

Closes #42
```

```
fix: Corriger le calcul de la valeur de l'As

L'As n'était pas correctement ajusté de 11 à 1
quand la main dépassait 21.
```

## Configuration de l'environnement de développement

1. Clonez le repo
```bash
git clone https://github.com/ilansah/BlackJackL3SDN.git
cd BlackJackL3SDN
```

2. Installez les dépendances
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Pour le développement
```

3. Installez les hooks pre-commit (optionnel)
```bash
pre-commit install
```

## Build et tests

### Lancer le jeu
```bash
python src/main.py
```

### Générer la documentation
```bash
cd docs
make html
```

### Lancer les tests (à implémenter)
```bash
pytest
```

## Questions ?

N'hésitez pas à ouvrir une issue pour toute question !
