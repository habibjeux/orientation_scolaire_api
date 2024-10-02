from flask import request
from sqlalchemy import delete

from ..app import app
from ..controllers.calendrier import *

@app.route('/calendrier', methods=['POST'])
def add_calendrier():
    return create()

@app.route('/calendrier', methods=['GET'])
def calendriers():
    return get_all()

@app.route('/calendrier/<id>', methods=['GET'])
def calendrier(id):
    return get_by_id(id)

@app.route('/calendrier/<id>', methods=['PUT'])
def update_calendrier(id):
    return update(id)

@app.route('/calendrier/<id>', methods=['DELETE'])
def delete_calendrier(id):
    return delete(id)

@app.route('/calendrier/etablissement/<etablissement_id>', methods=['GET'])
def calendrier_etablissement(etablissement_id):
    return get_by_etablissement(etablissement_id)