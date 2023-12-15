TD n°1


Fonctionnalités :


* Lister les films
* Ajouter un film ( si utilisateur connecté)
* Consulter ces film ( si utilisateur connecté)
* Modifier les informations d’un film ( si utilisateur connecté) !!
* Supprimer un film ( si on est propriétaire du film )
* Gérer les formats physiques et numériques
* Utilisateur spécifie si un film est sous format physique/numérique
* Rechercher un film par titre, genre, réalisateur etc …
* Mettre un avis sur les films
* Partager le film
* Noter un film
* Rendre le film privé ou publique
* Statistiques de la vidéothèque: Fournit des statistiques telles que le nombre total de films, la répartition par genre, les films les mieux notés, etc.
* Filtrage parental: Intègre des fonctionnalités de filtrage parental pour restreindre l'accès à certains films en fonction de leur classification d'âge.
* Middleware Service d'authentification
* Gate pour gérer l’accès
* Intégration d’une API externe, qui permet d’ajouter un film plus rapidement (TMDB Movies https://developer.themoviedb.org/reference/intro/getting-started ou IMDB https://www.imdb.com/  )




Acteurs & schéma général :


* Administrateur :
* gérer les utilisateurs et visiteurs et les back office
* autoriser les accès aux films
* ajouter des films
* supprimer des films
* modifier un film
* s’authentifier
* Utilisateur :
* voir la liste des films
* consulter des films
* mettre un avis
* s’authentifier


* Visiteur:
* voir la liste des films qui sont publiques
* s’enregistrer

Données du système :


* les objets exploités par le système


* Films :
* title: string
* Director : string
* Main actors : liste de string
* Genre: string
* Année de sortie : entier
* Pays d’origine : String
* Durée : entier
* Langue : string
* Format : énumération (numérique, DVD, Blu-ray)
* isPublic : boolean
* Note : clé étrangère avec une table note
* Commentaires : clé étrangères vers une table comments
* idUtilisateur : propriétaire du film
* LocalisationFilm : String (dire où se trouve mon film)
* Synopsis du film : String
* Résumé : String


* Utilisateurs :
* pseudo : string
* age : int (pour vérifier l'âge pour regarder certain film 🔞)
* email : string
* password : string
* nom : string
* prenom : string
* droit : int (public/privé)
* TypeFilm : liste de string ( peut aussi choisir parmi un liste existante )

\*



Modèle d’exécution et échanges

Utilisateur recherche un film -> Système renvoie les résultats

Utilisateur ajout un film -> Système renvoie un message de confirmation d’ajout


























Architecture :






Architecture de l’API REST :

Opérations sur les Films :

GET /films : Récupérer la liste complète des films.

GET /films/{id} : Récupérer les détails d'un film spécifique.

POST /films/add : Ajouter un nouveau film.

PUT /films/edit{id} : Mettre à jour les informations d'un film existant.

DELETE /films/{id} : Supprimer un film

GET /films/search/{key} : Rechercher un film

POST /films/add/{id}/comments/ : Ajouter un commentaire

POST /films/add/{id}/rating/ : Ajouter une note




Opérations sur les utilisateurs :

GET /users : Récupérer la liste complète des utilisateurs

GET /users/{id} : Récupérer les détails d'un utilisateur spécifique

POST /users/add/ : Ajouter un nouvel utilisateur

PUT /users/edit/{id} : Mettre à jour les informations d'un utilisateur existant

DELETE /users/delete/{id} : Supprimer un utilisateur


token Authorization à mettre pour certaine route
