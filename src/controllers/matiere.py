from datetime import datetime
from flask import request, jsonify

from .. import db
from ..models import Matiere

def create():
  data = request.get_json()
  libelle = data.get('libelle')
  if libelle is None:
      return jsonify({'message': 'Libellé manquant'}), 400
  
  matiere = Matiere(libelle=libelle)

  existing_matiere = Matiere.query.filter_by(libelle=libelle).first()
  if existing_matiere is not None:
      return jsonify({'message': 'Matière déjà existante'}), 409

  db.session.add(matiere)
  db.session.commit()
  return jsonify({'message': 'Matière créée avec succès'}), 201

def get_all():
  matieres = Matiere.query.all()
  return jsonify([matiere.to_dict() for matiere in matieres])

def get_by_id(id):
  matiere = Matiere.query.get(id)
  if matiere is None:
      return jsonify({'message': 'Matière introuvable'}), 404
  return jsonify(matiere.to_dict())

def update(id):
  matiere = Matiere.query.get(id)
  if matiere is None:
      return jsonify({'message': 'Matière introuvable'}), 404

  data = request.get_json()
  libelle = data.get('libelle')
  if libelle is not None:
      matiere.libelle = libelle

  existing_matiere = Matiere.query.filter_by(libelle=libelle).first()
  if existing_matiere is not None and existing_matiere.id != id:
      return jsonify({'message': 'Matière déjà existante'}), 409

  db.session.commit()
  return jsonify({'message': 'Matière modifiée avec succès'})

def delete(id):
  matiere = Matiere.query.get(id)
  if matiere is None:
      return jsonify({'message': 'Matière introuvable'}), 404

  db.session.delete(matiere)
  db.session.commit()
  return jsonify({'message': 'Matière supprimée avec succès'})

