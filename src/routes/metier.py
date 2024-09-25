from flask import request
from sqlalchemy import delete

from ..app import app
from ..controllers.metier import *

@app.route('/metier', methods=['POST'])
def create_metier():
  return create()

@app.route('/metier', methods=['GET'])
def get_all_metiers():
  return get_all()

@app.route('/metier/<int:id>', methods=['GET'])
def get_metier_by_id(id):
  return get_by_id(id)

@app.route('/metier/<int:id>', methods=['PUT'])
def update_metier(id):
  return update(id)

@app.route('/metier/<int:id>', methods=['DELETE'])
def delete_metier(id):
  return delete(id)