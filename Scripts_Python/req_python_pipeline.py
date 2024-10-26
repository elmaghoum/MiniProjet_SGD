from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint
from datetime import datetime

#connexion au serveur mongo2
c=MongoClient("mongo2.iem",port=27017,username="fe874388",password="fe874388",authSource="fe874388",authMechanism="SCRAM-SHA-1")

#récupération de la base de données
db=c.fe874388


#récupérer toutes les collections
films = db.films.find()
cinemas = db.cinemas.find()
avis_films = db.avis.find()
 

## Requête n°1 : Obtenir le nombre total d'avis par réseau social
pipeline = [
    {"$group": {"_id": "$reseau_social", "nombre_avis": {"$sum": 1}}},
    {"$sort": {"nombre_avis": -1}}
]

result3 = db.avis.aggregate(pipeline)

## Résultats n°1
pprint("Nombre total d'avis par réseau social :")
for doc in result3:
    pprint(f"{doc['_id']}: {doc['nombre_avis']} avis")

'''
"Nombre total d'avis par réseau social :"
'Twitter: 4 avis'
'Instagram: 3 avis'
'Facebook: 3 avis'
'''

## Requête n°2 : afficher les noms des films qui ont une note moyenne >= 4.0
moyenne_minimale = 4.0
pipeline = [
    {"$group": {"_id": "$film_id", "moyenne": {"$avg": "$note"}}},
    {"$match": {"moyenne": {"$gte": moyenne_minimale}}}
]
result = db.avis.aggregate(pipeline)
pprint("tous les noms des films qui ont une note moyenne >= 4.0 :")
for doc in result:
    film = db.films.find_one({"_id": doc["_id"]})
    pprint(film["titre"])

## Résultat n°2 
'''
'tous les noms des films qui ont une note moyenne >= 4.0 :'
'Titanic'
'The Shawshank Redemption'
'The Dark Knight'
'Pulp Fiction'
'Fight Club'
'Forrest Gump'
'Inception'
'''

## Requête 3 : afficher la Moyenne des notes pour chaque réseau social
pipeline = [
    {"$group": {"_id": "$reseau_social", "moyenne_notes": {"$avg": "$note"}}}
]

pprint("moyennes des notes par réseau social : ")
result = db.avis.aggregate(pipeline)
for doc in result:
    pprint(f"Moyenne des notes sur {doc['_id']}: {doc['moyenne_notes']:.2f}")

## Résultats n°3
'''
'moyennes des notes par réseau social : '
'Moyenne des notes sur Twitter: 4.80'
'Moyenne des notes sur Instagram: 4.87'
'Moyenne des notes sur Facebook: 4.97'
'''
    

## Requête n°4 : afficher le film qui a la longue durée
pipeline = [
    {"$sort": {"duree": -1}},
    {"$limit": 1}
]

result = db.films.aggregate(pipeline)
pprint("le film avec la plus longue durée est : ")
for film in result:
    pprint(film)

## Résultats n°4
'''
'le film avec la plus longue durée est :
{'_id': ObjectId('60527b186168afabf7e0c0e2'),
 'categorie': ['Action', 'Romance'],
 'date_de_sortie': datetime.datetime(2004, 12, 10, 0, 0),
 'description': '',
 'duree': 194.0,
 'realisateur': 'James Cameron',
 'salles_diffusion': [{'cinema_id': ObjectId('60527b186168afabf7e0c0e3'),
                       'date_diffusion': datetime.datetime(2005, 7, 1, 0, 0),
                       'heure_diffusion': '21h10',
                       'nombre_entrees': 100.0,
                       'nombre_place': 100.0,
                       'num_salle': 2.0}],
 'titre': 'Titanic'}
'''

## Requête 5 : afficher le titre de chaque film suivi du nombre d'avis
pipeline = [
    {"$group": {"_id": "$film_id", "nombre_avis": {"$sum": 1}}},
    {"$lookup": {"from": "films", "localField": "_id", "foreignField": "_id", "as": "film"}},
    {"$unwind": "$film"},
    {"$project": {"_id": "$_id", "titre_film": "$film.titre", "nombre_avis": "$nombre_avis"}}
]

result = db.avis.aggregate(pipeline)
pprint("nombres d'avis par films : ")
for avis in result:
    print(f"{avis['titre_film']} - Nombre d'avis: {avis['nombre_avis']}")

