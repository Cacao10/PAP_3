"""
intro_screen.py
Tela inicial — limpa, com imagem, descrição e botão de simulação.
"""

from pathlib import Path

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont

BG      = "#ffffff"
SURFACE = "#f4f4f5"
BORDER  = "#d4d4d8"
TEXT    = "#18181b"
DIM     = "#52525b"
ACCENT  = "#2563eb"

STYLE = f"""
QWidget {{ background: {BG}; color: {TEXT}; font-family: 'Segoe UI', Arial, sans-serif; }}

QPushButton#btnStart {{
    background: {ACCENT};
    color: #fff;
    border: none;
    border-radius: 8px;
    padding: 12px 40px;
    font-size: 15px;
    font-weight: 700;
}}
QPushButton#btnStart:hover  {{ background: #1d4ed8; }}
QPushButton#btnStart:pressed {{ background: #1e40af; }}
"""


class IntroScreen(QWidget):
    def __init__(self, start_callback):
        super().__init__()
        self.start_callback = start_callback
        self.setStyleSheet(STYLE)
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── header ──────────────────────────────────────────────────────────
        header = QWidget()
        header.setStyleSheet(f"background:{SURFACE}; border-bottom:1px solid {BORDER};")
        header.setFixedHeight(52)
        hl = QHBoxLayout(header)
        hl.setContentsMargins(28, 0, 28, 0)
        logo = QLabel("◉  Fibra Simulador")
        logo.setStyleSheet(f"color:{ACCENT}; font-size:15px; font-weight:700;")
        hl.addWidget(logo)
        hl.addStretch()
        root.addWidget(header)

        # ── corpo ────────────────────────────────────────────────────────────
        body = QVBoxLayout()
        body.setContentsMargins(80, 36, 80, 36)
        body.setSpacing(20)
        body.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # título
        title = QLabel("Simulação de Atenuação em Fibras Ópticas")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size:26px; font-weight:700; color:{TEXT};")
        body.addWidget(title)

        # imagem
        img_lbl = QLabel()
        img_lbl.setAlignment(Qt.AlignCenter)
        project_root = Path(__file__).resolve().parents[2]
        img_path = project_root / "assets" / "icons" / "monomodo.png"
        px = QPixmap(str(img_path))
        if not px.isNull():
            img_lbl.setPixmap(px.scaled(320, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            img_lbl.setText("[ imagem da fibra ]")
            img_lbl.setStyleSheet(f"color:{DIM}; font-size:13px;")
        body.addWidget(img_lbl)

        # separador
        sep = QFrame(); sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"color:{BORDER};")
        body.addWidget(sep)

        # texto explicativo
        txt = QLabel(
            "Uma <b>fibra óptica</b> transmite informação através de pulsos de luz "
            "guiados por um núcleo de vidro com índice de refração superior ao do "
            "revestimento (reflexão interna total).<br><br>"
            "Ao contrário do cabo metálico, que atenua o sinal a <b>2 dB/km</b>, "
            "a fibra monomodo perde apenas <b>0,2 dB/km</b> — permitindo distâncias "
            "de dezenas a centenas de km sem repetidores.<br><br>"
            "Neste simulador podes escolher o tipo de fibra, ajustar a distância, "
            "comparar com o cabo metálico, <b>guardar simulações</b> e "
            "<b>compará-las entre si</b>."
        )
        txt.setWordWrap(True)
        txt.setAlignment(Qt.AlignCenter)
        txt.setStyleSheet(f"color:{DIM}; font-size:13px; line-height:1.6;")
        body.addWidget(txt)

        # cards informativos
        cards = QHBoxLayout()
        cards.setSpacing(14)
        for icon, label, val in [
            ("🔵", "Monomodo",     "0,2 dB/km"),
            ("🟢", "Multimodo",    "0,5 dB/km"),
            ("🟠", "Cabo Metálico","2,0 dB/km"),
        ]:
            card = QFrame()
            card.setStyleSheet(
                f"QFrame{{background:{SURFACE};border:1px solid {BORDER};"
                f"border-radius:10px;padding:10px;}}"
            )
            cl = QVBoxLayout(card)
            cl.setSpacing(4)
            cl.setAlignment(Qt.AlignCenter)
            cl.addWidget(_lbl(f"{icon}  {label}", f"font-size:12px;font-weight:600;color:{TEXT};", center=True))
            cl.addWidget(_lbl(val, f"font-size:19px;font-weight:700;color:{ACCENT};", center=True))
            cards.addWidget(card)
        body.addLayout(cards)

        # botão
        btn_row = QHBoxLayout()
        btn_row.setAlignment(Qt.AlignHCenter)
        btn = QPushButton("▶   Iniciar Simulação")
        btn.setObjectName("btnStart")
        btn.setFixedHeight(46)
        btn.setMinimumWidth(210)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(self.start_callback)
        btn_row.addWidget(btn)
        body.addLayout(btn_row)

        root.addLayout(body)
        root.addStretch()


def _lbl(text, style, center=False):
    l = QLabel(text)
    l.setStyleSheet(style)
    if center:
        l.setAlignment(Qt.AlignCenter)
    return l
