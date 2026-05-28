"""
metrics.py
Métricas didáticas para simulação de fibra óptica.

Este módulo fornece métricas simples e intuitivas
para análise do efeito da atenuação do sinal.
"""


class Metrics:
    def __init__(self, initial_power_mw: float):
        """
        Inicializa o módulo de métricas.

        :param initial_power_mw: Potência inicial do sinal (mW)
        """
        self.initial_power_mw = initial_power_mw

    def calculate_metrics(self, output_power_mw: float) -> dict:
        """
        Calcula métricas básicas da transmissão.

        :param output_power_mw: Potência final do sinal (mW)
        :return: Dicionário com métricas simples
        """
        power_loss_mw = self.initial_power_mw - output_power_mw

        loss_percentage = (power_loss_mw / self.initial_power_mw) * 100

        return {
            "potencia_inicial_mw": round(self.initial_power_mw, 3),
            "potencia_final_mw": round(output_power_mw, 3),
            "perda_mw": round(power_loss_mw, 3),
            "perda_percentual": round(loss_percentage, 1),
        }
