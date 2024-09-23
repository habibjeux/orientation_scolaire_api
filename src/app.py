import os

# App Initialization
from . import create_app # from __init__ file
app = create_app(os.getenv("CONFIG_MODE"))

# Hello World!
@app.route('/')
def hello():
    return "Hello World!"

# Application Routes
from .routes import etablissement, utilisateur

# Run the app

if __name__ == "__main__":
    app.run()