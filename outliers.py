"""
Detección de valores atípicos usando el método de
cajas y bigotes (rango intercuartíl / IQR).
"""

import numpy as np


def calcular_limites_iqr(valores: list[float]) -> tuple[float, float]:
    """
    Calcula los límites inferior y superior según el método de Tukey
    (cajas y bigotes): Q1 - 1.5*IQR y Q3 + 1.5*IQR.
    Cualquier valor fuera de este rango se considera atípico.
    """

    q1 = np.percentile(valores, 25)
    q3 = np.percentile(valores, 75)
    iqr = q3 - q1

    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr

    return limite_inferior, limite_superior


def es_outlier(valor: float, historico: list[float]) -> bool:
    """
    Determina si valor es un outlier respecto al histórico dado.
    Necesita al menos ~5 valores históricos para que el cálculo
    tenga sentido estadístico.
    """

    if len(historico) < 5:
        return False  # sin suficiente historia, no podemos evaluar

    limite_inf, limite_sup = calcular_limites_iqr(historico)
    return valor < limite_inf or valor > limite_sup
