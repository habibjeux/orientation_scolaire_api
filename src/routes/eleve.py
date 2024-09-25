from flask import request
from sqlalchemy import delete

from ..app import app
from ..controllers.eleve import *

@app.route('/eleve', methods=['POST'])
def create_eleve():
  return create()

@app.route('/eleve/<int:id>', methods=['GET'])
def get_eleve_by_id(id):
  return get_by_id(id)

@app.route('/eleve', methods=['GET'])
def get_all_eleves():
  return get_all()

@app.route('/eleve/<int:id>', methods=['DELETE'])
def delete_eleve(id):
  return delete(id)

@app.route('/eleve/<int:id>', methods=['PUT'])
def update_eleve(id):
  return update(id)