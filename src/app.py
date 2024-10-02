import os

# App Initialization
from flask_cors import CORS
from . import create_app # from __init__ file
app = create_app(os.getenv("CONFIG_MODE"))
CORS(app)

# Hello World!
@app.route('/')
def hello():
    return "Hello World!"

# Application Routes
from .routes import etablissement, utilisateur, calendrier, gerant, enseignant, classe, metier, matiere, eleve

# Run the app

if __name__ == "__main__":
    app.run()