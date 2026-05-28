from PyQt5.QtWidgets import QLabel


class SignalIndicator(QLabel):
    def __init__(self):
        super().__init__()
        self.setText("Sinal: -")

    def update_quality(self, quality):
        if quality == "bom":
            self.setText("Sinal: BOM")
            self.setStyleSheet("color: green; font-weight: bold;")
        elif quality == "medio":
            self.setText("Sinal: MÉDIO")
            self.setStyleSheet("color: orange; font-weight: bold;")
        else:
            self.setText("Sinal: RUIM")
            self.setStyleSheet("color: red; font-weight: bold;")