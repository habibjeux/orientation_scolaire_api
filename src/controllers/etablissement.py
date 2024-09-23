from flask import request, jsonify

from .. import db
from ..models import Etablissement

def create():
    data = request.get_json()
    new_etablissement = Etablissement(nom=data['nom'], adresse=data['adresse'])
    db.session.add(new_etablissement)
    db.session.commit()
    return jsonify({'message': 'new etablissement created'})

def get_one(id):
    etablissement = Etablissement.query.get(id)
    if not etablissement:
        return jsonify({'message': 'no etablissement found'})
    etablissement_data = {}
    etablissement_data['id'] = etablissement.id
    etablissement_data['nom'] = etablissement.nom
    etablissement_data['adresse'] = etablissement.adresse
    return jsonify(etablissement_data)

def update(id):
    etablissement = Etablissement.query.get(id)
    if not etablissement:
        return jsonify({'message': 'no etablissement found'})
    data = request.get_json()
    if('nom' in data):
      etablissement.nom = data['nom']
    if('adresse' in data):
      etablissement.adresse = data['adresse']
    db.session.commit()
    return jsonify({'message': 'etablissement updated'})

def delete(id):
    etablissement = Etablissement.query.get(id)
    if not etablissement:
        return jsonify({'message': 'no etablissement found'})
    db.session.delete(etablissement)
    db.session.commit()
    return jsonify({'message': 'etablissement deleted'})

def get_all():
    return jsonify([etablissement.to_dict() for etablissement in Etablissement.query.all()])

def search_by_name(name):
    etablissements = Etablissement.query.filter_by(nom=name).all()
    if not etablissements:
        return jsonify({'message': 'no etablissement found'})
    output = []
    for etablissement in etablissements:
        etablissement_data = {}
        etablissement_data['id'] = etablissement.id
        etablissement_data['nom'] = etablissement.nom
        etablissement_data['adresse'] = etablissement.adresse
        output.append(etablissement_data)
    return jsonify(output)