from flask import request
from sqlalchemy import delete

from ..app import app
from ..controllers.utilisateur import *

@app.route('/utilisateur', methods=['POST'])
def add_utilisateur():
    return create()

@app.route('/utilisateur', methods=['GET'])
def utilisateurs():
    return get_all()

@app.route('/utilisateur/<id>', methods=['GET'])
def utilisateur(id):
    return get_one(id)

@app.route('/utilisateur/<id>', methods=['PUT'])
def update_utilisateur(id):
    return update(id)

@app.route('/utilisateur/<id>', methods=['DELETE'])
def delete_utilisateur(id):
    return delete(id)

@app.route('/utilisateur/role/<role>', methods=['GET'])
def utilisateur_role(role):
    return get_by_role(role)