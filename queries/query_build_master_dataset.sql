-- query_build_master_dataset.sql
SELECT
    cs.edad, cs.sexo, cs.educacion,
    cs.estado_civil, cs.limite_credito, cs.default_pago,
    hm.*
FROM clientes cs
JOIN (
    SELECT
        cliente_id,
        MAX(CASE WHEN mes = 1 THEN estado_pago END) AS estado_pago_mes_1,
        MAX(CASE WHEN mes = 1 THEN monto_facturado END) AS monto_facturado_mes_1,
        MAX(CASE WHEN mes = 1 THEN monto_pagado END) AS pago_mes_1,
        MAX(CASE WHEN mes = 2 THEN estado_pago END) AS estado_pago_mes_2,
        MAX(CASE WHEN mes = 2 THEN monto_facturado END) AS monto_facturado_mes_2,
        MAX(CASE WHEN mes = 2 THEN monto_pagado END) AS pago_mes_2,
        MAX(CASE WHEN mes = 3 THEN estado_pago END) AS estado_pago_mes_3,
        MAX(CASE WHEN mes = 3 THEN monto_facturado END) AS monto_facturado_mes_3,
        MAX(CASE WHEN mes = 3 THEN monto_pagado END) AS pago_mes_3,
        MAX(CASE WHEN mes = 4 THEN estado_pago END) AS estado_pago_mes_4,
        MAX(CASE WHEN mes = 4 THEN monto_facturado END) AS monto_facturado_mes_4,
        MAX(CASE WHEN mes = 4 THEN monto_pagado END) AS pago_mes_4,
        MAX(CASE WHEN mes = 5 THEN estado_pago END) AS estado_pago_mes_5,
        MAX(CASE WHEN mes = 5 THEN monto_facturado END) AS monto_facturado_mes_5,
        MAX(CASE WHEN mes = 5 THEN monto_pagado END) AS pago_mes_5,
        MAX(CASE WHEN mes = 6 THEN estado_pago END) AS estado_pago_mes_6,
        MAX(CASE WHEN mes = 6 THEN monto_facturado END) AS monto_facturado_mes_6,
        MAX(CASE WHEN mes = 6 THEN monto_pagado END) AS pago_mes_6
    FROM historial_mensual
    GROUP BY cliente_id
) hm
ON cs.cliente_id = hm.cliente_id
ORDER BY hm.cliente_id DESC;
