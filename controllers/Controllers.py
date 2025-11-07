import json
from pathlib import Path
from PySide6.QtCore import QDate
from PySide6.QtWidgets import QMessageBox

FICHIER_DONNEES = Path(__file__).parent.parent / "data" / "tasks.json"

class ControleurTaches:
    def __init__(self, parent=None):
        self.taches = []
        self.parent = parent
        self.charger_taches()

    def charger_taches(self):
        if not FICHIER_DONNEES.exists():
            self.taches = []
            return
        try:
            with open(FICHIER_DONNEES, "r", encoding="utf-8") as f:
                self.taches = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self.taches = []
            if self.parent:
                QMessageBox.warning(self.parent, "Erreur", "Le fichier de données est corrompu.")

    def sauvegarder_taches(self):
        FICHIER_DONNEES.parent.mkdir(parents=True, exist_ok=True)
        with open(FICHIER_DONNEES, "w", encoding="utf-8") as f:
            json.dump(self.taches, f, indent=4, ensure_ascii=False)

    def ajouter_tache(self, tache):
        tache["date_creation"] = QDate.currentDate().toString("yyyy-MM-dd")
        if "commentaires" not in tache:
            tache["commentaires"] = []
        self.taches.append(tache)
        self.sauvegarder_taches()

    def modifier_tache(self, index, tache):
        ancienne_tache = self.taches[index]
        tache["date_creation"] = ancienne_tache.get("date_creation", QDate.currentDate().toString("yyyy-MM-dd"))
        if "commentaires" not in tache:
            tache["commentaires"] = ancienne_tache.get("commentaires", [])
        self.taches[index] = tache
        self.sauvegarder_taches()

    def supprimer_tache(self, index):
        if 0 <= index < len(self.taches):
            del self.taches[index]
            self.sauvegarder_taches()

    def obtenir_tache_par_titre(self, titre):
        for i, t in enumerate(self.taches):
            if t["titre"] == titre:
                return i, t
        return None, None

   
   
   
    def ajouter_commentaire(self, index, texte):
        if 0 <= index < len(self.taches):
            date_str = QDate.currentDate().toString("yyyy-MM-dd")
            if "commentaires" not in self.taches[index]:
                self.taches[index]["commentaires"] = []
            self.taches[index]["commentaires"].append({"date": date_str, "texte": texte})
            self.sauvegarder_taches()

    def supprimer_commentaire(self, index_tache, index_commentaire):
        if 0 <= index_tache < len(self.taches):
            commentaires = self.taches[index_tache].get("commentaires", [])
            if 0 <= index_commentaire < len(commentaires):
                del commentaires[index_commentaire]
                self.sauvegarder_taches()

    def definir_etat_tache(self, index, etat):
        if 0 <= index < len(self.taches):
            self.taches[index]["etat"] = etat
            if etat == "Réalisé":
                self.taches[index]["date_fin"] = QDate.currentDate().toString("yyyy-MM-dd")
            self.sauvegarder_taches()

  
    def taches_triees(self, tri_date=False):
        if tri_date:
            return sorted(self.taches, key=lambda t: t.get("date_creation", ""))
        return self.taches

    def filtrer_taches(self, filtre_titre="", filtre_etat="Tous", tri_date=False):
        taches = self.taches_triees(tri_date)
        return [
            t for t in taches
            if filtre_titre.lower() in t["titre"].lower() and (filtre_etat == "Tous" or t["etat"] == filtre_etat)
        ]
