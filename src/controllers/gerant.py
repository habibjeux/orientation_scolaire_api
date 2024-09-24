from flask import request, jsonify

from .. import db
from ..models import GerantEtablissement, Utilisateur, Etablissement
from .utilisateur import user_exists
from .etablissement import search_by_name as search_etablissement_by_name

def create():
  
  data = request.get_json()

  prenom = data.get('prenom')
  nom = data.get('nom')
  mot_de_passe = data.get('mot_de_passe')
  role = 'gerant'
  date_naissance = data.get('date_naissance')
  adresse = data.get('adresse')
  email = data.get('email')

  # Vérification des champs obligatoires
  if not prenom or not nom or not mot_de_passe or not date_naissance or not adresse or not email:
      return jsonify({'error': 'Veuillez sairir tous les champs'}), 400
  
  # Vérification si l'email est déjà utilisé par un autre gérant
  existing_email = GerantEtablissement.query.filter_by(email=data['email']).first()
  if existing_email:
    return jsonify({'message': 'Email déjà pris'}), 400

  if user_exists(prenom, nom, date_naissance, adresse, role):
      return jsonify({'error': 'Ce gérant existe déjà'}), 400

  # Création de l'utilisateur
  utilisateur = Utilisateur(prenom=prenom, nom=nom, role=role, date_naissance=date_naissance, adresse=adresse)
  utilisateur.set_password(mot_de_passe)

  try:
    db.session.add(utilisateur)
    db.session.commit()
  except:
    return jsonify({'message': 'Erreur lors de la création de l\'utilisateur'}), 500
  
  # Création du gérant
  gerant = GerantEtablissement(utilisateur_id=utilisateur.id, email=email)
  try:
    db.session.add(gerant)
    db.session.commit()
    return jsonify({'message': 'Gérant créé avec succès'}), 201
  except:
    return jsonify({'message': 'Erreur lors de la création du gérant'}), 500

def get_by_id(id):
  gerant = GerantEtablissement.query.get(id)
  if not gerant:
    return jsonify({'message': 'Gérant non trouvé'}), 404
  
  gerant_data = {
    'id': gerant.utilisateur.id,
    'prenom': gerant.utilisateur.prenom,
    'nom': gerant.utilisateur.nom,
    'date_naissance': gerant.utilisateur.date_naissance,
    'adresse': gerant.utilisateur.adresse,
    'email': gerant.email,
    'etablissement': gerant.etablissement.nom if gerant.etablissement else None
  }
  return jsonify(gerant_data), 200    

def get_all():
  gerants = GerantEtablissement.query.all()
  gerants_data = []
  for gerant in gerants:
    gerant_data = {
      'id': gerant.utilisateur.id,
      'prenom': gerant.utilisateur.prenom,
      'nom': gerant.utilisateur.nom,
      'date_naissance': gerant.utilisateur.date_naissance,
      'adresse': gerant.utilisateur.adresse,
      'email': gerant.email,
      'etablissement': gerant.etablissement.nom if gerant.etablissement else None
    }
    gerants_data.append(gerant_data)
  return jsonify(gerants_data), 200

def assign_etablissement_to_gerant():
  data = request.get_json()
  gerant_id = data.get('gerant_id')
  etablissement_id = data.get('etablissement_id')

  if not gerant_id or not etablissement_id:
    return jsonify({'message': 'Veuillez saisir tous les champs'}), 400
  
  gerant = GerantEtablissement.query.get(gerant_id)
  if not gerant:
    return jsonify({'message': 'Gérant non trouvé'}), 404
  
  etablissement = Etablissement.query.get(etablissement_id)
  if not etablissement:
    return jsonify({'message': 'Etablissement non trouvé'}), 404
  
  gerant.etablissement_id = etablissement_id
  try:
    db.session.commit()
    return jsonify({'message': 'Etablissement assigné avec succès'}), 200
  except:
    return jsonify({'message': 'Erreur lors de l\'assignation de l\'établissement'}), 500
  
def delete_gerant(id):
  gerant = GerantEtablissement.query.get(id)
  if not gerant:
    return jsonify({'message': 'Gérant non trouvé'}), 404
  
  try:
    db.session.delete(gerant)
    utilisateur = Utilisateur.query.get(id)
    db.session.delete(utilisateur)
    db.session.commit()
    return jsonify({'message': 'Gérant supprimé avec succès'}), 200
  except:
    return jsonify({'message': 'Erreur lors de la suppression du gérant'}), 500


