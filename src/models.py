import bcrypt
from . import db
from datetime import datetime

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prenom = db.Column(db.String(50))
    nom = db.Column(db.String(50))
    mot_de_passe = db.Column(db.String(255))
    date_naissance = db.Column(db.Date)
    adresse = db.Column(db.String(255))
    role = db.Column(db.Enum('super_admin', 'gerant', 'enseignant', 'eleve', name='user_role_enum'))

    gerant = db.relationship('GerantEtablissement', backref='utilisateur', uselist=False)
    eleve = db.relationship('Eleve', backref='utilisateur', uselist=False)
    enseignant = db.relationship('Enseignant', backref='utilisateur', uselist=False)

    def set_password(self, password):
        self.mot_de_passe = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.mot_de_passe)

    def to_dict(self):
        return {
            'id': self.id,
            'prenom': self.prenom,
            'nom': self.nom,
            'date_naissance': self.date_naissance.isoformat() if self.date_naissance else None,
            'adresse': self.adresse,
            'role': str(self.role)
        }

class Calendrier(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titre = db.Column(db.String(255))
    debut = db.Column(db.DateTime)
    fin = db.Column(db.DateTime)

    inscriptions = db.relationship('Inscription', backref='calendrier')
    enseignements = db.relationship('Enseigner', backref='calendrier')
    notes = db.relationship('Note', backref='calendrier')
    appreciations_specifiques = db.relationship('AppreciationCompetenceSpecifique', backref='calendrier')
    appreciations_comportementales = db.relationship('AppreciationCompetenceComportementale', backref='calendrier')
    appreciations_aptitudes = db.relationship('AppreciationAptitude', backref='calendrier')

    def to_dict(self):
        return {
            'id': self.id,
            'titre': self.titre,
            'debut': self.debut.isoformat() if self.debut else None,
            'fin': self.fin.isoformat() if self.fin else None,
        }

class Etablissement(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100))
    adresse = db.Column(db.String(255))

    gerants = db.relationship('GerantEtablissement', backref='etablissement')
    enseignants = db.relationship('Enseignant', backref='etablissement')
    inscriptions = db.relationship('Inscription', backref='etablissement')
    enseignements = db.relationship('Enseigner', backref='etablissement')
    eleves = db.relationship('Eleve', backref='etablissement')

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'adresse': self.adresse,
        }

class GerantEtablissement(db.Model):
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), primary_key=True)
    etablissement_id = db.Column(db.Integer, db.ForeignKey('etablissement.id'))
    email = db.Column(db.String(100))

    def to_dict(self):
        return {
            'utilisateur_id': self.utilisateur_id,
            'etablissement_id': self.etablissement_id,
            'email': self.email,
        }

class Classe(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    libelle = db.Column(db.String(50))
    serie = db.Column(db.String(50))

    inscriptions = db.relationship('Inscription', backref='classe')
    enseignements = db.relationship('Enseigner', backref='classe')

    def to_dict(self):
        return {
            'id': self.id,
            'libelle': self.libelle,
            'serie': self.serie,
        }

class Metier(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    libelle = db.Column(db.String(100))

    eleves = db.relationship('Eleve', backref='metier')
    matieres = db.relationship('MetierMatiere', backref='metier')

    def to_dict(self):
        return {
            'id': self.id,
            'libelle': self.libelle,
        }

class Eleve(db.Model):
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), primary_key=True)
    matricule = db.Column(db.String(20))
    metier_id = db.Column(db.Integer, db.ForeignKey('metier.id'))
    etablissement_id = db.Column(db.Integer, db.ForeignKey('etablissement.id'))

    inscriptions = db.relationship('Inscription', backref='eleve')
    notes = db.relationship('Note', backref='eleve')
    interets = db.relationship('InteretEleve', backref='eleve')
    appreciations_specifiques = db.relationship('AppreciationCompetenceSpecifique', backref='eleve')
    appreciations_comportementales = db.relationship('AppreciationCompetenceComportementale', backref='eleve')
    appreciations_aptitudes = db.relationship('AppreciationAptitude', backref='eleve')

    def to_dict(self):
        return {
            'utilisateur_id': self.utilisateur_id,
            'matricule': self.matricule,
            'metier_id': self.metier_id,
        }

class Inscription(db.Model):
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleve.utilisateur_id'), primary_key=True)
    classe_id = db.Column(db.Integer, db.ForeignKey('classe.id'), primary_key=True)
    etablissement_id = db.Column(db.Integer, db.ForeignKey('etablissement.id'), primary_key=True)
    calendrier_id = db.Column(db.Integer, db.ForeignKey('calendrier.id'), primary_key=True)

    def to_dict(self):
        return {
            'eleve_id': self.eleve_id,
            'classe_id': self.classe_id,
            'etablissement_id': self.etablissement_id,
            'calendrier_id': self.calendrier_id,
        }

class Enseignant(db.Model):
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), primary_key=True)
    matricule = db.Column(db.String(20))
    etablissement_id = db.Column(db.Integer, db.ForeignKey('etablissement.id'))

    enseignements = db.relationship('Enseigner', backref='enseignant')

    def to_dict(self):
        return {
            'utilisateur_id': self.utilisateur_id,
            'matricule': self.matricule,
            'etablissement_id': self.etablissement_id,
        }

