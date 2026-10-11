-- query_exploratory_historial_mensual.sql
SELECT
    cliente_id,
    1 AS mes_1,
    MAX(CASE WHEN mes = 1 THEN estado_pago END) AS estado_pago_mes_1,
    MAX(CASE WHEN mes = 1 THEN monto_facturado END) AS monto_facturado_mes_1,
    MAX(CASE WHEN mes = 1 THEN monto_pagado END) AS pago_mes_1,
    2 AS mes_2,
    MAX(CASE WHEN mes = 2 THEN estado_pago END) AS estado_pago_mes_2,
    MAX(CASE WHEN mes = 2 THEN monto_facturado END) AS monto_facturado_mes_2,
    MAX(CASE WHEN mes = 2 THEN monto_pagado END) AS pago_mes_2,
    3 AS mes_3,
    MAX(CASE WHEN mes = 3 THEN estado_pago END) AS estado_pago_mes_3,
    MAX(CASE WHEN mes = 3 THEN monto_facturado END) AS monto_facturado_mes_3,
    MAX(CASE WHEN mes = 3 THEN monto_pagado END) AS pago_mes_3,
    4 AS mes_4,
    MAX(CASE WHEN mes = 4 THEN estado_pago END) AS estado_pago_mes_4,
    MAX(CASE WHEN mes = 4 THEN monto_facturado END) AS monto_facturado_mes_4,
    MAX(CASE WHEN mes = 4 THEN monto_pagado END) AS pago_mes_4,
    5 AS mes_5,
    MAX(CASE WHEN mes = 5 THEN estado_pago END) AS estado_pago_mes_5,
    MAX(CASE WHEN mes = 5 THEN monto_facturado END) AS monto_facturado_mes_5,
    MAX(CASE WHEN mes = 5 THEN monto_pagado END) AS pago_mes_5,
    6 AS mes_6,
    MAX(CASE WHEN mes = 6 THEN estado_pago END) AS estado_pago_mes_6,
    MAX(CASE WHEN mes = 6 THEN monto_facturado END) AS monto_facturado_mes_6,
    MAX(CASE WHEN mes = 6 THEN monto_pagado END) AS pago_mes_6
FROM historial_mensual
GROUP BY cliente_id
LIMIT 5;
