from flask import request
from sqlalchemy import delete

from ..app import app
from ..controllers.classe import *

@app.route('/classe', methods=['POST'])
def create_classe():
  return create()

@app.route('/classe', methods=['GET'])
def get_all_classes():
  return get_all()

@app.route('/classe/<int:id>', methods=['GET'])
def get_classe_by_id(id):
  return get_by_id(id)

@app.route('/classe/<int:id>', methods=['PUT'])
def update_classe(id):
  return update(id)

@app.route('/classe/<int:id>', methods=['DELETE'])
def delete_classe(id):
  return delete(id)