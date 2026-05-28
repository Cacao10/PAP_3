"""
signal_simulator.py
Simulador didático da qualidade do sinal óptico.

Este módulo interpreta a potência final do sinal
e classifica sua qualidade de forma simples e visual.
"""


class SignalSimulator:
    def __init__(self, good_threshold_mw: float, medium_threshold_mw: float):
        """
        Inicializa os limites de qualidade do sinal.

        :param good_threshold_mw: Potência mínima para sinal bom (mW)
        :param medium_threshold_mw: Potência mínima para sinal médio (mW)
        """
        self.good_threshold_mw = good_threshold_mw
        self.medium_threshold_mw = medium_threshold_mw

    def evaluate_signal(self, output_power_mw: float) -> str:
        """
        Avalia a qualidade do sinal com base na potência final.

        :param output_power_mw: Potência final do sinal (mW)
        :return: Qualidade do sinal ("bom", "medio", "ruim")
        """
        if output_power_mw >= self.good_threshold_mw:
            return "bom"
        elif output_power_mw >= self.medium_threshold_mw:
            return "medio"
        else:
            return "ruim"
