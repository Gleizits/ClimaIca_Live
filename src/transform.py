"""
Limpia y estructura los datos crudos de Open-Meteo
antes de cargarlos a PostgreSQL.
"""

from datetime import datetime


def limpiar_datos(datos_crudos: list[dict]) -> list[dict]:
    """
    Recibe la lista que devuelve extract.obtener_clima_distritos()
    y devuelve una lista de diccionarios con datos limpios, uno por distrito,
    con solo los campos que van a la base de datos.
    """

    registros_limpios = []

    for item in datos_crudos:
        distrito = item["distrito"]
        current = item["raw"].get("current")

        # Si un distrito vino sin datos "current" (falla de la API),
        # lo saltamos en vez de romper todo el pipeline.
        if not current:
            print(f"Sin datos 'current' para {distrito}, se omite.")
            continue

        try:
            registro = {
                "distrito": distrito,
                "fecha_hora": formatear_fecha(current.get("time")),
                "temperatura": current.get("temperature_2m"),
                "humedad_relativa": current.get("relative_humidity_2m"),
                "velocidad_viento": current.get("wind_speed_10m"),
                "precipitacion": current.get("precipitation"),
            }
        except (TypeError, ValueError) as e:
            print(f"Error transformando datos de {distrito}: {e}")
            continue

        # Validación mínima: sin fecha_hora o sin temperatura, el registro
        # no sirve de nada.
        if registro["fecha_hora"] is None or registro["temperatura"] is None:
            print(f"Registro incompleto para {distrito}, se omite.")
            continue

        registros_limpios.append(registro)

    return registros_limpios


def formatear_fecha(fecha_str: str | None) -> datetime | None:

    """
    Convierte el string de fecha que devuelve Open-Meteo
    (formato ISO, ejemplo: 2026-08-09T00:00) a un objeto datetime de Python.
    """

    if not fecha_str:
        return None
    return datetime.fromisoformat(fecha_str)


if __name__ == "__main__":
    # Prueba manual: encadena extract -> transform y muestra el resultado
    from extract import obtener_clima_distritos

    crudos = obtener_clima_distritos()
    limpios = limpiar_datos(crudos)

    for registro in limpios:
        print(registro)
