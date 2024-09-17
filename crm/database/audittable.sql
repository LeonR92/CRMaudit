CREATE TABLE bd_versicherungsunternehmen_audit (
    id SERIAL PRIMARY KEY,
    versicherungsunternehmen_id INT,
    mandantkuerzel VARCHAR(10),
    mandantenname VARCHAR(255),
    parent_id INT,
    operation_type VARCHAR(10),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
