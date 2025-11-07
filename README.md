#  Application de Gestion de Tâches – Architecture MVC (PySide6)

Une application graphique en Python (PySide6) permettant de gérer des tâches, d’ajouter des commentaires, et de clôturer les activités réalisées.  
Les données sont stockées en JSON pour assurer la simplicité.

---

##  Architecture MVC

###  Description du modèle MVC appliqué

L’application suit le modèle MVC (Modèle - Vue - Contrôleur) afin de séparer la logique, les données et la présentation : 

---

###  Role du découpage choisi

- La séparation MVC rend le code plus lisible, modulaire et facile à maintenir.  
- On peut modifier l’interface sans toucher à la logique métier.  
- Le Contrôleur isole les actions et simplifie la gestion des événements.  
- Le Modèle  est facilement remplaçable (par exemple, passer de JSON à SQLite sans impacter la Vue) 

---
### Justification du découpage choisi
Dans mon cas, je n’ai pas forcément besoin d’un dossier Modèle pour un petit projet comme celui-ci. C’est pour cela que j’ai un dossier data avec mon fichier JSON, ce qui fera complètement l’affaire. mais à coté j'ai bien controlleurs et views
## Organisation des fichiers
```
gestion_taches/
├─ views/
│ └─ ui_interface.py  # C’est un fichier Python généré de untitled.ui
│ └─ untitled.ui # C’est un fichier généré par Qt Designer
│ └─  style.qss # Pour le style de la page
├─ controllers/
│ └─ ControleurTaches.py # Contient la classe TaskController
├─ data/
│ └─ tasks.json # Fichier de stockage des tâches 
├─ main.py # Fichier principal, gère la fenêtre et la Vue 
└─ README.md # Documentation du projet
```
## Choix techniques

### Stockage des données

- **Format choisi : JSON**  
  Le JSON est simple, léger, portable et facilement modifiable.  
  Il se situe dans `data/tasks.json`.

### Représentation des tâches et commentaires

```json
{
  "titre": "Faire la lessive",
  "description": "Lancer la machine à laver avant midi",
  "date_debut": "2025-10-28",
  "date_fin": "2025-10-29",
  "etat": "En cours",
  "commentaires": [
    { "date": "2025-10-28 10:30", "texte": "Machine prête à lancer." }
  ],
  "date_creation": "2025-10-25"
}
```


## Gestion des relations

 - Une tâche peut contenir plusieurs commentaires.

 - Les commentaires sont intégrés directement dans la tâche sous forme de liste.

### Fonctionnement de la clôture

- Si l’utilisateur coche “Clôturer”, l’état passe automatiquement à “Réalisé”.

- Une confirmation s’affiche avant de modifier l’état. la date de fin ce mets à aujourd'hui

- Si on décoche, la tâche repasse en “En cours”.

## Validation et gestion des erreurs

Titre obligatoire : un message d’erreur s’affiche si le champ est vide.

Dates valides : le format est contrôlé via les widgets QDateEdit.

État cohérent : si la tâche est clôturée, l’état devient “Réalisé”.

Commentaires vides interdits : on ne peut pas ajouter un commentaire vide.

## Gestion des erreurs

Utilisation de QMessageBox pour informer l’utilisateur : Erreur de type messages dans les erreur de validation le bute est pas de bloqué l'utilisateur mais de l'informée par exaple il  ne peut pas valider une tache si il y a pas de titre donc un message d erreur non bloquant

### Interface utilisateur
## Principes de conception

## Navigation et filtres

- Une seule page, car je trouve que ce type d’application ne nécessite pas forcément une navigation ; je trouve même cela plus simple avec une seule page.

- Recherche par titre

- Filtre par état (À faire, En cours, Réalisé, etc.)

- Tri par date de création

## Gestion des commentaires

Ajout via un champ bouton “Ajouter commentaire”

Suppression par sélection dans la liste

Enregistrement automatique dans le JSON

## Gestion de la clôture

Coche “Clôturer” => message de confirmation

Passage automatique à “Réalisé”

Décochement = retour à “En cours”

pour tout action suur les bouton une confirmation est nessesaire 

## Difficultés rencontrées et solutions

- Les dificulté sont les parties styles
  j’ai consulté la documentation.

- Une autre difficulté concernait la compréhension du langage.
Pour les surmonter, j’ai consulté la documentation.

- Le coche "Clôturer" ne restait pas cochée	
Ajout du blocage avec(blockSignals(True/False)) pour éviter les boucles.

- Les commentaires n’apparaissaient pas après rechargement.

- Le tri ne fonctionnait pas correctement	
Mise en place d’un tri basé sur la date de création enregistrée dans le modèle.

## Ce que j’aurais fait différemment avec plus de temp
- Ajout d’une base SQL pour des recherches plus rapides et plus robustes.

- Création d’un système d’authentification pour gérer plusieurs utilisateurs.

- Ajout d’un système de notifications ou de rappels de tâches.

# Guide d’installation et d’exécution
 ## Cloner le projet
 ```
git clone https://github.com/MatthieuQuerel/Matthieu_-pyside.git
```

 ## Créer un environnement virtuel
 ```
python -m venv venv
```

 ## Activer l’environnement virtuel
Sous Windows :
```
venv\Scripts\activate
```

## Sous macOS / Linux :
```
source venv/bin/activate
```

## Installer les dépendances
```
pip install PySide6
```

## Lancer le programme
```
python main.py
```