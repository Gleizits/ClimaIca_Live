"""
Consulta histórico, evalúa outliers e inserta los registros
limpios en PostgreSQL (con upsert para evitar duplicados, creo que esa era el nombre
debo repasar mis apuntes).
"""

from .db import get_connection
from .outliers import es_outlier


def obtener_historico(conn, distrito: str, campo: str, limite: int = 30) -> list[float]:
    """
    Trae los últimos N valores de un campo numérico para un distrito,
    usados como base para el cálculo de outliers (IQR).
    """

    query = f"""
        SELECT {campo}
        FROM lecturas_clima
        WHERE distrito = %s AND {campo} IS NOT NULL
        ORDER BY fecha_hora DESC
        LIMIT %s;
    """

    with conn.cursor() as cur:
        cur.execute(query, (distrito, limite))
        filas = cur.fetchall()
    return [fila[0] for fila in filas]


def guardar_en_bd(registros: list[dict]) -> None:
    """
    Recibe la lista de registros limpios,
    evalúa si la temperatura es outlier respecto al histórico, y hace
    upsert en lecturas_clima (ignora si ya existe esa combinación de
    distrito y fecha_hora).
    """

    conn = get_connection()
    insertados = 0
    omitidos_duplicados = 0

    try:
        for registro in registros:
            historico_temp = obtener_historico(conn, registro["distrito"], "temperatura")
            temp_es_outlier = es_outlier(registro["temperatura"], historico_temp)

            query = """
                INSERT INTO lecturas_clima
                    (distrito, fecha_hora, temperatura, humedad_relativa,
                     velocidad_viento, precipitacion, temp_es_outlier)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (distrito, fecha_hora) DO NOTHING;
            """
            with conn.cursor() as cur:
                cur.execute(query, (
                    registro["distrito"],
                    registro["fecha_hora"],
                    registro["temperatura"],
                    registro["humedad_relativa"],
                    registro["velocidad_viento"],
                    registro["precipitacion"],
                    temp_es_outlier,
                ))
                if cur.rowcount == 0:
                    omitidos_duplicados += 1
                else:
                    insertados += 1

        conn.commit()
        print(f"Insertados: {insertados} | Duplicados omitidos: {omitidos_duplicados}")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error al guardar en BD: {e}")
        raise

    finally:
        conn.close()
