"""
attenuation_plot.py
Gráfico didático de atenuação embutido na interface.
"""

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class AttenuationPlot(FigureCanvas):
    def __init__(self):
        self.figure = Figure(figsize=(5, 3))
        self.ax = self.figure.add_subplot(111)

        super().__init__(self.figure)

        self.ax.set_xlabel("Distância (km)")
        self.ax.set_ylabel("Potência (mW)")
        self.ax.set_title("Atenuação do sinal na fibra óptica")
        self.ax.grid(True)

    def update_plot(self, distances, powers):
        self.ax.clear()
        self.ax.plot(distances, powers)
        self.ax.set_xlabel("Distância (km)")
        self.ax.set_ylabel("Potência (mW)")
        self.ax.set_title("Atenuação do sinal na fibra óptica")
        self.ax.grid(True)

        self.draw()
