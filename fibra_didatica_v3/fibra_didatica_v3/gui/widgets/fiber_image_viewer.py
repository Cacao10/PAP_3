from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class FiberImageViewer(QLabel):
    """Widget responsável por apresentar a imagem da fibra selecionada."""

    def __init__(self, width=300, height=180):
        super().__init__()
        self.width = width
        self.height = height

        self.setAlignment(Qt.AlignCenter)
        self.setMinimumHeight(height)
        self.setText("Imagem da fibra")

    def update_image(self, fiber_type):
        fiber_type = fiber_type.lower().strip()

        if "mono" in fiber_type:
            image_name = "monomodo.png"
        elif "multi" in fiber_type:
            image_name = "multimodo.png"
        else:
            self.clear()
            self.setText("Tipo de fibra desconhecido")
            return

        project_root = Path(__file__).resolve().parents[2]
        image_path = project_root / "assets" / "icons" / image_name

        if not image_path.exists():
            self.clear()
            self.setText(f"Imagem não encontrada:\n{image_path}")
            return

        pixmap = QPixmap(str(image_path))

        if pixmap.isNull():
            self.clear()
            self.setText(f"Não foi possível carregar:\n{image_path.name}")
            return

        pixmap = pixmap.scaled(
            self.width,
            self.height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )

        self.clear()
        self.setPixmap(pixmap)
