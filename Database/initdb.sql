--Tabella Login Utenti
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email_address VARCHAR(255) NOT NULL UNIQUE
);

--Tabella Pazienti
CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL UNIQUE REFERENCES users(user_id) ON DELETE CASCADE,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    FC VARCHAR(255) NOT NULL,
    contact_info VARCHAR(255)
);

--Tabella Operatori
CREATE TABLE operators (
    operator_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL UNIQUE REFERENCES users(user_id) ON DELETE CASCADE,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    contact_info VARCHAR(255)
);

--Tabella Laboratori
CREATE TABLE laboratories (
    laboratory_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    contact_info VARCHAR(255)
);

--Tabella Tipi di Esame
CREATE TABLE exam_types (
    exam_type_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT
);

--Tabella Esami Prenotabili e Regole di Prenotazione
CREATE TABLE exams (
    exam_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    exam_type_id INT NOT NULL REFERENCES exam_types(exam_type_id) ON DELETE CASCADE,
    laboratory_id INT NOT NULL REFERENCES laboratories(laboratory_id) ON DELETE CASCADE,
    operator_id INT REFERENCES operators(operator_id) ON DELETE CASCADE,
    is_available BOOLEAN DEFAULT TRUE,
    available_from DATE,
    available_to DATE,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    slot_duration INT NOT NULL CHECK(slot_duration IN (10,20,30,40,50,60,70,80,90,100,110)),
    pause_minutes INT NOT NULL CHECK(pause_minutes IN (0,5,10,15,20,25,30)),
    weekday INT NOT NULL CHECK(weekday IN (0,1,2,3,4,5,6))
);

--Tabella Chiusure Laboratori
CREATE TABLE laboratory_closures (
    closure_id SERIAL PRIMARY KEY,
    laboratory_id INT NOT NULL REFERENCES laboratories(laboratory_id) ON DELETE CASCADE,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL CHECK(end_date >= start_date)
);

--Tabella Assenze Operatori
CREATE TABLE operator_absences (
    absence_id SERIAL PRIMARY KEY,
    operator_id INT NOT NULL REFERENCES operators(operator_id) ON DELETE CASCADE,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL CHECK(end_date >= start_date)
);

--Tabella Prenotazioni
CREATE TABLE bookings (
    appointment_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    exam_id INT NOT NULL REFERENCES exams(exam_id) ON DELETE CASCADE,
    appointment_date TIMESTAMP NOT NULL,
    appointment_time TIME NOT NULL,
    status VARCHAR(50) DEFAULT 'confirmed'
);
