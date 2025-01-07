-- Tabella Login Utenti
CREATE TABLE Users (
    User_ID SERIAL PRIMARY KEY,
    Username VARCHAR(255) NOT NULL UNIQUE,
    Password_Hash VARCHAR(255) NOT NULL,
    Email_Address VARCHAR(255) NOT NULL UNIQUE
);

-- Tabella Pazienti
CREATE TABLE Patients (
    Patient_ID SERIAL PRIMARY KEY,
    First_Name VARCHAR(255) NOT NULL,
    Last_Name VARCHAR(255) NOT NULL,
    Date_of_Birth DATE NOT NULL,
    Tax_Code VARCHAR(16) UNIQUE,
    Contact_Info VARCHAR(255)
);

-- Tabella Operatori
CREATE TABLE Operators (
    Operator_ID SERIAL PRIMARY KEY,
    First_Name VARCHAR(255) NOT NULL,
    Last_Name VARCHAR(255) NOT NULL,
    Role VARCHAR(255) NOT NULL,
    Contact_Info VARCHAR(255)
);

-- Tabella Laboratori
CREATE TABLE Laboratories (
    Laboratory_ID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Address VARCHAR(255),
    Contact_Info VARCHAR(255)
);

-- Tabella Tipi di Esame
CREATE TABLE Exam_Types (
    Exam_Type_ID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL UNIQUE,
    Description TEXT
);

-- Tabella Esami Prenotabili e Regole di Prenotazione
CREATE TABLE Exams (
    Exam_ID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Description TEXT,
    Exam_Type_ID INT NOT NULL REFERENCES Exam_Types(Exam_Type_ID) ON DELETE CASCADE,
    Laboratory_ID INT NOT NULL REFERENCES Laboratories(Laboratory_ID) ON DELETE CASCADE,
    Operator_ID INT REFERENCES Operators(Operator_ID) ON DELETE SET NULL,
    Is_Available BOOLEAN DEFAULT TRUE,
    Avaiable_From DATE,
    Avaiable_To DATE,
    Opening_Time TIME NOT NULL,
    Closing_Time TIME NOT NULL,
    Slot_Duration INT NOT NULL,
    Buffer_Time INT NOT NULL,
    Weekday VARCHAR(50) NOT NULL CHECK(Weekday IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')),
);

-- Tabella Chiusure Laboratori
CREATE TABLE Laboratory_Closures (
    Closure_ID SERIAL PRIMARY KEY,
    Laboratory_ID INT NOT NULL REFERENCES Laboratories(Laboratory_ID) ON DELETE CASCADE,
    Start_Date TIMESTAMP NOT NULL,
    End_Date TIMESTAMP NOT NULL
);

-- Tabella Assenze Operatori
CREATE TABLE Operator_Absences (
    Absence_ID SERIAL PRIMARY KEY,
    Operator_ID INT NOT NULL REFERENCES Operators(Operator_ID) ON DELETE CASCADE,
    Start_Date TIMESTAMP NOT NULL,
    End_Date TIMESTAMP NOT NULL
);

-- Tabella Chiusure Laboratori
CREATE TABLE Laboratory_Closures (
    Closure_ID SERIAL PRIMARY KEY,
    Laboratory_ID INT NOT NULL REFERENCES Laboratories(Laboratory_ID) ON DELETE CASCADE,
    Start_Date TIMESTAMP NOT NULL,
    End_Date TIMESTAMP NOT NULL
);

-- Tabella Assenze Operatori
CREATE TABLE Operator_Absences (
    Absence_ID SERIAL PRIMARY KEY,
    Operator_ID INT NOT NULL REFERENCES Operators(Operator_ID) ON DELETE CASCADE,
    Start_Date TIMESTAMP NOT NULL,
    End_Date TIMESTAMP NOT NULL
);

-- Tabella Prenotazioni
CREATE TABLE Bookings (
    Appointment_ID SERIAL PRIMARY KEY,
    Patient_ID INT NOT NULL REFERENCES Patients(Patient_ID) ON DELETE CASCADE,
    Exam_ID INT NOT NULL REFERENCES Exams(Exam_ID) ON DELETE CASCADE,
    Appointment_Date TIMESTAMP NOT NULL,
    Appointment_Time TIME NOT NULL,
    Status VARCHAR(50) DEFAULT 'Confirmed' 
);
