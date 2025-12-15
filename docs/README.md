# Documentation Blackjack L3 SDN

Ce dossier contient la documentation complète du projet Blackjack.

## Installation des dépendances

Pour générer la documentation, vous devez installer Sphinx et ses extensions :

```bash
pip install sphinx sphinx-rtd-theme
```

## Génération de la documentation

### Format HTML

Pour générer la documentation au format HTML :

```bash
cd docs
make html
```

ou sous Windows :

```bash
cd docs
make.bat html
```

La documentation sera disponible dans `docs/_build/html/index.html`.

### Format PDF

Pour générer la documentation au format PDF, vous devez avoir LaTeX installé sur votre système.

#### Installation de LaTeX

**Windows :**
- Téléchargez et installez MiKTeX : https://miktex.org/download
- OU TeXLive : https://www.tug.org/texlive/

**Linux (Debian/Ubuntu) :**
```bash
sudo apt-get install texlive-latex-recommended texlive-fonts-recommended texlive-latex-extra latexmk
```

**macOS :**
```bash
brew install --cask mactex
```

#### Générer le PDF

Une fois LaTeX installé :

```bash
cd docs
make latexpdf
```

ou sous Windows :

```bash
cd docs
make.bat latexpdf
```

Le PDF sera généré dans `docs/_build/latex/BlackjackL3SDN.pdf`.

## Autres formats disponibles

- **EPUB** : `make epub` (livre électronique)
- **Manual Pages** : `make man` (pages de manuel Unix)
- **Text** : `make text` (texte brut)

## Structure de la documentation

```
docs/
├── conf.py              # Configuration Sphinx
├── index.rst            # Page d'accueil
├── installation.rst     # Guide d'installation
├── usage.rst           # Guide d'utilisation
├── modules/
│   ├── core.rst        # Documentation du module core
│   └── game.rst        # Documentation du module game
├── Makefile            # Makefile pour Linux/macOS
└── make.bat            # Script batch pour Windows
```

## Mise à jour de la documentation

Après avoir modifié les docstrings dans le code source, régénérez la documentation :

```bash
cd docs
make clean
make html
```

## Visualiser la documentation

### HTML

Ouvrez simplement le fichier `docs/_build/html/index.html` dans votre navigateur.

### PDF

Ouvrez le fichier `docs/_build/latex/BlackjackL3SDN.pdf` avec votre lecteur PDF.

## Format des docstrings

Ce projet utilise le format **Google Style** pour les docstrings :

```python
def ma_fonction(param1: int, param2: str) -> bool:
    """Description courte de la fonction.
    
    Description détaillée optionnelle sur plusieurs lignes
    expliquant le fonctionnement de la fonction.
    
    Args:
        param1 (int): Description du premier paramètre
        param2 (str): Description du deuxième paramètre
        
    Returns:
        bool: Description de la valeur de retour
        
    Raises:
        ValueError: Description de quand cette exception est levée
        
    Examples:
        >>> ma_fonction(42, "test")
        True
    """
    pass
```

## Aide

Pour obtenir de l'aide sur Sphinx :

```bash
make help
```

Pour plus d'informations sur Sphinx : https://www.sphinx-doc.org/
