SELECT 
    table_name, 
    pg_size_pretty(pg_total_relation_size(table_name::regclass)) AS total_size
FROM 
    information_schema.tables
WHERE 
    table_schema = 'public'
ORDER BY 
    pg_total_relation_size(table_name::regclass) DESC;
