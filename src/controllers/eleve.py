from flask import request, jsonify

from .. import db
from ..models import Calendrier, Classe, Eleve, Etablissement, Inscription, Metier, Utilisateur

def create():
  data = request.get_json()
  prenom = data.get('prenom')
  nom = data.get('nom')
  mot_de_passe = data.get('mot_de_passe')
  role = 'enseignant'
  date_naissance = data.get('date_naissance')
  adresse = data.get('adresse')
  matricule = data.get('matricule')
  etablissement = data.get('etablissement')
  metier = data.get('metier')

  if not prenom or not nom or not mot_de_passe or not date_naissance or not adresse or not matricule or not etablissement:
    return jsonify({'error': 'Veuillez sairir tous les champs obligatoires'}), 400
  
  existing_matricule = Eleve.query.filter_by(matricule=data['matricule']).first()
  if existing_matricule:
    return jsonify({'message': 'Matricule déjà pris'}), 400
  
  etablissement = Etablissement.query.filter_by(nom=etablissement).first()
  if not etablissement:
    return jsonify({'message': 'Etablissement non trouvé'}), 404
  
  utilisateur = Utilisateur(prenom=prenom, nom=nom, role=role, date_naissance=date_naissance, adresse=adresse)
  utilisateur.set_password(mot_de_passe)

  try:
    db.session.add(utilisateur)
    db.session.commit()
  except:
    return jsonify({'message': 'Erreur lors de la création de l\'utilisateur'}), 500
  
  eleve = Eleve(utilisateur_id=utilisateur.id, matricule=matricule, etablissement_id=etablissement.id)

  if metier:
    metier = Metier.query.filter_by(libelle=metier).first()
    if not metier:
      return jsonify({'message': 'Metier non trouvé'}), 404
    eleve.metier_id = metier.id

  try:
    db.session.add(eleve)
    db.session.commit()
    return jsonify({'message': 'Eleve créé avec succès'}), 201
  except:
    return jsonify({'message': 'Erreur lors de la création de l\'eleve'}), 500
  
def get_by_id(id):
  eleve = Eleve.query.get(id)
  if not eleve:
    return jsonify({'message': 'Eleve non trouvé'}), 404
  
  eleve_data = {
    'id': eleve.utilisateur.id,
    'prenom': eleve.utilisateur.prenom,
    'nom': eleve.utilisateur.nom,
    'date_naissance': eleve.utilisateur.date_naissance,
    'adresse': eleve.utilisateur.adresse,
    'matricule': eleve.matricule,
    'etablissement': eleve.etablissement.nom if eleve.etablissement else None,
    'metier': eleve.metier.libelle if eleve.metier else None
  }
  return jsonify(eleve_data), 200

def get_all():
  eleves = Eleve.query.all()
  eleves_data = []
  for eleve in eleves:
    eleve_data = {
      'id': eleve.utilisateur.id,
      'prenom': eleve.utilisateur.prenom,
      'nom': eleve.utilisateur.nom,
      'date_naissance': eleve.utilisateur.date_naissance,
      'adresse': eleve.utilisateur.adresse,
      'matricule': eleve.matricule,
      'etablissement': eleve.etablissement.nom if eleve.etablissement else None,
      'metier': eleve.metier.libelle if eleve.metier else None
    }
    eleves_data.append(eleve_data)
  return jsonify(eleves_data), 200

def delete(id):
  eleve = Eleve.query.get(id)
  if not eleve:
    return jsonify({'message': 'Eleve non trouvé'}), 404
  
  try:
    db.session.delete(eleve)
    db.session.commit()
  except:
    return jsonify({'message': 'Erreur lors de la suppression de l\'eleve'}), 500
  
  try:
    utilisateur = Utilisateur.query.get(eleve.utilisateur_id)
    db.session.delete(utilisateur)
    db.session.commit()
    return jsonify({'message': 'Eleve supprimé avec succès'}), 200
  except:
    return jsonify({'message': 'Erreur lors de la suppression de l\'utilisateur'}), 500
  
def update(id):
  eleve = Eleve.query.get(id)
  if not eleve:
    return jsonify({'message': 'Eleve non trouvé'}), 404
  
  data = request.get_json()
  if data.get('etablissement'):
    etablissement = Etablissement.query.filter_by(nom=data['etablissement']).first()
    if not etablissement:
      return jsonify({'message': 'Etablissement non trouvé'}), 404
    eleve.etablissement_id = etablissement.id
  if data.get('metier'):
    metier = Metier.query.filter_by(libelle=data['metier']).first()
    if not metier:
      return jsonify({'message': 'Metier non trouvé'}), 404
    eleve.metier_id = metier.id
  if data.get('prenom'):
    eleve.utilisateur.prenom = data['prenom']
  if data.get('nom'):
    eleve.utilisateur.nom = data['nom']
  if data.get('date_naissance'):
    eleve.utilisateur.date_naissance = data['date_naissance']
  if data.get('adresse'):
    eleve.utilisateur.adresse = data['adresse']
  if data.get('matricule'):
    existing_matricule = Eleve.query.filter_by(matricule=data['matricule']).first()
    if existing_matricule and existing_matricule.utilisateur_id != eleve.utilisateur_id:
      return jsonify({'message': 'Matricule déjà pris'}), 400
    eleve.matricule = data['matricule']
  
  try:
    db.session.commit()
    return jsonify({'message': 'Eleve modifié avec succès'}), 200
  except:
    return jsonify({'message': 'Erreur lors de la modification de l\'eleve'}), 500
  
