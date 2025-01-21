# Python Royal

## Description

Support pour le workshop Python Royal du SnowCamp 2025.

## Objectifs

Apprendre à faire du code Python stylé et robuste !

Python a la réputation de ne pas être axé sur la qualité logicielle. 
C’était vrai il y a 20 ans, mais depuis de grands noms se sont bâtis sur ce langage :
Instagram, Spotify, Reddit, Dropbox...
Pour arriver à allier Fiabilité, Maintenabilité, Évolutivité et Sécurité (= la fameuse
Qualité), il faut apprendre le fonctionnement du langage et de son écosystème.

Découvrons ensemble la structure d'un projet Python, les principes du langage à 
respecter, l'outillage à mettre en place et les pratiques à adopter pour travailler
en Python avec une qualité industrielle. 

## Prérequis

- avoir les bases en Python
- pouvoir installer des logiciels sur sa machine (accès réseau et droits)
- un shell
- si possible un compte GitLab ou GitHub

## Déroulement

Il y a des fichiers de détecteur de rayon X/gamma sur ce repo, affichons-les !

- [ ] Créer un projet sur son compte perso GitHub ou Gitlab
- [ ] Cloner le projet sur sa machine perso
- [ ] Installer uv
- [ ] Initier un nouveau projet avec uv
- [ ] Remplir le `pyproject.toml`
- [ ] Ajouter une dépendance : [Streamlit](https://streamlit.io/)
- [ ] Afficher le hello world Streamlit
- [ ] Ajouter de nouvelles dépendances : pandas et plotly
- [ ] Charger un fichier et afficher la courbe avec Streamlit

Et maintenant, un peu d'outillage.

- [ ] Installer ruff, mypy et pytest en dépendance de dev
- [ ] Formatter son code avec ruff
- [ ] Analyser son code avec ruff
- [ ] Vérifier les types avec mypy
- [ ] Écrire un test avec pytest
- [ ] Intégrer ces pratiques dans son workflow avec son IDE

Publions ce code.

- [ ] Créer une release et son tag sur Git(Hub|Lab)
- [ ] Créer un paquet (formats sdist et wheel) avec uv
- [ ] Intégrer le tag dans le paquet avec versioningit
- [ ] Publier ce code sur le package registry de Git(Hub|Lab)
- [ ] (en option, construire une image Docker contenant le code et la publier)

Automatisons un peu tout ça.

- [ ] Vérifier le code avec de commiter avec pre-commit
- [ ] Uniformiser le workflow avec Doit (voire Make)
- [ ] Lancer la vérification automatique avec GitLab CI / GitHub Actions

Et quand même documentons.

- [ ] Installer sphinx en dev
- [ ] Construire la base de sa documentation
- [ ] Extraire les docstrings et les intégrer avec apidoc

Continuer l'application tant qu'on peut !

- [ ] Ajouter un champ pour charger un fichier de données
- [ ] Extraire le temps d'acquisition et afficher les courbes en impact/s
- [ ] Ajouter une page de recherche de pics sur les courbes
- [ ] Étalonner les courbes en énergie à partir des courbes de références
  (Na22, Cs137, Co60)
- [ ] Refactoriser en séparant affichage, lecture de données, et traitement
- [ ] Enregistrer les valeurs d'étalonnage dans l'état de l'application et les utiliser
  pour toutes les courbes
- [ ] Ajouter un champ optionnel pour charger un second fichier à soustraire au premier
- [ ] Ajuster les couleurs, ajouter un logo (CSS en option)
