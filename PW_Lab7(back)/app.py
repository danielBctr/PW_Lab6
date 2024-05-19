# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database.database import db
from database.REcipe import Recipes
def create_app():
    app = Flask(__name__)
    # Configure SQLAlchemy to use SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
    b.init_app(app)
    return app
    if __name__ == "__main__":
    app = create_app()
    import routes
    app.run()