from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

class User(db.Model):
    __tablename__ = 'users'  # Nome della tabella nel database

    # Colonne

    id = db.Column('user_id', db.Integer, primary_key=True)  # Mappato al campo SERIAL PRIMARY KEY
    username = db.Column('username', db.String(255), unique=True, nullable=False)
    password_hash = db.Column('password_hash', db.String(255), nullable=False)
    email = db.Column('email_address', db.String(255), unique=True, nullable=False)

    # Metodi

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Exam(db.Model):
    __tablename__ = 'exams'  # Nome della tabella in minuscolo

    # Colonne
    
    exam_id = db.Column('exam_id', db.Integer, primary_key=True) # Chiave primaria
    name = db.Column('name', db.String(255), nullable=False) # Nome dell'esame
    description = db.Column('description', db.Text) # Descrizione dell'esame
    exam_type_id = db.Column('exam_type_id', db.Integer, db.ForeignKey('exam_types.exam_type_id'), nullable=False) # Tipo di esame
    laboratory_id = db.Column('laboratory_id', db.Integer, db.ForeignKey('laboratories.laboratory_id'), nullable=False) # Laboratorio in cui si svolge l'esame
    operator_id = db.Column('operator_id', db.Integer, db.ForeignKey('operators.operator_id'))  # Operatore che gestisce l'esame
    is_available = db.Column('is_available', db.Boolean, default=True) # Definisce se l'esame è prenotabile
    available_from = db.Column('available_from', db.Date) # Data di inizio dispobilità prenotazioni
    avaiable_to = db.Column('available_to', db.Date) # Data di fine disponibilità prenotazioni 
    opening_time = db.Column('opening_time', db.Time, nullable=False)  # Orario inizio esami
    closing_time = db.Column('closing_time', db.Time, nullable=False)  # Orario fine esami
    slot_duration = db.Column('slot_duration', db.Integer, nullable=False)  # Durata slot prenotabile in minuti
    buffer_time = db.Column('buffer_time', db.Integer, nullable=False)  # Buffer in minuti tra uno slot e l'altro
    weekdays = db.Column('weekdays', db.String(50), nullable=False)  # Giornati della settimana in cui l'esame è disponibile

