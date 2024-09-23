from . import create_app, db
import os

app = create_app(os.getenv("CONFIG_MODE"))

def init_db():
    with app.app_context():
        db.create_all()
        print("Database tables created")

if __name__ == "__main__":
    init_db()