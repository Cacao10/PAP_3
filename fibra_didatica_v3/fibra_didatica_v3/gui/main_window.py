"""
main_window.py
Janela principal — navegação entre os 3 ecrãs.
"""

from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt

from gui.screens.intro_screen import IntroScreen
from gui.screens.simulation_screen import SimulationScreen
from gui.screens.comparison_screen import ComparisonScreen


class MainWindow(QMainWindow):
    def __init__(self, fiber_profiles: dict):
        super().__init__()
        self.setWindowTitle("Simulação Didática de Fibra Óptica")
        self.setMinimumSize(900, 620)
        self.resize(1100, 720)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.intro      = IntroScreen(self._go_simulation)
        self.simulation = SimulationScreen(fiber_profiles)
        self.comparison = ComparisonScreen()

        # injectar navegação
        self.simulation.set_nav(
            on_home=self._go_intro,
            on_compare=self._go_comparison,
        )
        self.comparison.set_nav(on_back=self._go_simulation)

        self.stack.addWidget(self.intro)
        self.stack.addWidget(self.simulation)
        self.stack.addWidget(self.comparison)

        self.stack.setCurrentWidget(self.intro)

    def _go_intro(self):
        self.stack.setCurrentWidget(self.intro)

    def _go_simulation(self):
        self.stack.setCurrentWidget(self.simulation)

    def _go_comparison(self):
        self.comparison.reload()
        self.stack.setCurrentWidget(self.comparison)
