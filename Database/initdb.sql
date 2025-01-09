--Tabella Login Utenti
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email_address VARCHAR(255) NOT NULL UNIQUE,
    tel_number VARCHAR(255)NOT NULL UNIQUE
);

--Tabella Pazienti
CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL UNIQUE REFERENCES users(user_id) ON DELETE CASCADE,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    fiscal_code VARCHAR(255) NOT NULL UNIQUE,
    address VARCHAR(255)
);

--Tabella Operatori
CREATE TABLE operators (
    operator_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL UNIQUE REFERENCES users(user_id) ON DELETE CASCADE,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    address VARCHAR(255)
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

--Tabella disponibilità operatori
CREATE TABLE operators_availability(
    availability_id SERIAL PRIMARY KEY,
    exam_type_id INT NOT NULL REFERENCES exam_types(exam_type_id) ON DELETE CASCADE,
    laboratory_id INT NOT NULL REFERENCES laboratories(laboratory_id) ON DELETE CASCADE,
    operator_id INT  NOT NULL REFERENCES operators(operator_id) ON DELETE CASCADE,
    available_from_date DATE NOT NULL CHECK (available_to_date >= available_from_date),
    available_to_date DATE NOT NULL CHECK (available_from_date <= available_to_date),
    available_from_time TIME NOT NULL CHECK (available_to_time > available_from_time),
    available_to_time TIME NOT NULL CHECK (available_from_time < available_to_time),
    available_weekday INT NOT NULL CHECK(available_weekday IN (0,1,2,3,4,5,6)),
    slot_duration_minutes INT NOT NULL CHECK(slot_duration_minutes IN (10,20,30,40,50,60)),
    pause_minutes INT NOT NULL CHECK(pause_minutes IN (0,5,10,15,20,25,30)),
    enabled BOOLEAN DEFAULT TRUE
);

--Tabella Chiusure Laboratori
CREATE TABLE laboratory_closures (
    closure_id SERIAL PRIMARY KEY,
    laboratory_id INT NOT NULL REFERENCES laboratories(laboratory_id) ON DELETE CASCADE,
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date TIMESTAMP WITH TIME ZONE NOT NULL CHECK(end_date >= start_date)
);

--Tabella Assenze Operatori
CREATE TABLE operator_absences (
    absence_id SERIAL PRIMARY KEY,
    operator_id INT NOT NULL REFERENCES operators(operator_id) ON DELETE CASCADE,
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date TIMESTAMP WITH TIME ZONE NOT NULL CHECK(end_date >= start_date)
);

--Tabella Prenotazioni
CREATE TABLE slot_bookings (
    appointment_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL REFERENCES patients(patient_id) ON DELETE SET NULL,
    availability_id INT NOT NULL REFERENCES operators_availability(availability_id) ON DELETE CASCADE,
    appointment_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    rejected BOOLEAN DEFAULT FALSE
);


INSERT INTO users (username, password_hash, email_address, tel_number)
VALUES
('mrossi', 'hashpassword1', 'marco.rossi@example.com', '3401234567'),
('gverdi', 'hashpassword2', 'giulia.verdi@example.com', '3402345678'),
('albianchi', 'hashpassword3', 'alessandro.bianchi@example.com', '3403456789'),
('esantini', 'hashpassword4', 'elena.santini@example.com', '3404567890'),
('clombardi', 'hashpassword5', 'carlo.lombardi@example.com', '3405678901');

INSERT INTO patients (user_id, first_name, last_name, date_of_birth, fiscal_code, address)
VALUES
(1, 'Marco', 'Rossi', '1985-06-15', 'RSSMRC85H15F205Z', 'Via Roma 1, Milano'),
(2, 'Giulia', 'Verdi', '1992-09-20', 'VRDGLL92S20H501K', 'Corso Venezia 3, Roma'),
(3, 'Alessandro', 'Bianchi', '1988-03-12', 'BNCALS88C12L219M', 'Piazza Garibaldi 7, Torino'),
(4, 'Elena', 'Santini', '1990-01-05', 'SNTLNE90A45H703P', 'Via Dante 9, Firenze'),
(5, 'Carlo', 'Lombardi', '1983-12-25', 'LMBCRL83T25L219N', 'Via Manzoni 4, Bologna');

INSERT INTO operators (user_id, first_name, last_name, role, address)
VALUES
(1, 'Marco', 'Rossi', 'Medico', 'Via Roma 1, Milano'),
(2, 'Giulia', 'Verdi', 'Tecnico', 'Corso Venezia 3, Roma'),
(3, 'Alessandro', 'Bianchi', 'Tecnico', 'Piazza Garibaldi 7, Torino'),
(4, 'Elena', 'Santini', 'Medico', 'Via Dante 9, Firenze'),
(5, 'Carlo', 'Lombardi', 'Assistente', 'Via Manzoni 4, Bologna');

INSERT INTO laboratories (name, address, contact_info)
VALUES
('Laboratorio Milano', 'Via Milano 10, Milano', 'info.milano@laboratori.it'),
('Laboratorio Roma', 'Via Appia 20, Roma', 'info.roma@laboratori.it'),
('Laboratorio Torino', 'Corso Italia 15, Torino', 'info.torino@laboratori.it'),
('Laboratorio Firenze', 'Piazza Duomo 5, Firenze', 'info.firenze@laboratori.it'),
('Laboratorio Bologna', 'Via Marconi 12, Bologna', 'info.bologna@laboratori.it');

INSERT INTO exam_types (name, description)
VALUES
('Esame del Sangue', 'Analisi completa del sangue'),
('Risonanza Magnetica', 'Esame di diagnostica per immagini'),
('TAC', 'Tomografia assiale computerizzata'),
('Ecografia', 'Esame ecografico generale'),
('Visita Medica', 'Visita specialistica');

INSERT INTO operators_availability 
(exam_type_id, laboratory_id, operator_id, available_from_date, available_to_date, 
available_from_time, available_to_time, available_weekday, slot_duration_minutes, pause_minutes, enabled)
VALUES
(1, 1, 1, '2025-01-01', '2025-12-31', '08:00:00', '16:00:00', 1, 30, 10, TRUE),
(2, 2, 2, '2025-01-01', '2025-12-31', '09:00:00', '17:00:00', 3, 20, 5, TRUE),
(3, 3, 3, '2025-01-01', '2025-12-31', '10:00:00', '18:00:00', 5, 40, 15, TRUE),
(4, 4, 4, '2025-01-01', '2025-12-31', '08:00:00', '12:00:00', 2, 30, 10, TRUE),
(5, 5, 5, '2025-01-01', '2025-12-31', '13:00:00', '19:00:00', 4, 60, 20, TRUE);

INSERT INTO laboratory_closures (laboratory_id, start_date, end_date)
VALUES
(1, '2025-08-01 08:00:00+01', '2025-08-15 18:00:00+01'),
(2, '2025-12-24 08:00:00+01', '2025-12-26 18:00:00+01'),
(3, '2025-01-06 08:00:00+01', '2025-01-06 18:00:00+01');

INSERT INTO operator_absences (operator_id, start_date, end_date)
VALUES
(1, '2025-03-01 08:00:00+01', '2025-03-10 18:00:00+01'),
(2, '2025-07-15 08:00:00+01', '2025-07-20 18:00:00+01'),
(4, '2025-11-01 08:00:00+01', '2025-11-05 18:00:00+01');

INSERT INTO slot_bookings (patient_id, availability_id, appointment_datetime, rejected)
VALUES
(1, 1, '2025-01-10 08:30:00+01', FALSE),
(2, 2, '2025-01-15 09:20:00+01', TRUE),
(3, 3, '2025-02-10 10:40:00+01', FALSE),
(4, 4, '2025-03-05 08:30:00+01', FALSE),
(5, 5, '2025-04-12 14:30:00+01', FALSE);
