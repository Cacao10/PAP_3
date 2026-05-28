"""
comparison_screen.py
Ecrã de comparação — simulações guardadas na DB + tabela fibra vs metal.
"""

from pathlib import Path
import numpy as np

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QGroupBox, QFrame, QScrollArea, QSizePolicy,
    QMessageBox, QTabWidget,
)
from PyQt5.QtCore import Qt

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from core.database import load_all_simulations, delete_simulation
from utils.constants import INITIAL_POWER_MW, METAL_ATTENUATION_DB_PER_KM

BG      = "#ffffff"
SURFACE = "#f4f4f5"
BORDER  = "#d4d4d8"
TEXT    = "#18181b"
DIM     = "#52525b"
ACCENT  = "#2563eb"
GREEN   = "#16a34a"
AMBER   = "#d97706"
RED     = "#dc2626"
ORANGE  = "#ea580c"

COLORS = ["#2563eb","#16a34a","#ea580c","#7c3aed","#d97706","#0891b2","#be185d","#65a30d"]

FIBER_ATTEN = {
    "Monomodo Simplex": 0.2, "Monomodo Duplex": 0.2,
    "Multimodo Simplex": 0.5, "Multimodo Duplex": 0.5,
}

STYLE = f"""
QWidget {{ background:{BG}; color:{TEXT}; font-family:'Segoe UI',Arial,sans-serif; }}
QTabWidget::pane {{ border:1px solid {BORDER}; border-radius:8px; background:{BG}; }}
QTabBar::tab {{
    background:{SURFACE}; border:1px solid {BORDER}; border-bottom:none;
    border-radius:6px 6px 0 0; padding:8px 20px; font-size:12px;
}}
QTabBar::tab:selected {{ background:{BG}; color:{ACCENT}; font-weight:700; }}
QListWidget {{
    background:{SURFACE}; border:1px solid {BORDER}; border-radius:8px; outline:none;
}}
QListWidget::item {{ padding:10px 12px; border-bottom:1px solid {BORDER}; }}
QListWidget::item:selected {{ background:#dbeafe; color:#1d4ed8; }}
QListWidget::item:hover {{ background:#eff6ff; }}
QGroupBox {{
    background:{SURFACE}; border:1px solid {BORDER}; border-radius:8px;
    margin-top:10px; padding:8px;
    font-size:10px; color:{DIM}; font-weight:600; letter-spacing:1px;
}}
QGroupBox::title {{ subcontrol-origin:margin; left:10px; padding:0 4px; }}
QPushButton#btnVoltar, QPushButton#btnReload {{
    background:{SURFACE}; color:{TEXT}; border:1px solid {BORDER};
    border-radius:7px; padding:8px 18px; font-size:12px; font-weight:600;
}}
QPushButton#btnVoltar:hover, QPushButton#btnReload:hover {{
    border-color:{ACCENT}; color:{ACCENT};
}}
QPushButton#btnDelete {{
    background:#fee2e2; color:{RED}; border:1px solid #fca5a5;
    border-radius:7px; padding:8px 18px; font-size:12px; font-weight:600;
}}
QPushButton#btnDelete:hover {{ background:#fecaca; }}
QPushButton#btnCompare {{
    background:{ACCENT}; color:#fff; border:none;
    border-radius:7px; padding:8px 18px; font-size:12px; font-weight:700;
}}
QPushButton#btnCompare:hover {{ background:#1d4ed8; }}
"""


class ComparisonPlot(FigureCanvas):
    def __init__(self):
        self.fig = Figure(figsize=(6, 3), facecolor=BG)
        super().__init__(self.fig)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ax = self.fig.add_subplot(111)
        self._style()

    def _style(self):
        self.ax.set_facecolor(SURFACE)
        self.ax.tick_params(colors=DIM, labelsize=8)
        for s in self.ax.spines.values():
            s.set_edgecolor(BORDER)
        self.ax.set_xlabel("Distância (km)", color=DIM, fontsize=9)
        self.ax.set_ylabel("Potência (mW)", color=DIM, fontsize=9)
        self.ax.grid(True, color=BORDER, lw=0.5, ls="--", alpha=0.7)
        self.fig.tight_layout(pad=1.2)

    def draw_comparison(self, sims):
        self.ax.cla(); self._style()
        if not sims:
            self.ax.text(0.5, 0.5, "Seleciona simulações para comparar",
                         transform=self.ax.transAxes, ha="center", va="center",
                         color=DIM, fontsize=11)
            self.draw(); return
        max_d = max(s["distancia_km"] for s in sims)
        d = np.linspace(0, max(max_d * 1.2, 10), 400)
        for i, sim in enumerate(sims):
            col = COLORS[i % len(COLORS)]
            a = FIBER_ATTEN.get(sim["fibra"], 0.2)
            p = INITIAL_POWER_MW * 10 ** (-a * d / 10)
            self.ax.plot(d, p, color=col, lw=2,
                         label=f"{sim['nome']} ({sim['distancia_km']:.0f}km)")
            pf = INITIAL_POWER_MW * 10 ** (-a * sim["distancia_km"] / 10)
            self.ax.scatter([sim["distancia_km"]], [pf], color=col,
                            s=55, zorder=5, edgecolors="white", lw=1)
        pm = INITIAL_POWER_MW * 10 ** (-METAL_ATTENUATION_DB_PER_KM * d / 10)
        self.ax.plot(d, pm, color=ORANGE, lw=1.5, ls=":", label="Cabo Metálico (ref.)")
        self.ax.set_xlim(0, max(max_d * 1.2, 10)); self.ax.set_ylim(bottom=0)
        self.ax.legend(fontsize=8, facecolor=SURFACE, edgecolor=BORDER, labelcolor=TEXT)
        self.draw()


