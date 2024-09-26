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

@app.route('/eleve/transfert/<int:id>', methods=['PUT'])
def transfert_eleve(id):
  return transfert(id)

@app.route('/eleve/etablissement/<int:id>', methods=['GET'])
def get_eleves_by_etablissement(id):
  return get_by_etablissement(id)

@app.route('/eleve/inscription/<int:id>', methods=['POST'])
def inscrire_eleve(id):
  return inscrire(id)

