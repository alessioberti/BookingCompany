import re
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from . import db

from .models import User 

auth_bp = Blueprint('auth_routes', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    # Verifica campi login tramite regex altrimenti restituisci un errore
    if not re.match(r"^[a-zA-Z0-9_-]{3,20}$", username):
        return jsonify({"message": "Username non valido. Deve avere tra 3 e 20 caratteri e può contenere solo lettere, numeri, underscore e trattini."}), 400
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$", email):
        return jsonify({"message": "Email non valida. Fornisci un indirizzo email corretto."}), 400
    if not re.match(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", password):
        return jsonify({"message": "Password non valida. Deve avere almeno 8 caratteri, includere una lettera, un numero e un carattere speciale."}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username già in uso"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email già in uso"}), 400

    # Creazione Utente - Crea un nuovo oggetto User e aggiungilo al database
    new_user = User(username=username, email=email) 
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Utente registrato con successo"}), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()

    # Verifica se l'utente esiste e se la password è corretta altrimenti accesso negato
    if not user or not user.check_password(password):
        return jsonify({"message": "Credenziali non valide"}), 401

    # Genera un token JWT
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200