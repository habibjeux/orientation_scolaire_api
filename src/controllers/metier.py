from datetime import datetime
from flask import request, jsonify

from .. import db
from ..models import Metier

def create():
  data = request.get_json()
  libelle = data.get('libelle')
  if libelle is None:
      return jsonify({'message': 'Libellé manquant'}), 400
  
  metier = Metier(libelle=libelle)

  existing_metier = Metier.query.filter_by(libelle=libelle).first()
  if existing_metier is not None:
      return jsonify({'message': 'Métier déjà existant'}), 409

  db.session.add(metier)
  db.session.commit()
  return jsonify({'message': 'Métier créé avec succès'}), 201

def get_all():
  metiers = Metier.query.all()
  return jsonify([metier.to_dict() for metier in metiers])

def get_by_id(id):
  metier = Metier.query.get(id)
  if metier is None:
      return jsonify({'message': 'Métier introuvable'}), 404
  return jsonify(metier.to_dict())

def update(id):
  metier = Metier.query.get(id)
  if metier is None:
      return jsonify({'message': 'Métier introuvable'}), 404

  data = request.get_json()
  libelle = data.get('libelle')
  if libelle is not None:
      metier.libelle = libelle

  existing_metier = Metier.query.filter_by(libelle=libelle).first()
  if existing_metier is not None and existing_metier.id != id:
      return jsonify({'message': 'Métier déjà existant'}), 409

  db.session.commit()
  return jsonify({'message': 'Métier modifié avec succès'})

def delete(id):
  metier = Metier.query.get(id)
  if metier is None:
      return jsonify({'message': 'Métier introuvable'}), 404

  db.session.delete(metier)
  db.session.commit()
  return jsonify({'message': 'Métier supprimé avec succès'})