class ComparisonScreen(QWidget):
    def __init__(self):
        super().__init__()
        self._sims = []
        self._on_back = None
        self.setStyleSheet(STYLE)
        self._build()

    def set_nav(self, on_back):
        self._on_back = on_back

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # topbar
        topbar = QWidget()
        topbar.setStyleSheet(f"background:{SURFACE};border-bottom:1px solid {BORDER};")
        topbar.setFixedHeight(50)
        tl = QHBoxLayout(topbar)
        tl.setContentsMargins(20, 0, 20, 0); tl.setSpacing(10)
        btn_back = QPushButton("← Simulação")
        btn_back.setObjectName("btnVoltar")
        btn_back.setCursor(Qt.PointingHandCursor)
        btn_back.clicked.connect(lambda: self._on_back and self._on_back())
        tl.addWidget(btn_back)
        tl.addStretch()
        tl.addWidget(_lbl("Comparação de Simulações", f"font-size:14px;font-weight:700;color:{TEXT};"))
        tl.addStretch()
        btn_rel = QPushButton("🔄 Recarregar")
        btn_rel.setObjectName("btnReload")
        btn_rel.setCursor(Qt.PointingHandCursor)
        btn_rel.clicked.connect(self.reload)
        tl.addWidget(btn_rel)
        root.addWidget(topbar)

        # tabs
        body = QWidget()
        bl = QVBoxLayout(body)
        bl.setContentsMargins(14, 12, 14, 12)
        tabs = QTabWidget()

        # ── aba 1: simulações guardadas ──────────────────────────────────────
        tab1 = QWidget()
        t1 = QHBoxLayout(tab1)
        t1.setSpacing(12)

        # lista
        left = QVBoxLayout(); left.setSpacing(8)
        left.addWidget(_lbl("Simulações guardadas", f"font-size:11px;font-weight:600;color:{DIM};"))
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        self.list_widget.itemSelectionChanged.connect(self._on_select)
        left.addWidget(self.list_widget, 1)
        btns = QHBoxLayout()
        self.btn_cmp = QPushButton("📊  Comparar")
        self.btn_cmp.setObjectName("btnCompare")
        self.btn_cmp.setCursor(Qt.PointingHandCursor)
        self.btn_cmp.clicked.connect(self._compare)
        btns.addWidget(self.btn_cmp)
        self.btn_del = QPushButton("🗑  Apagar")
        self.btn_del.setObjectName("btnDelete")
        self.btn_del.setCursor(Qt.PointingHandCursor)
        self.btn_del.clicked.connect(self._delete)
        btns.addWidget(self.btn_del)
        left.addLayout(btns)
        t1.addLayout(left, 1)

        # direito: gráfico + cards
        right = QVBoxLayout(); right.setSpacing(10)
        chart_box = QGroupBox("CURVAS DE ATENUAÇÃO")
        ch = QVBoxLayout(chart_box)
        self.plot = ComparisonPlot()
        ch.addWidget(self.plot)
        right.addWidget(chart_box, 3)

        cards_box = QGroupBox("DETALHES")
        self.cards_scroll = QScrollArea()
        self.cards_scroll.setWidgetResizable(True)
        self.cards_scroll.setStyleSheet("border:none;background:transparent;")
        self.cards_inner = QWidget()
        self.cards_inner.setStyleSheet(f"background:{SURFACE};")
        self.cards_layout = QHBoxLayout(self.cards_inner)
        self.cards_layout.setSpacing(10)
        self.cards_layout.setAlignment(Qt.AlignLeft)
        self.cards_scroll.setWidget(self.cards_inner)
        QVBoxLayout(cards_box).addWidget(self.cards_scroll)
        right.addWidget(cards_box, 2)
        t1.addLayout(right, 3)

        tabs.addTab(tab1, "Simulações Guardadas")

        # ── aba 2: tabela fibra vs metal ─────────────────────────────────────
        tab2 = QWidget()
        t2l = QVBoxLayout(tab2)
        t2l.setContentsMargins(20, 20, 20, 20)
        t2l.setSpacing(16)

        t2l.addWidget(_lbl("Fibra Óptica  ×  Cabo Metálico",
                           f"font-size:18px;font-weight:700;color:{TEXT};", center=True))
        t2l.addWidget(_lbl(
            "Comparação das principais características entre os dois meios de transmissão.",
            f"font-size:12px;color:{DIM};", center=True))

        table_data = [
            ("Atenuação típica",    "0,2 – 0,5 dB/km",         "2,0 dB/km"),
            ("Velocidade",          "Muito alta (luz)",          "Limitada (elétrica)"),
            ("Imunidade EMI",       "Total (dielétrico)",        "Suscetível"),
            ("Distância máxima",    "Dezenas a centenas de km",  "Poucos km"),
            ("Largura de banda",    "Muito alta (THz)",          "Baixa"),
            ("Peso",                "Leve",                      "Pesado"),
            ("Instalação",          "Requer cuidado",            "Mais simples"),
            ("Uso atual",           "Internet, data centers",    "Redes locais curtas"),
        ]

        # cabeçalho
        hdr = QFrame()
        hdr.setStyleSheet(f"background:{SURFACE};border:1px solid {BORDER};border-radius:8px;")
        hl = QHBoxLayout(hdr); hl.setContentsMargins(12, 8, 12, 8)
        for txt, w in [("Característica", 3), ("Fibra Óptica", 2), ("Cabo Metálico", 2)]:
            l = _lbl(txt, f"font-size:11px;font-weight:700;color:{DIM};")
            hl.addWidget(l, w)
        t2l.addWidget(hdr)

        for i, (car, fib, met) in enumerate(table_data):
            row = QFrame()
            bg = BG if i % 2 == 0 else SURFACE
            row.setStyleSheet(f"background:{bg};border:1px solid {BORDER};border-radius:6px;")
            rl = QHBoxLayout(row); rl.setContentsMargins(12, 8, 12, 8)
            rl.addWidget(_lbl(car,  f"font-size:12px;color:{TEXT};font-weight:600;"), 3)
            rl.addWidget(_lbl(fib,  f"font-size:12px;color:{GREEN};"), 2)
            rl.addWidget(_lbl(met,  f"font-size:12px;color:{ORANGE};"), 2)
            t2l.addWidget(row)

        t2l.addStretch()
        tabs.addTab(tab2, "Fibra vs Cabo Metálico")

        bl.addWidget(tabs)
        root.addWidget(body, 1)

    def reload(self):
        try:
            self._sims = load_all_simulations()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível carregar simulações:\n{e}")
            self._sims = []
        self.list_widget.clear()
        for sim in self._sims:
            ts = str(sim.get("criado_em", ""))[:16]
            item = QListWidgetItem(
                f"[{sim['id']}]  {sim['nome']}  —  {sim['fibra']} · {sim['distancia_km']:.1f} km  ({ts})"
            )
            item.setData(Qt.UserRole, sim["id"])
            self.list_widget.addItem(item)
        self.plot.draw_comparison([])
        self._clear_cards()

    def _get_selected(self):
        ids = {item.data(Qt.UserRole) for item in self.list_widget.selectedItems()}
        return [s for s in self._sims if s["id"] in ids]

    def _on_select(self):
        self._compare()

    def _compare(self):
        sims = self._get_selected()
        self.plot.draw_comparison(sims)
        self._clear_cards()
        if not sims:
            self.cards_layout.addWidget(
                _lbl("Seleciona simulações na lista para ver detalhes.",
                     f"color:{DIM};font-size:12px;padding:12px;"))
            return
        for i, sim in enumerate(sims):
            col = COLORS[i % len(COLORS)]
            card = QFrame()
            card.setStyleSheet(
                f"QFrame{{background:{BG};border:2px solid {col};border-radius:8px;}}"
            )
            cl = QVBoxLayout(card); cl.setContentsMargins(12, 10, 12, 10); cl.setSpacing(4)
            cl.addWidget(_lbl(f"● {sim['nome']}",
                              f"color:{col};font-size:12px;font-weight:700;"))
            for lbl, val in [
                ("Fibra",      sim["fibra"]),
                ("Distância",  f"{sim['distancia_km']:.1f} km"),
                ("Potência",   f"{sim['potencia_mw']:.5f} mW"),
                ("Perda",      f"{sim['perda_pct']:.1f} %"),
                ("Qualidade",  sim["qualidade"]),
                ("Guardado",   str(sim.get("criado_em", ""))[:16]),
            ]:
                r = QHBoxLayout()
                r.addWidget(_lbl(lbl, f"color:{DIM};font-size:10px;"))
                r.addStretch()
                r.addWidget(_lbl(val, f"color:{TEXT};font-size:11px;font-weight:600;"))
                cl.addLayout(r)
            self.cards_layout.addWidget(card)

    def _clear_cards(self):
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _delete(self):
        sims = self._get_selected()
        if not sims:
            QMessageBox.information(self, "Apagar", "Seleciona pelo menos uma simulação.")
            return
        names = "\n".join(f"• {s['nome']}" for s in sims)
        if QMessageBox.question(self, "Confirmar",
                                f"Apagar {len(sims)} simulação(ões)?\n\n{names}",
                                QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes:
            return
        for sim in sims:
            try:
                delete_simulation(sim["id"])
            except Exception as e:
                QMessageBox.critical(self, "Erro", str(e))
        self.reload()


def _lbl(text, style, center=False):
    l = QLabel(text)
    l.setStyleSheet(style)
    if center:
        l.setAlignment(Qt.AlignCenter)
    return l
