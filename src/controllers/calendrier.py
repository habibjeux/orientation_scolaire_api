from datetime import datetime
from flask import request, jsonify

from .. import db
from ..models import Calendrier, Etablissement

'''
class Calendrier(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    annee_academique = db.Column(db.String(9))  # Format : YYYY-YYYY
    debut = db.Column(db.DateTime)
    fin = db.Column(db.DateTime)
    etablissement_id = db.Column(db.Integer, db.ForeignKey('etablissement.id'))
'''

def create():
    data = request.get_json()
    debut = data.get('debut')
    fin = data.get('fin')
    annee_academique = data.get('annee-academique')
    etablissement = data.get('etablissement')

    if not debut or not annee_academique or not etablissement:
        return jsonify({'message': 'Veuillez saisir tous les champs obligatoires'}), 400
    
    if len(annee_academique) != 9 or annee_academique[4] != '-':
        return jsonify({'message': 'Format d\'année académique invalide'}), 400
    try:
        debut = datetime.strptime(debut, '%Y-%m-%d')
    except ValueError:
        return jsonify({'message': 'Format de date invalide'}), 400
    
    if fin:
        try:
            fin = datetime.strptime(fin, '%Y-%m-%d')
        except ValueError:
            return jsonify({'message': 'Format de date invalide'}), 400
        if debut > fin:
            return jsonify({'message': 'Plage de date invalide'}), 400
        
    etablissement = Etablissement.query.filter_by(nom=etablissement).first()
    if not etablissement:
        return jsonify({'message': 'Etablissement non trouvé'}), 404
    
    calendrier = Calendrier(annee_academique=annee_academique, debut=debut, etablissement_id=etablissement.id)
    if fin:
        calendrier.fin = fin


    existing_calendrier = Calendrier.query.filter(Calendrier.etablissement_id == calendrier.etablissement_id, Calendrier.annee_academique == calendrier.annee_academique).first()
    if existing_calendrier:
        return jsonify({'message': 'Conflit de calendrier'}), 400

    try:
        db.session.add(calendrier)
        db.session.commit()
        return jsonify({'message': 'Calendrier créé avec succès'}), 201
    except:
        return jsonify({'message': 'Erreur lors de la création du calendrier'}), 500
    

def get_all():
    calendriers = Calendrier.query.all()
    return jsonify([calendrier.to_dict() for calendrier in calendriers])

def get_by_id(id):
    calendrier = Calendrier.query.get(id)
    if calendrier is None:
        return jsonify({'message': 'Calendrier introuvable'}), 404
    return jsonify(calendrier.to_dict())

def update(id):
    calendrier = Calendrier.query.get(id)
    if calendrier is None:
        return jsonify({'message': 'Calendrier introuvable'}), 404
    
    data = request.get_json()
    if 'annee-academique' in data:
        calendrier.annee_academique = data['annee-academique']
    if 'debut' in data:
        try:
            data['debut'] = datetime.strptime(data['debut'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'message': 'Format de date invalide'}), 400
        calendrier.debut = data['debut']
    if 'fin' in data:
        try:
            data['fin'] = datetime.strptime(data['fin'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'message': 'Format de date invalide'}), 400
        calendrier.fin = data['fin']
    if 'etablissement' in data:
        etablissement = Etablissement.query.filter_by(nom=data['etablissement']).first()
        if not etablissement:
            return jsonify({'message': 'Etablissement non trouvé'}), 404
        calendrier.etablissement_id = etablissement.id

    if calendrier.debut > calendrier.fin:
        return jsonify({'message': 'Plage de date invalide'}), 400
    db.session.commit()

    if 'etablissement' in data or 'annee-academique' in data:
        existing_calendrier = Calendrier.query.filter(Calendrier.etablissement_id == calendrier.etablissement_id, Calendrier.annee_academique == calendrier.annee_academique, Calendrier.id != calendrier.id).first()
        if existing_calendrier:
            return jsonify({'message': 'Conflit de calendrier'}), 400

    return jsonify({'message': 'Calendrier modifié avec succès'})

def delete(id):
    calendrier = Calendrier.query.get(id)
    if calendrier is None:
        return jsonify({'message': 'Calendrier introuvable'}), 404
    
    db.session.delete(calendrier)
    db.session.commit()
    return jsonify({'message': 'Calendrier supprimé avec succès'})