class Matiere(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    libelle = db.Column(db.String(100))

    metiers = db.relationship('MetierMatiere', backref='matiere')
    enseignements = db.relationship('Enseigner', backref='matiere')
    notes = db.relationship('Note', backref='matiere')
    ressources = db.relationship('Ressource', backref='matiere')

    def to_dict(self):
        return {
            'id': self.id,
            'libelle': self.libelle,
        }

class MetierMatiere(db.Model):
    metier_id = db.Column(db.Integer, db.ForeignKey('metier.id'), primary_key=True)
    matiere_id = db.Column(db.Integer, db.ForeignKey('matiere.id'), primary_key=True)
    coefficient = db.Column(db.Float)

    def to_dict(self):
        return {
            'metier_id': self.metier_id,
            'matiere_id': self.matiere_id,
            'coefficient': self.coefficient,
        }

class Enseigner(db.Model):
    enseignant_id = db.Column(db.Integer, db.ForeignKey('enseignant.utilisateur_id'), primary_key=True)
    etablissement_id = db.Column(db.Integer, db.ForeignKey('etablissement.id'), primary_key=True)
    matiere_id = db.Column(db.Integer, db.ForeignKey('matiere.id'), primary_key=True)
    classe_id = db.Column(db.Integer, db.ForeignKey('classe.id'), primary_key=True)
    calendrier_id = db.Column(db.Integer, db.ForeignKey('calendrier.id'), primary_key=True)

    def to_dict(self):
        return {
            'enseignant_id': self.enseignant_id,
            'etablissement_id': self.etablissement_id,
            'matiere_id': self.matiere_id,
            'classe_id': self.classe_id,
            'calendrier_id': self.calendrier_id,
        }

class Note(db.Model):
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleve.utilisateur_id'), primary_key=True)
    matiere_id = db.Column(db.Integer, db.ForeignKey('matiere.id'), primary_key=True)
    calendrier_id = db.Column(db.Integer, db.ForeignKey('calendrier.id'), primary_key=True)
    semestre = db.Column(db.Enum('1', '2', name='semestre_enum'), primary_key=True)
    note_cc1 = db.Column(db.Float)
    note_cc2 = db.Column(db.Float)
    note_composition = db.Column(db.Float)

    def to_dict(self):
        return {
            'eleve_id': self.eleve_id,
            'matiere_id': self.matiere_id,
            'calendrier_id': self.calendrier_id,
            'semestre': str(self.semestre),
            'note_cc1': self.note_cc1,
            'note_cc2': self.note_cc2,
            'note_composition': self.note_composition,
        }

class AppreciationCompetenceSpecifique(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleve.utilisateur_id'), primary_key=True)
    competence_id = db.Column(db.Integer, db.ForeignKey('competence_specifique.id'), primary_key=True)
    calendrier_id = db.Column(db.Integer, db.ForeignKey('calendrier.id'), primary_key=True)
    semestre = db.Column(db.Enum('1', '2', name='semestre_enum'), primary_key=True)

    competence = db.relationship('CompetenceSpecifique', backref='appreciations')

    def to_dict(self):
        return {
            'id': self.id,
            'eleve_id': self.eleve_id,
            'competence_id': self.competence_id,
            'calendrier_id': self.calendrier_id,
            'semestre': str(self.semestre)
        }

class AppreciationCompetenceComportementale(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleve.utilisateur_id'), primary_key=True)
    competence_id = db.Column(db.Integer, db.ForeignKey('competence_comportementale.id'), primary_key=True)
    calendrier_id = db.Column(db.Integer, db.ForeignKey('calendrier.id'), primary_key=True)
    semestre = db.Column(db.Enum('1', '2', name='semestre_enum'), primary_key=True)

    competence = db.relationship('CompetenceComportementale', backref='appreciations')

    def to_dict(self):
        return {
            'id': self.id,
            'eleve_id': self.eleve_id,
            'competence_id': self.competence_id,
            'calendrier_id': self.calendrier_id,
            'semestre': str(self.semestre)
        }

class AppreciationAptitude(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleve.utilisateur_id'), primary_key=True)
    aptitude_id = db.Column(db.Integer, db.ForeignKey('aptitude.id'), primary_key=True)
    calendrier_id = db.Column(db.Integer, db.ForeignKey('calendrier.id'), primary_key=True)
    semestre = db.Column(db.Enum('1', '2', name='semestre_enum'), primary_key=True)

    aptitude = db.relationship('Aptitude', backref='appreciations')

    def to_dict(self):
        return {
            'id': self.id,
            'eleve_id': self.eleve_id,
            'aptitude_id': self.aptitude_id,
            'calendrier_id': self.calendrier_id,
            'semestre': str(self.semestre)
        }

class InteretEleve(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleve.utilisateur_id'))
    interet_id = db.Column(db.Integer, db.ForeignKey('interet.id'))

    interet = db.relationship('Interet', backref='eleves')

    def to_dict(self):
        return {
            'id': self.id,
            'eleve_id': self.eleve_id,
            'interet_id': self.interet_id,
        }

class Commentaire(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.String(20))

    def to_dict(self):
        return {
            'id': self.id,
            'tag': self.tag,
        }

class CompetenceSpecifique(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    libelle = db.Column(db.String(30))

    def to_dict(self):
        return {
            'id': self.id,
            'libelle': self.libelle,
        }

class CompetenceComportementale(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    libelle = db.Column(db.String(30))

    def to_dict(self):
        return {
            'id': self.id,
            'libelle': self.libelle,
        }

class Aptitude(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    libelle = db.Column(db.String(30))

    def to_dict(self):
        return {
            'id': self.id,
            'libelle': self.libelle,
        }

class Interet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    libelle = db.Column(db.String(30))

    def to_dict(self):
        return {
            'id': self.id,
            'libelle': self.libelle,
        }

class Ressource(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titre = db.Column(db.String(255))
    url = db.Column(db.String(255))
    matiere_id = db.Column(db.Integer, db.ForeignKey('matiere.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'titre': self.titre,
            'url': self.url,
            'matiere_id': self.matiere_id,
        }