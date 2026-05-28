from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QSlider
from PyQt5.QtCore import Qt, pyqtSignal


class DistanceSlider(QWidget):
    distance_changed = pyqtSignal(int)

    def __init__(self, minimum=0, maximum=50):
        super().__init__()

        self.label = QLabel(f"Distância: {minimum} km")

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(minimum, maximum)
        self.slider.valueChanged.connect(self._on_value_changed)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.slider)

        self.setLayout(layout)

    def _on_value_changed(self, value):
        self.label.setText(f"Distância: {value} km")
        self.distance_changed.emit(value)

    def value(self):
        return self.slider.value()