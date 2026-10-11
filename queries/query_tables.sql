-- query_tables.sql
SELECT
    name,
    sql
FROM sqlite_master
WHERE type = 'table';
