from flask import request
from sqlalchemy import delete

from ..app import app
from ..controllers.etablissement import *

@app.route('/etablissement', methods=['POST'])
def add_etablissement():
    return create()

@app.route('/etablissement/<id>', methods=['DELETE'])
def delete_etablissement(id):
    return delete(id)

@app.route('/etablissement', methods=['GET'])
def etablissements():
    return get_all()

@app.route('/etablissement/<id>', methods=['GET'])
def etablissement(id):
    return get_one(id)

@app.route('/etablissement/<id>', methods=['PUT'])
def update_etablissement(id):
    return update(id)

@app.route('/etablissement/no_assigned', methods=['GET'])
def get_etablissement_no_assigned():
    return etablissement_no_assigned()