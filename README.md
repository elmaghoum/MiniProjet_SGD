# MiniProjet de Systèmes de gestion de documents (SGD) sur MongoDB - UB - 2023/2024

# Contexte

Dans le cadre d’un rendu de projet pour le module Systèmes de Gestion de Documents, on nous a demander de intéresser au développement d’une base de données MongoDB et d’un ensemble de fonctionnalités pour permettre de réaliser de l’analyse décisionnelle concernant un ensemble de Film, d'Avis et de Cinéma.


Ce mini-projet est pour nous une maniere de montrer qu’on peut exploiter les possibilités et les fonctionnalités offertes par une base de données MongoDB afin de réaliser une analyse décisionnelle sur des films diffusés dans les salles de cinéma.

# Modèle de Données pour le Projet de Cinéma
Pour répondre au sujet, nous avons décidé de composer notre modèle de données de trois collections :

### 1. Collection "Films"

Cette collection est composée des attributs suivants :

- **_id** : Identifiant unique du film.
- **titre** : Titre du film.
- **réalisateur** : Nom du réalisateur du film.
- **durée** : Durée du film en minutes.
- **date_de_sortie** : Date de sortie du film.
- **description** : Description du film.
- **catégorie** : Genre du film (Romance, Action, etc.).
- **salles_diffusion** : Tableau contenant les informations sur les salles où le film a été diffusé :
  - **num_salle** : Numéro de la salle de cinéma.
  - **nombre_place** : Nombre de places de la salle.
  - **date_diffusion** : Date de diffusion du film.
  - **heure_diffusion** : Horaire de diffusion du film.
  - **nombre_entrees** : Nombre d’entrées du film (nombre de personnes venues voir le film à cette date).
  - **cinema_id** : Identifiant du cinéma où se trouve la salle.

### 2. Collection "Avis"

Cette collection est composée des attributs suivants :

- **_id** : Identifiant unique de l’avis.
- **film_id** : Identifiant du film auquel l’avis est associé.
- **nom_utilisateur** : Nom de l’utilisateur ayant laissé l’avis.
- **commentaire** : Texte de l’avis.
- **note** : Note d’appréciation attribuée au film par l’utilisateur.
- **reseau_social** : Nom du réseau social où le commentaire a été posté.
- **date_commentaire** : Date à laquelle le commentaire a été posté.

### 3. Collection "Cinémas"

Cette collection est composée des attributs suivants :

- **_id** : Identifiant unique du cinéma.
- **nom** : Nom du cinéma.
- **ville** : Ville où se trouve le cinéma.


# Remarque
Pour réaliser un lien/association entre deux collections on utilisera un attribut comment entre les deux collections.
- Attribut commum entre la collection Films et la collection Avis : l’id du film
- Attribut commum entre la collection Films et la collection Cinemas : l’id du cinéma
- Attribut commum entre la collection Avis et la collection Cinemas : Aucun. Il faudra passé par la collection Film.

# Exemple de fonctionnalités
Afin de realiser de l’analyse décisionnelle nous aurons besoins des fonctionnalités suivantes :
- Afficher la liste des films, des cinémas et des avis.
- Afficher les détails (titre, durée, catégorie(s), ...), (nom du cinéma, adresse, ...), (note, nom du réseau social).
- Pouvoir trié les films grâce à leurs attributs.
- Pouvoir faire la recherche de films/cinémas/avis par attributs (titre, catégorie, date de sortie/adresse, nom du cinéma/ films, note, réseau social ...).
- Donnée des statistiques sur les films comme le nombre total de films, le nombre de film par catégorie et la moyenne des notes pour un même film dans different cinémas.
- Pouvoir faire l’analyse des performances (nombre d’entrée) d’une salle ou d’un cinémas en particulier.
- Afficher la moyenne des notes attribuées à chaque film.
- Etc

# Exemple de Requête MongoDB

Ce projet contient plusieurs répertoires avec des scripts pour l'insertion et l'exécution de requêtes sur les collections de données.

## Répertoires et Contenus

### 1. Répertoire `Insertions_des_donnees`

Ce répertoire contient les scripts d'insertion des données pour les trois collections de travail :

- **Scripts d'insertion** (insertMany) des collections :
  - **avis**
  - **cinemas**
  - **films**

### 2. Répertoire `Requetes_Mongo`

Ce répertoire contient des scripts de requêtes MongoDB :

- **find** dans le fichier `Requete-Find`
- **aggregate** dans le fichier `Requete-Aggregate`
- **Map-Reduce** dans le fichier `Requete-Map-Reduce`
- **delete** dans le fichier `Requete_delete`
- **update** dans le fichier `Requete_update`
- Ensemble de ces scripts + résultats dans le fichier `Requetes_Resultats`

### 3. Répertoire `Scripts_Python`

Ce répertoire contient des scripts de requêtes en Python :

- **Sans pipeline** dans le fichier `req_python_sans_pipeline.py`
- **Avec pipeline** dans le fichier `req_python_pipeline.py`


# Conclusion

Bien que nous connaissions déjà un peu MongoDB dès le départ, cela ne nous a pas empêché de rencontrer quelques difficultés. Nos problèmes étaient surtout liés à la compréhension et à la formalisation du sujet, mais ceux-ci ont été rapidement résolus lors de nos échanges par e-mail et de nos discussions en TD avec nos enseignants. 


En conclusion, ce projet a été riche en apprentissage. Il nous a permis de renforcer nos connaissances déjà acquises durant notre formation, mais aussi d’en acquérir de nouvelles, comme la programmation en utilisant Python, l’utilisation du plugin PyMongo (qui était nouveau pour nous).

Et bien sûr, ce projet nous a permis de mettre un pied (rapide et général) dans le monde du décisionnel et de la BI (Business Intelligence).

MongoDB s’ajoutera désormais à notre arsenal d’outils pour notre formation pédagogique et professionnelle.



# AUTEUR
- AMZAL Idir
- EL MAGHOUM Fayçal

--- Mai 2024
