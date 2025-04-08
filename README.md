# Python Royal

[![Project management: uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Code style & Static analysis: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Type check: Mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Pipeline status](https://gitlab.com/jgaffiot1/python-royal/badges/app-demo/pipeline.svg)](https://gitlab.com/jgaffiot1/python-royal/-/commits/app-demo)
[![Coverage report](https://gitlab.com/jgaffiot1/python-royal/badges/app-demo/coverage.svg)](https://gitlab.com/jgaffiot1/python-royal/-/commits/app-demo)
[![Latest release](https://gitlab.com/jgaffiot1/python-royal/-/badges/release.svg)](https://gitlab.com/jgaffiot1/python-royal/-/releases)

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

- [ ] Forker le projet [GitLab](https://gitlab.com/jgaffiot1/python-royal)
      ou [GitHub](https://github.com/Lenormju/python-royal) sur son compte perso
- [ ] Cloner le fork sur sa machine perso
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

- [ ] Vérifier le code avant de commiter avec pre-commit
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

## Données

Les données proviennent d'un capteur de rayonnement X et gamma (la version plus
énergétique des X), utilisé pour mesurer la radioactivité résiduelle d'échantillons
qu'on espère très purs, donc de très faibles radioactivités.

Il fonctionne sur un principe proche des panneaux solaires, mais au lieu d'être exposé
à une quantité astronomique de photons optiques, il ne reçoit qu'un photon X ou gamma
de temps en temps. Le capteur ne donne donc pas un courant continu comme le panneau
solaire, mais de petits pics quand par hasard un photon X ou gamma tape dedans.
La hauteur du pic nous donne l'énergie du photon qui a impacté le capteur.

Sauf que le capteur enregistre ces hauteurs de façon très, très brute. Il se contente
de compter les hauteurs sur une échelle allant de 1 à 16384. Ce ne sont même pas des
volts ou une unité d'énergie, juste le nombre de canaux du convertisseur
analogique/numérique, qui code les hauteurs sur 14 bits (16384=2^14).
Comme le capteur ne fait que compter les impacts, il faut tenir compte manuellement
du temps d'enregistrement pour savoir si l'échantillon était peu ou beaucoup radioactif
(combien d'impact en 1 heure par exemple ?).

Pour retrouver l'échelle d'énergie, on place devant le capteur des éléments radioactifs
connus, donc on connait l'énergie des pics (keV=une unité d'énergie) :

- Cobalt 60 (Co60) : 2 pics à 1173.2 keV et 1332.5 keV
- Sodium 22 (Na22) : 2 pics à 511 keV et 1274.5 keV
- Césium 137 (CS137) : pic à 661.7 keV

Enfin, les photons X ou gamma peuvent venir de l'échantillon ou de l'environnement, qui
est toujours un peu radioactif. Pour en tenir compte, il faut soustraire à la mesure
d'un échantillon la mesure de la radioactivité de l'environnement, qu'on appelle
le bruit de fond (background en anglais). On a des mesures de deux échantillons :
"pmt" et "steel", et deux bruits de fond : "bkg" et "bkg2".

À vos claviers !