def transfert(id):
  eleve = Eleve.query.get(id)
  if not eleve:
    return jsonify({'message': 'Eleve non trouvé'}), 404
  
  data = request.get_json()
  if not data.get('etablissement'):
    return jsonify({'message': 'Veuillez saisir l\'etablissement de destination'}), 400
  etablissement = Etablissement.query.filter_by(nom=data['etablissement']).first()
  if not etablissement:
    return jsonify({'message': 'Etablissement non trouvé'}), 404
  
  eleve.etablissement_id = etablissement.id
  try:
    db.session.commit()
    return jsonify({'message': 'Eleve transféré avec succès'}), 200
  except:
    return jsonify({'message': 'Erreur lors du transfert de l\'eleve'}), 500
  
def get_by_etablissement(id):
  eleves = Eleve.query.filter_by(etablissement_id=id).all()
  eleves_data = []
  for eleve in eleves:
    eleve_data = {
      'id': eleve.utilisateur.id,
      'prenom': eleve.utilisateur.prenom,
      'nom': eleve.utilisateur.nom,
      'date_naissance': eleve.utilisateur.date_naissance,
      'adresse': eleve.utilisateur.adresse,
      'matricule': eleve.matricule,
      'etablissement': eleve.etablissement.nom if eleve.etablissement else None,
      'metier': eleve.metier.libelle if eleve.metier else None
    }
    eleves_data.append(eleve_data)
  return jsonify(eleves_data), 200

def inscrire(id):
  eleve = Eleve.query.get(id)
  if not eleve:
    return jsonify({'message': 'Eleve non trouvé'}), 404
  
  data = request.get_json()
  if not data.get('metier'):
    return jsonify({'message': 'Veuillez saisir le metier à inscrire'}), 400
  metier = Metier.query.filter_by(libelle=data['metier']).first()
  if not metier:
    return jsonify({'message': 'Metier non trouvé'}), 404
  
  eleve.metier_id = metier.id
  try:
    db.session.commit()
    return jsonify({'message': 'Eleve inscrit avec succès'}), 200
  except:
    return jsonify({'message': 'Erreur lors de l\'inscription de l\'eleve'}), 500
  

'''
class Inscription(db.Model):
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleve.utilisateur_id'), primary_key=True)
    classe_id = db.Column(db.Integer, db.ForeignKey('classe.id'), primary_key=True)
    etablissement_id = db.Column(db.Integer, db.ForeignKey('etablissement.id'), primary_key=True)
    calendrier_id = db.Column(db.Integer, db.ForeignKey('calendrier.id'), primary_key=True)
'''

def inscrire(id):
  eleve = Eleve.query.get(id)
  if not eleve:
    return jsonify({'message': 'Eleve non trouvé'}), 404
  
  data = request.get_json()
  classe = data['classe']
  etablissement = data['etablissement']
  annee_academique = data['annee-academique']

  if not classe or not etablissement or not annee_academique:
    return jsonify({'message': 'Veuillez saisir tous les champs obligatoires'}), 400
  
  classe = Classe.query.filter_by(libelle=classe).first()
  if not classe:
    return jsonify({'message': 'Classe non trouvée'}), 404
  
  etablissement = Etablissement.query.filter_by(nom=etablissement).first()
  if not etablissement:
    return jsonify({'message': 'Etablissement non trouvé'}), 404
  
  if eleve.etablissement_id != etablissement.id:
    return jsonify({'message': 'L\'eleve n\'appartient pas à cet établissement'}), 400
  
  calendrier = Calendrier.query.filter_by(etablissement_id=etablissement.id, annee_academique=annee_academique).first()
  if not calendrier:
    return jsonify({'message': 'Calendrier non trouvé'}), 404
  
  inscription = Inscription(eleve_id=eleve.utilisateur_id, classe_id=classe.id, etablissement_id=etablissement.id, calendrier_id=calendrier.id)

  try:
    db.session.add(inscription)
    db.session.commit()
    return jsonify({'message': 'Eleve inscrit avec succès'}), 201
  except:
    return jsonify({'message': 'Erreur lors de l\'inscription de l\'eleve'}), 500