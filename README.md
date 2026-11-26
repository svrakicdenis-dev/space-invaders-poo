# Space Invaders : Python Edition (Projet POO)

Version orientée objet du jeu **Space Invaders** développée en Python avec la bibliothèque **Pygame** par Thomas Sa. & Denis Sv.

## Prérequis

- **Python 3** (version 3.8 ou supérieure) installé sur votre machine ([télécharger Python](https://www.python.org/downloads/)).
  - *Sous Windows, pensez à cocher « Add Python to PATH » lors de l'installation.*

## 1. Récupérer le projet

### Option A — Avec Git (recommandé)
Ouvrez un terminal et exécutez :
```bash
git clone https://github.com/svrakicdenis-dev/space-invaders-poo.git
cd space-invaders-poo/
```

### Option B — Sans Git (téléchargement ZIP)
1. Cliquez sur le bouton vert **`<> Code`** en haut de cette page, puis sur **`Download ZIP`**.
2. Extrayez l'archive ZIP sur votre ordinateur.
3. Ouvrez un terminal **dans le dossier extrait** (celui qui contient `main.py`).

## 2. Installer les dépendances

Depuis le dossier du projet, installez Pygame via le fichier `requirements.txt` :

- **Sous Windows :**
```bash
pip install -r requirements.txt
```
*(Si `pip` n'est pas reconnu, utilisez `py -m pip install -r requirements.txt`)*

- **Sous macOS / Linux :**
```bash
pip3 install -r requirements.txt
```

## 3. Lancer le jeu

Toujours depuis le dossier racine du projet (là où se trouve `main.py`), exécutez :

- **Sous Windows :**
```bash
python main.py
```
*(Ou `py main.py` si `python` n'est pas reconnu)*

- **Sous macOS / Linux :**
```bash
python3 main.py
```

## Commandes pour jouer

- **Flèche Gauche (`←`) / Flèche Droite (`→`)** : Déplacer le vaisseau
- **Espace** : Tirer (et relancer une partie sur l'écran *Game Over*)
- **Échap (`ESC`)** : Mettre le jeu en pause / reprendre (ou quitter le jeu sur l'écran *Game Over*)

## Structure du projet

- `main.py` : Code source complet du jeu (classes et boucle principale)
- `requirements.txt` : Liste des dépendances Python (`pygame`)
- `highscore.txt` : Sauvegarde du meilleur score
- `sprites/` : Images du vaisseau, des ennemis et des lasers
- `sfx/` : Effets sonores et musique de démarrage
- `font/` : Police d'écriture (`PressStart2P.ttf`)
