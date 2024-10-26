from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint
from datetime import datetime


#connexion au serveur mongo2
c=MongoClient("mongo2.iem",port=27017,username="fe874388",password="fe874388",authSource="fe874388",authMechanism="SCRAM-SHA-1")

#recuperation de la base de donnees
db=c.fe874388

#recuperer toutes les collections
films = db.films.find()
cinemas = db.cinemas.find()
avis_films = db.avis.find()


# Requête 1 : afficher le nombre total des gens qui sont entrees au film The Dark Knight 
result = db.films.find_one({"titre": "The Dark Knight"})

somme=0
for doc in result["salles_diffusion"]:
    somme += doc["nombre_entrees"]

pprint("le total d'entrees du film The Dark Knight : " + str(somme))

# Resultats 1
'''
"le total d'entrees du film The Dark Knight : 510.0"
'''


# Requête 2 : afficher la liste des films realises par Christopher Nolan
result2 = db.films.find({"realisateur": "Christopher Nolan"})

pprint("la liste des films realises par Christopher Nolan : ")
for film in result2:
    pprint(film["titre"])

# Resultats 2
'''
la liste des films realises par Christopher Nolan : '
'Inception'
'The Dark Knight'
'''

# Requête 3 : afficher le titre du film qui a les meilleurs avis sur internet
moyennes_notes = {}
# Boucle pour calculer la somme des notes et le nombre d'avis pour chaque film
for avis in avis_films:
    film_id = avis["film_id"]
    note = avis["note"]
    # Si le film_id n'est pas dejà dans le dictionnaire, l'initialiser avec une somme de 0 et un nombre d'avis de 0
    if film_id not in moyennes_notes:
        moyennes_notes[film_id] = {"somme_notes": 0, "nombre_avis": 0}
    # Ajouter la note à la somme des notes pour ce film et incrementer le nombre d'avis
    moyennes_notes[film_id]["somme_notes"] += note
    moyennes_notes[film_id]["nombre_avis"] += 1

max_notes=0
# Boucle pour calculer la moyenne des notes pour chaque film
for film_id, info_notes in moyennes_notes.items():
    moyenne = info_notes["somme_notes"] / info_notes["nombre_avis"]
    if max_notes<moyenne:
        max_notes=moyenne
        id = film_id

film = db.films.find_one({"_id":id},{ "_id":0, "titre":1})

pprint(f"le titre du film qui a les meilleurs avis sur internet est : {film['titre']}")

# Resultats 3
'''
'le titre du film qui a les meilleurs avis sur internet est : Titanic'
'''


# Requête 4 : afficher tous les avis pour le film Titanic
pprint("tous les avis pour le film Titanic : ")
film = db.films.find_one({"_id":ObjectId("60527b186168afabf7e0c0e2")})
result = db.avis.find({"film_id": film["_id"]})
for avis in result:
    pprint(avis)

# Resultats 4
'''
'tous les avis pour le film Titanic : '
{'_id': ObjectId('65f6ccf30d6c607d7126f655'),
 'commentaire': "Un chef-d'œuvre absolu !",
 'date_commentaire': datetime.datetime(2011, 1, 7, 0, 0),
 'film_id': ObjectId('60527b186168afabf7e0c0e2'),
 'nom_utilisateur': 'kevin',
 'note': 5.0,
 'reseau_social': 'Facebook'}
{'_id': ObjectId('65f6ccf30d6c607d7126f65b'),
 'commentaire': 'Une experience cinematographique revolutionnaire !',
 'date_commentaire': datetime.datetime(2017, 5, 18, 0, 0),
 'film_id': ObjectId('60527b186168afabf7e0c0e2'),
 'nom_utilisateur': 'adam',
 'note': 5.0,
 'reseau_social': 'Facebook'}
'''
    
# Requête 5 : afficher le nombre de tickets vendus par mois 
# Initialiser une liste pour stocker les ventes par mois
ventes_par_mois = [0] * 12

# Parcourir tous les documents dans la collection "films"
for film in db.films.find():
    for salle in film["salles_diffusion"]:
        date_diffusion = salle["date_diffusion"]
        if date_diffusion.month in range(1, 13):  # Verifier si le mois est valide (entre 1 et 12)
            mois = date_diffusion.month
            ventes_par_mois[mois - 1] += salle["nombre_entrees"]  # Soustraire 1 car les indices de liste commencent à 0
            

pprint("Tous les tickets vendus par mois : ")
# Afficher le total des ventes par mois
for i in range(1, 13):
    print(f"Mois {i} : {ventes_par_mois[i - 1]} tickets vendus")

# Resultats 5
'''
'Tous les tickets vendus par mois : '
Mois 1 : 0 tickets vendus
Mois 2 : 0 tickets vendus
Mois 3 : 0 tickets vendus
Mois 4 : 0 tickets vendus
Mois 5 : 0 tickets vendus
Mois 6 : 0 tickets vendus
Mois 7 : 1680.0 tickets vendus
Mois 8 : 0 tickets vendus
Mois 9 : 490.0 tickets vendus
Mois 10 : 720.0 tickets vendus
Mois 11 : 0 tickets vendus
Mois 12 : 0 tickets vendus
'''



# Requête 6 : Recherche des films diffusé à Lyon
#Recherche des cinemas à Lyon
cinemas_Lyon = db.cinemas.find({"ville": "Lyon"})

#Liste des IDs des cinemas à Lyon
ids_cinemas_Lyon = [cinema["_id"] for cinema in cinemas_Lyon]

#Recherche des films diffusés dans les cinemas à Lyon
films_Lyon = db.films.find({"salles_diffusion.cinema_id": {"$in": ids_cinemas_Lyon}})

print("les films qui ont ete diffuse à Lyon sont : ")
for film in films_Lyon:
    pprint(film)


# Resultats 6 
'''
{'_id': ObjectId('60527b186168afabf7e0c0e6'),
 'categorie': ['Drama', 'Romance'],
 'date_de_sortie': datetime.datetime(1994, 7, 6, 0, 0),
 'description': 'The presidencies of Kennedy and Johnson, Vietnam, Watergate, '
                'and other history unfold through the perspective of an '
                'Alabama man with an IQ of 75.',
 'duree': 142.0,
 'realisateur': 'Robert Zemeckis',
 'salles_diffusion': [{'cinema_id': ObjectId('60527b186168afabf7e0c0ea'),
                       'date_diffusion': datetime.datetime(1994, 7, 7, 0, 0),
                       'heure_diffusion': '18h30',
                       'nombre_entrees': 320.0,
                       'nombre_place': 350.0,
                       'num_salle': 1.0},
                      {'cinema_id': ObjectId('60527b186168afabf7e0c0ea'),
                       'date_diffusion': datetime.datetime(1994, 7, 8, 0, 0),
                       'heure_diffusion': '21h00',
                       'nombre_entrees': 370.0,
                       'nombre_place': 400.0,
                       'num_salle': 2.0}],
 'titre': 'Forrest Gump'}
'''
