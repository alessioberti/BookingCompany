import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Carica variabili d'ambiente da .env
load_dotenv()

# Inizializza estensioni
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Configurazione dell'app
    app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  # Chiave JWT
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')  # Connessione al database PostgreSQL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disabilita notifiche inutili

    # Inizializza estensioni
    db.init_app(app)
    jwt.init_app(app)

    # Caricamento delle rotte dal file routes.py
    from .auth_routes import auth_bp
    from .slots_route import slots_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(slots_bp)
    
    return app

