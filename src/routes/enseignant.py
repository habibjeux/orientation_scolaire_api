from flask import request
from sqlalchemy import delete

from ..app import app
from ..controllers.enseignant import *

@app.route('/enseignant', methods=['POST'])
def create_enseignant():
  return create()

@app.route('/enseignant/<int:id>', methods=['GET'])
def get_enseignant_by_id(id):
  return get_by_id(id)

@app.route('/enseignant', methods=['GET'])
def get_all_enseignants():
  return get_all()

@app.route('/enseignant/<int:id>', methods=['DELETE'])
def delete_enseignant_by_id(id):
  return delete(id)