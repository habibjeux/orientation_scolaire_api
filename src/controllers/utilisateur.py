from flask import request, jsonify

from .. import db
from ..models import Utilisateur

def create():
    prenom = request.json.get('prenom')
    nom = request.json.get('nom')
    mot_de_passe = request.json.get('mot_de_passe')
    role = request.json.get('role')
    date_naissance = request.json.get('date_naissance')
    adresse = request.json.get('adresse')

    if not prenom or not nom or not mot_de_passe or not role or not date_naissance or not adresse:
        return jsonify({'error': 'Veuillez sairir tous les champs'}), 400
    
    if user_exists(prenom, nom, date_naissance, adresse, role):
        return jsonify({'error': 'Utilisateur existe déjà'}), 400
    
    if role not in ['super_admin', 'gerant', 'enseignant', 'eleve']:
        return jsonify({'error': 'Role invalide'}), 400

    utilisateur = Utilisateur(prenom=prenom, nom=nom, role=role, date_naissance=date_naissance, adresse=adresse)
    utilisateur.set_password(mot_de_passe)
    db.session.add(utilisateur)
    db.session.commit()

    return jsonify({'message': 'utilisateur créé'}), 201

def get_all():
    utilisateurs = Utilisateur.query.all()
    return jsonify([utilisateur.to_dict() for utilisateur in utilisateurs])


def get_one(id):
    utilisateur = Utilisateur.query.get(id)

    if not utilisateur:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    return jsonify(utilisateur.to_dict())

def update(id):
    utilisateur = Utilisateur.query.get(id)
    if not utilisateur:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404

    prenom = request.json.get('prenom')
    nom = request.json.get('nom')
    mot_de_passe = request.json.get('mot_de_passe')
    role = request.json.get('role')
    date_naissance = request.json.get('date_naissance')
    adresse = request.json.get('adresse')

    if prenom:
        utilisateur.prenom = prenom
    if nom:
        utilisateur.nom = nom
    if mot_de_passe:
        utilisateur.mot_de_passe = mot_de_passe
    if role:
        utilisateur.role = role
    if date_naissance:
        utilisateur.date_naissance = date_naissance
    if adresse:
        utilisateur.adresse = adresse

    db.session.commit()
    return jsonify({'id': utilisateur.id})

def delete(id):
    utilisateur = Utilisateur.query.get(id)
    if not utilisateur:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404

    db.session.delete(utilisateur)
    db.session.commit()
    return jsonify({'message': 'Utilisateur supprimé'})


def get_by_role(role):
    utilisateurs = Utilisateur.query.filter_by(role=role).all()
    return jsonify([utilisateur.to_dict() for utilisateur in utilisateurs])

def user_exists(prenom, nom, date_naissance, adresse, role):
    return db.session.query(Utilisateur).filter_by(prenom=prenom, nom=nom, date_naissance=date_naissance, adresse=adresse, role=role).first() is not None

