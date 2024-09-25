from flask import request
from sqlalchemy import delete

from ..app import app
from ..controllers.matiere import *

@app.route('/matiere', methods=['POST'])
def create_matiere():
  return create()

@app.route('/matiere', methods=['GET'])
def get_all_matieres():
  return get_all()

@app.route('/matiere/<int:id>', methods=['GET'])
def get_matiere_by_id(id):
  return get_by_id(id)

@app.route('/matiere/<int:id>', methods=['PUT'])
def update_matiere(id):
  return update(id)

@app.route('/matiere/<int:id>', methods=['DELETE'])
def delete_matiere(id):
  return delete(id)