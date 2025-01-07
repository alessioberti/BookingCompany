-- Creazione della tabella Utenti
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    pwdhash VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    failedcount INT DEFAULT 0,
    locked BOOLEAN DEFAULT 0
);
