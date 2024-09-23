from flask import request, jsonify
import uuid

from .. import db
from ..models import Etablissement

def get_all():
    etablissements = Etablissement.query.all()
    output = []
    for etablissement in etablissements:
        etablissement_data = {}
        etablissement_data['id'] = etablissement.id
        etablissement_data['nom'] = etablissement.nom
        etablissement_data['adresse'] = etablissement.adresse
        output.append(etablissement_data)
    return jsonify({'etablissements': output})