--query_exploratory_registres_number.sql
SELECT
    cliente_id,
    COUNT(*) AS cantidad_registros_por_cliente
FROM historial_mensual
GROUP BY cliente_id
HAVING COUNT(DISTINCT mes) = 6
LIMIT 5;
