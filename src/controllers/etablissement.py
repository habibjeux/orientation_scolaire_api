from flask import request, jsonify

from .. import db
from ..models import Etablissement

def create():
  data = request.get_json()
  new_etablissement = Etablissement(nom=data['nom'], adresse=data['adresse'])
  existing_etablissement = Etablissement.query.filter_by(nom=data['nom']).first()
  if existing_etablissement:
      return jsonify({'message': 'Etablissement existant'}), 400
  db.session.add(new_etablissement)
  db.session.commit()
  return jsonify({'message': 'Etalissement créé avec succès'})

def get_one(id):
  etablissement = Etablissement.query.get(id)
  if not etablissement:
      return jsonify({'message': 'Etablissement non trouvé'})
  etablissement_data = {}
  etablissement_data['id'] = etablissement.id
  etablissement_data['nom'] = etablissement.nom
  etablissement_data['adresse'] = etablissement.adresse
  return jsonify(etablissement_data)

def update(id):
  etablissement = Etablissement.query.get(id)
  if not etablissement:
      return jsonify({'message': 'Etablissement non trouvé'})
  data = request.get_json()
  if('nom' in data):
      etablissement.nom = data['nom']
  if('adresse' in data):
      etablissement.adresse = data['adresse']
  existing_etablissement = Etablissement.query.filter(Etablissement.nom==data['nom'], Etablissement.id!=id).first()
  if existing_etablissement:
      return jsonify({'message': 'Etablissement existant'}), 400


  db.session.commit()
  return jsonify({'message': 'Etablissement modifié avec succès'})

def delete(id):
  etablissement = Etablissement.query.get(id)
  if not etablissement:
      return jsonify({'message': 'no etablissement found'})
  db.session.delete(etablissement)
  db.session.commit()
  return jsonify({'message': 'etablissement deleted'})

def get_all():
  return jsonify([etablissement.to_dict() for etablissement in Etablissement.query.all()])

def etablissement_no_assigned():
  etablissements = Etablissement.query.filter(Etablissement.gerants == None).all()
  return jsonify([etablissement.to_dict() for etablissement in etablissements])
