EXPLAIN ANALYZE
SELECT 
    parent.id AS parent_id,
    parent.mandantenname AS parent_name,
    subsidiary.id AS subsidiary_id,
    subsidiary.mandantenname AS subsidiary_name,
    kp.name AS kontaktperson_name,
    kp.email AS kontaktperson_email,
    kp.phone AS kontaktperson_phone
FROM 
    bd_versicherungsunternehmen parent
LEFT JOIN 
    bd_versicherungsunternehmen subsidiary ON subsidiary.parent_id = parent.id
LEFT JOIN 
    kontaktperson kp ON kp.versicherungsunternehmen_id = subsidiary.id;
