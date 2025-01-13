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
    tel_number = db.Column('tel_number', db.String(255), unique=True, nullable=False)

    # Funzione per generare l'hash della password
    def set_password(self, password_text):
        self.password_hash = generate_password_hash(password_text)

    # Funzione per eseguire il check dell'hash della password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Model per la tabella laboratories
class Laboratory(db.Model):
    __tablename__ = 'laboratories'

    # Colonne
    laboratory_id = db.Column('laboratory_id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(255), nullable=False)
    address = db.Column('address', db.String(255))
    contact_info = db.Column('contact_info', db.String(255))

    # Relazione con tabella operators_availability
    operators_availability = db.relationship('OperatorsAvailability', back_populates='laboratory')


# Model per la tabella operators
class Operator(db.Model):
    __tablename__ = 'operators'

    # Colonne
    operator_id = db.Column('operator_id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), unique=True, nullable=False)
    first_name = db.Column('first_name', db.String(255), nullable=False)
    last_name = db.Column('last_name', db.String(255), nullable=False)
    role = db.Column('role', db.String(255), nullable=False)
    address = db.Column('address', db.String(255))

    # Relazione con tabella operators_availability
    operators_availability = db.relationship('OperatorsAvailability', back_populates='operator')

# Model per la tabella patients
class Patient(db.Model):
    __tablename__ = 'patients'

    # Colonne
    patient_id = db.Column('patient_id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), unique=True, nullable=False)
    first_name = db.Column('first_name', db.String(255), nullable=False)
    last_name = db.Column('last_name', db.String(255), nullable=False)
    date_of_birth = db.Column('date_of_birth', db.Date, nullable=False)
    fiscal_code = db.Column('fiscal_code', db.String(255), unique=True, nullable=False)
    address = db.Column('address', db.String(255))

# Model per la tabella operators_availability
class OperatorsAvailability(db.Model):
    __tablename__ = 'operators_availability'

    # Colonne
    availability_id = db.Column('availability_id', db.Integer, primary_key=True)
    exam_type_id = db.Column('exam_type_id', db.Integer, db.ForeignKey('exam_types.exam_type_id'), nullable=False)
    laboratory_id = db.Column('laboratory_id', db.Integer, db.ForeignKey('laboratories.laboratory_id'), nullable=False)
    operator_id = db.Column('operator_id', db.Integer, db.ForeignKey('operators.operator_id'), nullable=False)
    available_from_date = db.Column('available_from_date', db.Date, nullable=False)
    available_to_date = db.Column('available_to_date', db.Date, nullable=False)
    available_from_time = db.Column('available_from_time', db.Time, nullable=False)
    available_to_time = db.Column('available_to_time', db.Time, nullable=False)
    available_weekday = db.Column('available_weekday', db.Integer, nullable=False)
    slot_duration_minutes = db.Column('slot_duration_minutes', db.Integer, nullable=False)
    pause_minutes = db.Column('pause_minutes', db.Integer, nullable=False)
    enabled = db.Column('enabled', db.Boolean, default=True, nullable=False)

    # Relazione con tabella laboratories
    laboratory = db.relationship('Laboratory', back_populates='operators_availability')

    # Relazione con tabella operators
    operator = db.relationship('Operator', back_populates='operators_availability')


# Model per la tabella laboratory_closures
class LaboratoryClosure(db.Model):
    __tablename__ = 'laboratory_closures'

    # Colonne
    closure_id = db.Column('closure_id', db.Integer, primary_key=True)
    laboratory_id = db.Column('laboratory_id', db.Integer, db.ForeignKey('laboratories.laboratory_id'), nullable=False)
    start_date = db.Column('start_date', db.DateTime, nullable=False)
    end_date = db.Column('end_date', db.DateTime, nullable=False)

# Model per la tabella exam_types
class ExamType(db.Model):
    __tablename__ = 'exam_types'

    # Colonne
    exam_type_id = db.Column('exam_type_id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(255), unique=True, nullable=False)
    description = db.Column('description', db.Text)

    # Relazione con operators_availability
    operators_availability = db.relationship('OperatorsAvailability', backref='exam_type')





# Model per la tabella operator_absences
class OperatorAbsence(db.Model):
    __tablename__ = 'operator_absences'

    # Colonne
    absence_id = db.Column('absence_id', db.Integer, primary_key=True)
    operator_id = db.Column('operator_id', db.Integer, db.ForeignKey('operators.operator_id'), nullable=False)
    start_date = db.Column('start_date', db.DateTime, nullable=False)
    end_date = db.Column('end_date', db.DateTime, nullable=False)


# Model per la tabella slot_bookings
class SlotBooking(db.Model):
    __tablename__ = 'slot_bookings'

    # Colonne
    appointment_id = db.Column('appointment_id', db.Integer, primary_key=True)
    patient_id = db.Column('patient_id', db.Integer, db.ForeignKey('patients.patient_id'))
    availability_id = db.Column('availability_id', db.Integer, db.ForeignKey('operators_availability.availability_id'), nullable=False)
    appointment_datetime = db.Column('appointment_datetime', db.DateTime, nullable=False)
    rejected = db.Column('rejected', db.Boolean, default=False)

    # Relazioni
    patient = db.relationship('Patient', backref='slot_bookings')
    availability = db.relationship('OperatorsAvailability', backref='slot_bookings')