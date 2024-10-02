from flask import request
from sqlalchemy import delete

from ..app import app
from ..controllers.gerant import *

@app.route('/gerant', methods=['POST'])
def add_gerant():
    return create()

@app.route('/gerant', methods=['GET'])
def gerants():
    return get_all()

@app.route('/gerant/<int:id>', methods=['GET'])
def get_gerant(id):
    return get_by_id(id)

@app.route('/gerant/assign-etablissement', methods=['PUT'])
def assign_etablissement():
    return assign_etablissement_to_gerant()

@app.route('/gerant/<int:id>', methods=['DELETE'])
def del_gerant(id):
    return delete_gerant(id)
