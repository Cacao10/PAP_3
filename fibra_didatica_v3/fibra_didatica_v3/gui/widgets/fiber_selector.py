from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QComboBox
from PyQt5.QtCore import pyqtSignal


class FiberSelector(QWidget):
    fiber_changed = pyqtSignal(str)

    def __init__(self, fiber_types):
        super().__init__()

        self.label = QLabel("Tipo de fibra:")

        self.combo_box = QComboBox()
        self.combo_box.addItems(fiber_types)
        self.combo_box.currentTextChanged.connect(self.fiber_changed.emit)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.combo_box)

        self.setLayout(layout)

    def current_fiber(self):
        return self.combo_box.currentText()