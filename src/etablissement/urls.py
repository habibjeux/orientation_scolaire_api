from flask import request

from ..app import app
from .controllers import get_all

@app.route('/etablissements', methods=['GET'])
def etablissements():
    return get_all()