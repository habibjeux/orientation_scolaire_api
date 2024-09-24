from flask import request, jsonify

from .. import db
from ..models import Enseignant, Etablissement, Utilisateur
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

  if not prenom or not nom or not mot_de_passe or not date_naissance or not adresse or not matricule or not etablissement:
    return jsonify({'error': 'Veuillez sairir tous les champs'}), 400

  existing_matricule = Enseignant.query.filter_by(matricule=data['matricule']).first()
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
  enseignant = Enseignant(utilisateur_id=utilisateur.id, matricule=matricule, etablissement_id=etablissement.id)
  try:
    db.session.add(enseignant)
    db.session.commit()
    return jsonify({'message': 'Enseignant créé avec succès'}), 201
  except:
    return jsonify({'message': 'Erreur lors de la création de l\'enseignant'}), 500
  
def get_by_id(id):
  enseignant = Enseignant.query.get(id)
  if not enseignant:
    return jsonify({'message': 'Enseignant non trouvé'}), 404
  
  enseignant_data = {
    'id': enseignant.utilisateur.id,
    'prenom': enseignant.utilisateur.prenom,
    'nom': enseignant.utilisateur.nom,
    'date_naissance': enseignant.utilisateur.date_naissance,
    'adresse': enseignant.utilisateur.adresse,
    'matricule': enseignant.matricule,
    'etablissement': enseignant.etablissement.nom if enseignant.etablissement else None
  }
  return jsonify(enseignant_data), 200

def get_all():
  enseignants = Enseignant.query.all()
  enseignants_data = []
  for enseignant in enseignants:
    enseignant_data = {
      'id': enseignant.utilisateur.id,
      'prenom': enseignant.utilisateur.prenom,
      'nom': enseignant.utilisateur.nom,
      'date_naissance': enseignant.utilisateur.date_naissance,
      'adresse': enseignant.utilisateur.adresse,
      'matricule': enseignant.matricule,
      'etablissement': enseignant.etablissement.nom if enseignant.etablissement else None
    }
    enseignants_data.append(enseignant_data)
  return jsonify(enseignants_data), 200 

def delete(id):
  enseignant = Enseignant.query.get(id)
  if not enseignant:
    return jsonify({'message': 'Enseignant non trouvé'}), 404
  
  try:
    db.session.delete(enseignant)
    # delete utilisateur
    utilisateur = Utilisateur.query.get(enseignant.utilisateur_id)
    db.session.delete(utilisateur)
    db.session.commit()
    return jsonify({'message': 'Enseignant supprimé avec succès'}), 200
  except:
    return jsonify({'message': 'Erreur lors de la suppression de l\'enseignant'}), 500