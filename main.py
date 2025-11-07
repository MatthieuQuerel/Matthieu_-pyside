import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QPushButton, QComboBox, QDateEdit, QCheckBox, QMessageBox
)
from PySide6.QtCore import QDate
from controllers.Controllers import ControleurTaches

class FenetrePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion de tâches")
        self.controleur = ControleurTaches(parent=self)
        self.index_tache_courante = None

        central = QWidget(self)
        self.setCentralWidget(central)
        v = QVBoxLayout(central)

        # --- Barre de recherche et filtres ---
        self.champ_recherche = QLineEdit()
        self.champ_recherche.setPlaceholderText("Rechercher une tâche...")
        self.bouton_rechercher = QPushButton("Rechercher")
        self.combo_etat_filtre = QComboBox()
        self.combo_etat_filtre.addItem("Tous")
        self.combo_etat_filtre.addItems(["À faire", "En cours", "Réalisé", "Abandonné", "En attente"])
        self.bouton_ajouter = QPushButton("Ajouter")
        self.bouton_supprimer = QPushButton("Supprimer")

        top = QHBoxLayout()
        top.addWidget(QLabel("Recherche:"))
        top.addWidget(self.champ_recherche)
        top.addWidget(QLabel("Filtrer par état:"))
        top.addWidget(self.combo_etat_filtre)
        top.addWidget(self.bouton_rechercher)

        btn_row = QHBoxLayout()
        btn_row.addWidget(self.bouton_ajouter)
        btn_row.addWidget(self.bouton_supprimer)

        self.liste_taches = QListWidget()
        self.check_trier_date = QCheckBox("Trier par date de création (croissant)")

        # --- Formulaire ---
        self.champ_titre = QLineEdit()
        self.champ_description = QLineEdit()
        self.date_debut = QDateEdit()
        self.date_debut.setDate(QDate.currentDate())
        self.date_fin = QDateEdit()
        self.date_fin.setDate(QDate.currentDate())
        self.combo_etat = QComboBox()
        self.combo_etat.addItems(["À faire", "En cours", "Réalisé", "Abandonné", "En attente"])
        self.check_cloturer = QCheckBox("Clôturer")
        self.champ_commentaire = QLineEdit()
        self.bouton_ajouter_commentaire = QPushButton("Ajouter commentaire")
        self.liste_commentaires = QListWidget()
        self.bouton_supprimer_commentaire = QPushButton("Supprimer commentaire")
        self.bouton_valider = QPushButton("Valider")

        form = QVBoxLayout()
        form.addWidget(QLabel("Titre :"))
        form.addWidget(self.champ_titre)
        form.addWidget(QLabel("Description :"))
        form.addWidget(self.champ_description)
        form.addWidget(QLabel("Date début :"))
        form.addWidget(self.date_debut)
        form.addWidget(QLabel("Date fin :"))
        form.addWidget(self.date_fin)
        form.addWidget(QLabel("État :"))
        form.addWidget(self.combo_etat)
        form.addWidget(self.check_cloturer)
        form.addWidget(QLabel("Commentaire :"))
        form.addWidget(self.champ_commentaire)
        form.addWidget(self.bouton_ajouter_commentaire)
        form.addWidget(self.liste_commentaires)
        form.addWidget(self.bouton_supprimer_commentaire)
        form.addWidget(self.bouton_valider)

        # --- Assemblage principal ---
        v.addLayout(top)
        v.addLayout(btn_row)
        v.addWidget(self.check_trier_date)
        v.addWidget(self.liste_taches)
        v.addLayout(form)

        # --- Connexions ---
        self.bouton_rechercher.clicked.connect(self.actualiser_liste)
        self.champ_recherche.returnPressed.connect(self.actualiser_liste)
        self.bouton_ajouter.clicked.connect(self.ouvrir_nouvelle_tache)
        self.bouton_supprimer.clicked.connect(self.confirmer_supprimer_tache)
        self.bouton_valider.clicked.connect(self.confirmer_valider_tache)
        self.liste_taches.itemClicked.connect(self.charger_tache)
        self.bouton_ajouter_commentaire.clicked.connect(self.ajouter_commentaire)
        self.bouton_supprimer_commentaire.clicked.connect(self.confirmer_supprimer_commentaire)
        self.combo_etat_filtre.currentTextChanged.connect(self.actualiser_liste)
        self.check_cloturer.stateChanged.connect(self.changement_etat_cloture)
        self.check_trier_date.stateChanged.connect(self.actualiser_liste)

        self.actualiser_liste()

    # --- Méthodes ---
    def actualiser_liste(self):
        self.liste_taches.clear()
        filtre_titre = self.champ_recherche.text().strip()
        filtre_etat = self.combo_etat_filtre.currentText()
        taches = self.controleur.filtrer_taches(filtre_titre, filtre_etat, self.check_trier_date.isChecked())
        for t in taches:
            self.liste_taches.addItem(t["titre"])

    def ouvrir_nouvelle_tache(self):
        self.index_tache_courante = None
        self.champ_titre.clear()
        self.champ_description.clear()
        self.date_debut.setDate(QDate.currentDate())
        self.date_fin.setDate(QDate.currentDate())
        self.combo_etat.setCurrentIndex(0)
        self.liste_commentaires.clear()
        self.champ_commentaire.clear()
        self.check_cloturer.setChecked(False)

    def charger_tache(self, item):
        index, tache = self.controleur.obtenir_tache_par_titre(item.text())
        if tache:
            self.index_tache_courante = index
            self.champ_titre.setText(tache["titre"])
            self.champ_description.setText(tache["description"])
            self.date_debut.setDate(QDate.fromString(tache["date_debut"], "yyyy-MM-dd"))
            self.date_fin.setDate(QDate.fromString(tache["date_fin"], "yyyy-MM-dd"))
            self.combo_etat.setCurrentText(tache["etat"])
            self.check_cloturer.blockSignals(True)
            self.check_cloturer.setChecked(tache["etat"] == "Réalisé")
            self.check_cloturer.blockSignals(False)
            self.liste_commentaires.clear()
            for c in tache.get("commentaires", []):
                self.liste_commentaires.addItem(f"{c['date']} → {c['texte']}")

    # --- Valider tâche ---
    def confirmer_valider_tache(self):
        reply = QMessageBox.question(
            self, "Valider la tâche", "Voulez-vous vraiment valider cette tâche ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.valider_tache()

    def valider_tache(self):
        titre = self.champ_titre.text().strip()
        if not titre:
            QMessageBox.warning(self, "Erreur", "Le titre est obligatoire.")
            return

        etat_final = "Réalisé" if self.check_cloturer.isChecked() else self.combo_etat.currentText()

        # Récupérer les commentaires
        commentaires = []
        for i in range(self.liste_commentaires.count()):
            texte_complet = self.liste_commentaires.item(i).text()
            if "→" in texte_complet:
                date_str, texte = texte_complet.split("→", 1)
                commentaires.append({"date": date_str.strip(), "texte": texte.strip()})

        tache = {
            "titre": titre,
            "description": self.champ_description.text().strip(),
            "date_debut": self.date_debut.date().toString("yyyy-MM-dd"),
            "date_fin": self.date_fin.date().toString("yyyy-MM-dd"),
            "etat": etat_final,
            "commentaires": commentaires
        }

        if self.index_tache_courante is not None:
            self.controleur.modifier_tache(self.index_tache_courante, tache)
        else:
            self.controleur.ajouter_tache(tache)

        self.actualiser_liste()
        self.ouvrir_nouvelle_tache()

    # --- Supprimer commentaire ---
    def confirmer_supprimer_commentaire(self):
        index_commentaire = self.liste_commentaires.currentRow()
        if index_commentaire < 0:
            return
        reply = QMessageBox.question(
            self, "Supprimer commentaire", "Voulez-vous vraiment supprimer ce commentaire ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.supprimer_commentaire()

    def supprimer_commentaire(self):
        index_tache = self.index_tache_courante
        index_commentaire = self.liste_commentaires.currentRow()
        if index_tache is not None and index_commentaire >= 0:
            self.controleur.supprimer_commentaire(index_tache, index_commentaire)
            self.charger_tache(self.liste_taches.currentItem())
        elif index_tache is None and index_commentaire >= 0:
            self.liste_commentaires.takeItem(index_commentaire)

    # --- Supprimer tâche ---
    def confirmer_supprimer_tache(self):
        item = self.liste_taches.currentItem()
        if item:
            reply = QMessageBox.question(
                self, "Supprimer la tâche", "Voulez-vous vraiment supprimer cette tâche ?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                index, _ = self.controleur.obtenir_tache_par_titre(item.text())
                if index is not None:
                    self.controleur.supprimer_tache(index)
                    self.actualiser_liste()
                    self.ouvrir_nouvelle_tache()

    # --- Changement état Clôturer ---
    def changement_etat_cloture(self):
        if self.index_tache_courante is None:
            return
        if self.check_cloturer.isChecked():
            reply = QMessageBox.question(
                self, "Clôturer", "Voulez-vous vraiment clôturer la tâche ?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.controleur.definir_etat_tache(self.index_tache_courante, "Réalisé")
                self.charger_tache(self.liste_taches.currentItem())
            else:
                self.check_cloturer.setChecked(False)
        else:
            self.controleur.definir_etat_tache(self.index_tache_courante, "En cours")
            self.charger_tache(self.liste_taches.currentItem())

    # --- Ajouter commentaire directement ---
    def ajouter_commentaire(self):
        commentaire = self.champ_commentaire.text().strip()
        if not commentaire:
            QMessageBox.warning(
                self,
                "Erreur",
                "Le champ de commentaire ne peut pas être vide.\nVeuillez entrer un texte avant d’ajouter un commentaire."
            )
            return
        date_str = QDate.currentDate().toString("yyyy-MM-dd")
        texte_affiche = f"{date_str} → {commentaire}"

        # Affichage immédiat
        self.liste_commentaires.addItem(texte_affiche)

        # Ajout dans le contrôleur si tâche existante
        if self.index_tache_courante is not None:
            self.controleur.ajouter_commentaire(self.index_tache_courante, commentaire)

        self.champ_commentaire.clear()

def main():
    app = QApplication(sys.argv)
    fenetre = FenetrePrincipale()
    fenetre.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
