"""
Orquesta el pipeline completo: extract -> transform -> load.
"""

from src.extract import obtener_clima_distritos
from src.transform import limpiar_datos
from src.load import guardar_en_bd
from src.db import crear_tabla


def ejecutar_pipeline():
    print("Iniciando pipeline.....")

    crear_tabla()  # no hace nada si la tabla ya existe

    datos_crudos = obtener_clima_distritos()
    datos_limpios = limpiar_datos(datos_crudos)

    if not datos_limpios:
        print("No se obtuvieron registros válidos.")
        return

    guardar_en_bd(datos_limpios)
    print("Pipeline completado.\n")


if __name__ == "__main__":
    ejecutar_pipeline()
