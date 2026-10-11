#data/external/generate_collection_db.py
"""
Genera cobranza.db (SQLite) a partir de UCI_Credit_Card.csv (Kaggle:
Default of Credit Card Clients Dataset).

Normaliza el CSV "ancho" en dos tablas relacionadas:

    clientes
        cliente_id, edad, sexo, educacion, estado_civil,
        limite_credito, default_pago

    historial_mensual
        cliente_id, mes, estado_pago, monto_facturado, monto_pagado

Uso:
    1. Descarga UCI_Credit_Card.csv de Kaggle y ponlo en la misma
       carpeta que este script (o ajusta CSV_PATH abajo).
    2. Ejecuta:  python generar_cobranza_db.py
    3. Se crea cobranza.db en la misma carpeta.
"""

import sqlite3
import pandas as pd

CSV_PATH = "UCI_Credit_Card.csv"
DB_PATH = "cobranza.db"

# Los meses van de más reciente (0/sept) a más antiguo (6/abril).
# Los mapeamos a un número de mes 1-6 para que sea más natural
# trabajar con ellos en SQL (mes 1 = más antiguo, mes 6 = más reciente).
COLUMNAS_MES = [
    # (sufijo_original, numero_mes_normalizado)
    ("6", 1),  # abril 2005
    ("5", 2),  # mayo 2005
    ("4", 3),  # junio 2005
    ("3", 4),  # julio 2005
    ("2", 5),  # agosto 2005
    ("0", 6),  # septiembre 2005  (ojo: esta columna es PAY_0, no PAY_1)
]


def construir_tabla_clientes(df: pd.DataFrame) -> pd.DataFrame:
    clientes = df[["ID", "AGE", "SEX", "EDUCATION", "MARRIAGE",
                    "LIMIT_BAL", "default.payment.next.month"]].copy()
    clientes.columns = ["cliente_id", "edad", "sexo", "educacion",
                         "estado_civil", "limite_credito", "default_pago"]
    return clientes


def construir_tabla_historial(df: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for sufijo, mes in COLUMNAS_MES:
        pay_col = f"PAY_{sufijo}"
        bill_col = f"BILL_AMT{ {'6':1,'5':2,'4':3,'3':4,'2':5,'0':6}[sufijo] }"
        # BILL_AMT y PAY_AMT sí van de 1 a 6 (sin columna "0"),
        # así que su índice normalizado coincide con el mismo mes.
        idx = {'6': 6, '5': 5, '4': 4, '3': 3, '2': 2, '0': 1}[sufijo]
        bill_col = f"BILL_AMT{idx}"
        payamt_col = f"PAY_AMT{idx}"

        parte = df[["ID", pay_col, bill_col, payamt_col]].copy()
        parte.columns = ["cliente_id", "estado_pago",
                          "monto_facturado", "monto_pagado"]
        parte["mes"] = mes
        filas.append(parte)

    historial = pd.concat(filas, ignore_index=True)
    historial = historial[["cliente_id", "mes", "estado_pago",
                            "monto_facturado", "monto_pagado"]]
    historial = historial.sort_values(["cliente_id", "mes"]).reset_index(drop=True)
    return historial


def main():
    print(f"Leyendo {CSV_PATH} ...")
    df = pd.read_csv(CSV_PATH)

    print("Construyendo tabla 'clientes' ...")
    clientes = construir_tabla_clientes(df)

    print("Construyendo tabla 'historial_mensual' (esto puede tardar un poco) ...")
    historial = construir_tabla_historial(df)

    print(f"Escribiendo {DB_PATH} ...")
    conn = sqlite3.connect(DB_PATH)
    clientes.to_sql("clientes", conn, if_exists="replace", index=False)
    historial.to_sql("historial_mensual", conn, if_exists="replace", index=False)

    conn.execute("CREATE INDEX IF NOT EXISTS idx_hist_cliente ON historial_mensual(cliente_id);")
    conn.commit()
    conn.close()

    print("\nListo. Resumen:")
    print(f"  clientes:          {len(clientes)} filas")
    print(f"  historial_mensual: {len(historial)} filas")
    print(f"\nAbre {DB_PATH} con cualquier cliente SQLite (DB Browser, sqlite3 CLI, "
          f"o pd.read_sql en Python) para practicar tus consultas.")


if __name__ == "__main__":
    main()
