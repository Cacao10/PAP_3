"""
fiber_model.py
Modelo didático de fibra óptica para ensino técnico.

Este módulo simula a atenuação do sinal óptico
em função da distância percorrida na fibra.
"""

import math


class FiberModel:
    def __init__(self, initial_power_mw: float, attenuation_db_km: float):
        """
        Inicializa o modelo da fibra.

        :param initial_power_mw: Potência inicial do sinal (mW)
        :param attenuation_db_km: Atenuação da fibra (dB/km)
        """
        self.initial_power_mw = initial_power_mw
        self.attenuation_db_km = attenuation_db_km

    def calculate_output_power(self, distance_km: float) -> float:
        """
        Calcula a potência final do sinal após percorrer a fibra.

        Fórmula usada:
        P = P0 * 10^(-α * d / 10)

        :param distance_km: Distância da fibra (km)
        :return: Potência final do sinal (mW)
        """
        attenuation_total_db = self.attenuation_db_km * distance_km

        output_power = self.initial_power_mw * math.pow(
            10, -attenuation_total_db / 10
        )

        return output_power
