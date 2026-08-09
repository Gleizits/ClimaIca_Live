"""
Crea la tabla lecturas_clima en PostgreSQL si no existe.
Se corre una sola vez (o cada vez que main.py arranca, la verdad nose, no crea si ya existe, comprobado).
"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def crear_tabla():
    query = """
    CREATE TABLE IF NOT EXISTS lecturas_clima (
        id SERIAL PRIMARY KEY,
        distrito VARCHAR(50) NOT NULL,
        fecha_hora TIMESTAMP NOT NULL,
        temperatura NUMERIC,
        humedad_relativa NUMERIC,
        velocidad_viento NUMERIC,
        precipitacion NUMERIC,
        temp_es_outlier BOOLEAN DEFAULT FALSE,
        creado_en TIMESTAMP DEFAULT NOW(),
        UNIQUE (distrito, fecha_hora)
    );
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query)
        conn.commit()
        print("Tabla 'lecturas_clima' lista.")
    finally:
        conn.close()


if __name__ == "__main__":
    crear_tabla()
