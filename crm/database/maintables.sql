CREATE TABLE BD_versicherungsunternehmen (
    id SERIAL PRIMARY KEY,
    mandantkuerzel VARCHAR(10) NOT NULL,
    mandantenname VARCHAR(255) NOT NULL,
    parent_id INT REFERENCES BD_versicherungsunternehmen(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_mandantkuerzel ON BD_versicherungsunternehmen (mandantkuerzel);

CREATE TABLE Kontaktperson (
    id SERIAL PRIMARY KEY,
    versicherungsunternehmen_id INT REFERENCES BD_versicherungsunternehmen(id),
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_versicherungsunternehmen_id ON Kontaktperson (versicherungsunternehmen_id); 