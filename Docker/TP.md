\# TP de RT 0704 : un gestionnaire de vidéothèque

\## Mise en place d\'éléments de l\'infrastructure

1\. Rejoignez le lab \*M1RT RT0704 TP\* sur la pletforme RemoteLabz 2.
Installez VSCode sur votre machine physique 3. Installez le module
\*remote development\* de VSCode si nécessaire 4. Mettez en place un
échange de clé RSA entre la machine physique et la machine virtuelle 5.
Connectez vous depuis VSCode à la machine virtuelle 6. Vérifiez
l\'installation des éléments suivants :  - docker, docker-compose  - git
7. Créez deux projets VSCode et GIT :  - serveur, qui portera le code du
tiers de présentation  - API, qui portera le tiers d\'accès aux données
(l\'API REST + le fichier JSON)

\## Développement

dans cetta partie, vous mettrez en place deux conteneurs contenant
python et Flask.

\### Création et test des conteneurs Flask

Créez une image docker utilisateur contenant les éléments suivants : -
Python 3 - Flask - l\'architecture de répertoires nécessaires à
l\'exécution d\'une application Flask, application dans un volume
partagé avec l\'hôte Docker.

Vous utiliserez l\'image de base que vous souhaitez.

Testez votre conteneur en développant : - une page HTML simple - Une
page HTML contenant un forumlaire et une page de straiteemnt de ce
formulaire en python / JINJA - un page HTML contenant un template JINJA
qui exploitera des données issues d\'une fichier contenant des données
JSON, le fichier vidéothèque par exemple

\### Création du tiers de données

En reprenant l\'API REST que vous avez définie durant le TD, proposez
une implémentation de l\'ensemble des différentes fonctions. Comme
précisé durant le TD, l\'ensemble des données qui transitent entre le
client et le serveur sont au format JSON.

Vous exécuterez le serveur Flask portant l\'API REST dans le conteneur
instanciant l\'image précédemment créée.

Testez l\'ensemble des fonctions écrites, soit à l\'aide d\'un outil de
type \*postman\* ou \*rested\*, soit depuis un script python, soit en
testant le programme depuis une commande curl.

Le fichier de la vidéothèque pourra être créé manuellement, ou à l\'aide
d\'une fonction exploitant des appels externes.

\### Création du tiers de présentation

Dans cette partie, codez l\'ensemble des pages que vous avez définies
dans le TD, et créez ces différentes pages

Vous exécuterez le serveur Flask portant le servuer WEB dans le
conteneur instanciant l\'image précédemment créée.

Vous effectuerez une création coordonnée des deux conteneurs.
