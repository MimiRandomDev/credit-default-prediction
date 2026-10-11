-- query_exploratory_clientes.sql
SELECT
    cliente_id,
    edad,
    sexo,
    educacion,
    estado_civil,
    limite_credito,
    default_pago
FROM clientes
LIMIT 5
