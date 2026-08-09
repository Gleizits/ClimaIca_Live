"""
Extrae datos climáticos en tiempo real de Open-Meteo
para los distritos de la provincia de Ica.
"""

import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Distritos de Ica: nombre, latitud, longitud
DISTRITOS = [
    {"nombre": "Ica",              "lat": -14.0678, "lon": -75.7286},
    {"nombre": "Parcona",          "lat": -14.0453, "lon": -75.6889},
    {"nombre": "La Tinguiña",      "lat": -14.0342, "lon": -75.7208},
    {"nombre": "Santiago",         "lat": -14.1594, "lon": -75.7075},
    {"nombre": "Subtanjalla",      "lat": -14.0197, "lon": -75.7683},
    {"nombre": "Salas",            "lat": -14.0631, "lon": -75.6486},
    {"nombre": "Los Aquijes",      "lat": -14.1097, "lon": -75.6742},
    {"nombre": "Pueblo Nuevo",     "lat": -14.0872, "lon": -75.7469},
    {"nombre": "San Juan Bautista","lat": -14.1417, "lon": -75.7375},
    {"nombre": "Tate",             "lat": -14.1289, "lon": -75.6597},
    {"nombre": "Pachacútec",       "lat": -13.9867, "lon": -75.8058},
]

BASE_URL = "https://api.open-meteo.com/v1/forecast"

VARIABLES_ACTUALES = [
    "temperature_2m",
    "relative_humidity_2m",
    "wind_speed_10m",
    "precipitation",
]


def obtener_clima_distritos() -> list[dict]:
    """
    Llama a Open-Meteo pidiendo todos los distritos en una sola petición
    (lat/lon como listas separadas por comas) y devuelve una lista de
    diccionarios "crudos", uno por distrito.
    """
    latitudes = ",".join(str(d["lat"]) for d in DISTRITOS)
    longitudes = ",".join(str(d["lon"]) for d in DISTRITOS)

    params = {
        "latitude": latitudes,
        "longitude": longitudes,
        "current": ",".join(VARIABLES_ACTUALES),
        "timezone": "America/Lima",
    }

    respuesta = requests.get(BASE_URL, params=params, timeout=15)
    respuesta.raise_for_status()  # lanza error si la API responde con status != 200

    data = respuesta.json()

    """
    Cuando pides varias ubicaciones, Open-Meteo devuelve una LISTA,
    en el mismo orden en que las mandaste.
    """

    if isinstance(data, dict):
        data = [data]

    resultados = []
    for distrito, resultado_api in zip(DISTRITOS, data):
        resultados.append({
            "distrito": distrito["nombre"],
            "raw": resultado_api,
        })

    return resultados


if __name__ == "__main__":
    # Prueba rápida
    datos = obtener_clima_distritos()
    for item in datos:
        print(item["distrito"], "->", item["raw"].get("current"))
