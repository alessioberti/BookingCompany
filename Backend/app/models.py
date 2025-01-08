from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime, time, timedelta

# Model per la tabella users
class User(db.Model):
    __tablename__ = 'users' 

    # Colonne
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(255), unique=True, nullable=False)
    password_hash = db.Column('password_hash', db.String(255), nullable=False)
    email = db.Column('email_address', db.String(255), unique=True, nullable=False)

    # Funzione per generare l'hash della password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    #Funzione per esguire il check dell'hash della password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Model per tabella laboratories
class Laboratory(db.Model):
    __tablename__ = 'laboratories'

    # Colonne
    laboratory_id = db.Column('laboratory_id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(255), nullable=False)
    address = db.Column('address', db.String(255))
    contact_info = db.Column('contact_info', db.String(255))
    exams = db.relationship('Exam', back_populates='laboratory')
# Model per tabella operators
class Operator(db.Model):
    __tablename__ = 'operators'

    #Colonne
    operator_id = db.Column('operator_id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), unique=True, nullable=False)
    first_name = db.Column('first_name', db.String(255), nullable=False)
    last_name = db.Column('last_name', db.String(255), nullable=False)
    role = db.Column('role', db.String(255), nullable=False)
    contact_info = db.Column('contact_info', db.String(255))
    exams = db.relationship('Exam', back_populates='operator')

# Model per la tabella Exam
class Exam(db.Model):
    __tablename__ = 'exams'

    # Colonne 
    exam_id = db.Column('exam_id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(255), nullable=False)
    description = db.Column('description', db.Text)
    exam_type_id = db.Column('exam_type_id', db.Integer, db.ForeignKey('exam_types.exam_type_id'), nullable=False)
    laboratory_id = db.Column('laboratory_id', db.Integer, db.ForeignKey('laboratories.laboratory_id'), nullable=False)
    operator_id = db.Column('operator_id', db.Integer, db.ForeignKey('operators.operator_id'))
    is_available = db.Column('is_available', db.Boolean, default=True)
    available_from_date = db.Column('available_from_date', db.Date)
    available_to_date = db.Column('available_to_date', db.Date)
    available_from_time = db.Column('available_from_time', db.Time, nullable=False)
    available_to_time = db.Column('available_to_time', db.Time, nullable=False)
    slot_duration = db.Column('slot_duration', db.Integer, nullable=False)
    pause_minutes = db.Column('pause_minutes', db.Integer, nullable=False)
    available_weekday = db.Column('available_weekday', db.Integer, nullable=False)

    # Relazione con tabella laboratories
    laboratory = db.relationship('Laboratory', back_populates='exams') 

    # Relazione con tabella operators
    operator = db.relationship('Operator', back_populates='exams')