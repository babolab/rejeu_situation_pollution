# Application Streamlit pour la Simulation de Dérive et Trajectoires de Navires

Cette application Streamlit permet de simuler la dérive d'un polluant et de visualiser les trajectoires de navires à proximité. Elle génère un GIF montrant l'évolution de la situation heure par heure.

## Fonctionnalités

- **Téléchargement de fichiers** : Importez un fichier GPX de dérive et plusieurs fichiers GPX de trajectoires de navires.
- **Visualisation** : Génère un GIF avec les points de dérive et de trajectoire affichés sur une carte OpenStreetMap.
- **Légende** : Affiche une légende avec les noms des fichiers de trajectoire et leurs couleurs associées.
- **Contrôle du GIF** : Possibilité de mettre en pause et de reprendre l'animation du GIF.

## Prérequis

- Python 3.x
- Les bibliothèques Python listées dans `requirements.txt`

## Installation

1. Clonez le dépôt GitHub :
   ```bash
   git clone <URL_DU_DEPOT_GITHUB>
   cd <NOM_DU_REPERTOIRE>
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

1. Exécutez l'application Streamlit :
   ```bash
   streamlit run app.py
   ```

2. Dans l'interface Streamlit :
   - Téléchargez un fichier GPX de dérive.
   - Téléchargez un ou plusieurs fichiers GPX de trajectoires de navires.
   - Cliquez sur le bouton "Lancer la simulation" pour générer le GIF.

3. Visualisez le GIF et la légende sur la page Streamlit.

## Remarques

- Assurez-vous que les dossiers `mothy` et `trajectoires` existent et sont accessibles en écriture.
- Le GIF est généré dans le répertoire de travail actuel.
