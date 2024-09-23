from . import db
from datetime import datetime

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(50))
    nom = db.Column(db.String(50))
    mot_de_passe = db.Column(db.String(255))
    role = db.Column(db.Enum('super_admin', 'gerant', 'enseignant', 'eleve', name='user_role_enum'))
    email = db.Column(db.String(100))

class Calendrier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(255))
    debut = db.Column(db.DateTime)
    fin = db.Column(db.DateTime)

class Etablissement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    adresse = db.Column(db.String(255))

class GerantEtablissement(db.Model):
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), primary_key=True)
    etablissement_id = db.Column(db.Integer, db.ForeignKey('etablissement.id'))
    email = db.Column(db.String(100))

class Classe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(50))
    serie = db.Column(db.String(50))  # Peut être vide pour l'enseignement général

class Metier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(100))

class Eleve(db.Model):
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), primary_key=True)
    matricule = db.Column(db.String(20))
    date_naissance = db.Column(db.Date)
    metier_id = db.Column(db.Integer, db.ForeignKey('metier.id'))

class Inscription(db.Model):
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleve.utilisateur_id'), primary_key=True)
    classe_id = db.Column(db.Integer, db.ForeignKey('classe.id'), primary_key=True)
    etablissement_id = db.Column(db.Integer, db.ForeignKey('etablissement.id'), primary_key=True)
    calendrier_id = db.Column(db.Integer, db.ForeignKey('calendrier.id'), primary_key=True)

class Enseignant(db.Model):
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), primary_key=True)
    matricule = db.Column(db.String(20))
    date_naissance = db.Column(db.Date)

class Matiere(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(100))

class MetierMatiere(db.Model):
    metier_id = db.Column(db.Integer, db.ForeignKey('metier.id'), primary_key=True)
    matiere_id = db.Column(db.Integer, db.ForeignKey('matiere.id'), primary_key=True)
    coefficient = db.Column(db.Float)

class Enseigner(db.Model):
    enseignant_id = db.Column(db.Integer, db.ForeignKey('enseignant.utilisateur_id'), primary_key=True)
    etablissement_id = db.Column(db.Integer, db.ForeignKey('etablissement.id'), primary_key=True)
    matiere_id = db.Column(db.Integer, db.ForeignKey('matiere.id'), primary_key=True)
    classe_id = db.Column(db.Integer, db.ForeignKey('classe.id'), primary_key=True)
    calendrier_id = db.Column(db.Integer, db.ForeignKey('calendrier.id'), primary_key=True)

class Note(db.Model):
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleve.utilisateur_id'), primary_key=True)
    matiere_id = db.Column(db.Integer, db.ForeignKey('matiere.id'), primary_key=True)
    calendrier_id = db.Column(db.Integer, db.ForeignKey('calendrier.id'), primary_key=True)
    semestre = db.Column(db.Enum('1', '2', name='semestre_enum'), primary_key=True)
    note_cc1 = db.Column(db.Float)
    note_cc2 = db.Column(db.Float)
    note_composition = db.Column(db.Float)

class AppreciationCompetenceSpecifique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleve.utilisateur_id'), primary_key=True)
    competence_id = db.Column(db.Integer, db.ForeignKey('competence_specifique.id'), primary_key=True)
    calendrier_id = db.Column(db.Integer, db.ForeignKey('calendrier.id'), primary_key=True)
    semestre = db.Column(db.Enum('1', '2', name='semestre_enum'), primary_key=True)

class AppreciationCompetenceComportementale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleve.utilisateur_id'), primary_key=True)
    competence_id = db.Column(db.Integer, db.ForeignKey('competence_comportementale.id'), primary_key=True)
    calendrier_id = db.Column(db.Integer, db.ForeignKey('calendrier.id'), primary_key=True)
    semestre = db.Column(db.Enum('1', '2', name='semestre_enum'), primary_key=True)

class AppreciationAptitude(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleve.utilisateur_id'), primary_key=True)
    aptitude_id = db.Column(db.Integer, db.ForeignKey('aptitude.id'), primary_key=True)
    calendrier_id = db.Column(db.Integer, db.ForeignKey('calendrier.id'), primary_key=True)
    semestre = db.Column(db.Enum('1', '2', name='semestre_enum'), primary_key=True)

class InteretEleve(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleve.utilisateur_id'))
    interet_id = db.Column(db.Integer, db.ForeignKey('interet.id'))

class Commentaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(20))

class CompetenceSpecifique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(30))

class CompetenceComportementale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(30))

class Aptitude(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(30))

class Interet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(30))

class Ressource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(255))
    url = db.Column(db.String(255))
    matiere_id = db.Column(db.Integer, db.ForeignKey('matiere.id'))