## Résultats n°5
'''
"nombres d'avis par films : "
Fight Club - Nombre d'avis: 1
The Dark Knight - Nombre d'avis: 1
Titanic - Nombre d'avis: 2
Pulp Fiction - Nombre d'avis: 2
Inception - Nombre d'avis: 1
The Shawshank Redemption - Nombre d'avis: 2
Forrest Gump - Nombre d'avis: 1
'''    

## Requête n°6 : afficher le pourcentage d'occupation de chaque salle 
pipeline = [
    {"$unwind": "$salles_diffusion"},  # Dérouler les salles de diffusion pour chaque film
    {"$group": {"_id": "$salles_diffusion.num_salle", 
                "total_entrees": {"$sum": "$salles_diffusion.nombre_entrees"},
                "nombre_places": {"$sum": "$salles_diffusion.nombre_place"}}},  
    {"$project": {"_id": 0, "num_salle": "$_id", 
                  "total_entrees": 1, "nombre_places": 1}},  
]

result = db.films.aggregate(pipeline)

# Affichage du pourcentage d'occupation de chaque salle
print("Pourcentage d'occupation de chaque salle :")
for entry in result:
    pourcentage = (entry["total_entrees"] / entry["nombre_places"]) * 100
    print(f"Salle {entry['num_salle']:.0f}: {pourcentage:.2f}%")

## Résultats n°6
'''
Pourcentage d'occupation de chaque salle :
Salle 3: 72.00%
Salle 2: 93.00%
Salle 1: 80.00%
Salle 26: 90.00%
Salle 17: 92.00%
'''


## Requête n°7 : Top N des films par note moyenne
N = 5
pipeline_top_movies = [
    {"$group": {"_id": "$film_id", "note_moyenne": {"$avg": "$note"}}},
    {"$sort": {"note_moyenne": -1}},
    {"$limit": N},
    {"$lookup": {"from": "films", "localField": "_id", "foreignField": "_id", "as": "film"}},
    {"$unwind": "$film"},
    {"$project": {"_id": "$_id", "titre": "$film.titre", "note_moyenne": "$note_moyenne"}}
]

result_top_movies = db.avis.aggregate(pipeline_top_movies)
print("Top", N, "films par note moyenne :")
for movie in result_top_movies:
    print(f"{movie['titre']}: {movie['note_moyenne']:.2f}")
    
## résultats n°7
'''
Top 5 films par note moyenne :
Titanic: 5.00
Fight Club: 4.90
The Dark Knight: 4.90
Pulp Fiction: 4.85
The Shawshank Redemption: 4.80
'''

## Requête n°8 : Utilisateurs les plus actifs par nombre de critiques
N_utilisateurs_actifs = 5
pipeline_utilisateurs_actifs = [
    {"$group": {"_id": "$nom_utilisateur", "total_critiques": {"$sum": 1}}},
    {"$sort": {"total_critiques": -1}},
    {"$limit": N_utilisateurs_actifs}
]

result_utilisateurs_actifs = db.avis.aggregate(pipeline_utilisateurs_actifs)
print("Top", N_utilisateurs_actifs, "utilisateurs les plus actifs par nombre de critiques :")
for user in result_utilisateurs_actifs:
    print(f"{user['_id']}: {user['total_critiques']} critiques")

## resultats n°8
'''
Top 5 utilisateurs les plus actifs par nombre de critiques :
alex: 1 critiques
théo: 1 critiques
maxime: 1 critiques
adam: 1 critiques
kevin: 1 critiques
'''

# Requête n°9 : Note moyenne au fil du temps
pipeline_note_temps = [
    {"$group": {"_id": {"$year": "$date_commentaire"}, "note_moyenne": {"$avg": "$note"}}},
    {"$sort": {"_id": 1}}
]

result_note_temps = db.avis.aggregate(pipeline_note_temps)
print("Note moyenne au fil du temps :")
for année_note in result_note_temps:
    print(f"Année: {année_note['_id']}, Note moyenne: {année_note['note_moyenne']:.2f}")

# résultat n°9
'''
Note moyenne au fil du temps :
Année: 2010, Note moyenne: 4.90
Année: 2011, Note moyenne: 5.00
Année: 2012, Note moyenne: 4.70
Année: 2013, Note moyenne: 4.80
Année: 2014, Note moyenne: 4.80
Année: 2015, Note moyenne: 4.90
Année: 2016, Note moyenne: 4.90
Année: 2017, Note moyenne: 5.00
Année: 2018, Note moyenne: 4.90
Année: 2023, Note moyenne: 4.80
'''

    
