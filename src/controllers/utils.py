from datetime import datetime
from flask import request, jsonify

from .. import db
from ..models import GerantEtablissement, Utilisateur, Eleve, Enseignant


# verifier si user existe dans la base de données dans GerantEtablissement, Utilisateur, Eleve, Enseignant et Utilisateur
def verify_user_exist