from datetime import datetime
from flask import request, jsonify

from .. import db
from ..models import Classe

def create():
  data = request.get_json()
  libelle = data.get('libelle')
  serie = data.get('serie')
  if libelle is None:
      return jsonify({'message': 'Libellé manquant'}), 400
  
  classe = Classe(libelle=libelle)
  if serie is not None:
      classe.serie = serie

  existing_classe = Classe.query.filter_by(libelle=libelle, serie=serie).first()
  if existing_classe is not None:
      return jsonify({'message': 'Classe déjà existante'}), 409

  db.session.add(classe)
  db.session.commit()
  return jsonify({'message': 'Classe créée avec succès'}), 201

def get_all():
  classes = Classe.query.all()
  return jsonify([classe.to_dict() for classe in classes])

def get_by_id(id):
  classe = Classe.query.get(id)
  if classe is None:
      return jsonify({'message': 'Classe introuvable'}), 404
  return jsonify(classe.to_dict())
