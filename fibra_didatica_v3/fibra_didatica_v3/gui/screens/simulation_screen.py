"""
simulation_screen.py
Ecrã de simulação — redesenhado com melhor layout e botão Guardar.
"""

import math
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QFrame, QGroupBox, QDialog, QLineEdit,
    QDialogButtonBox, QMessageBox, QSizePolicy,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from core.fiber_model import FiberModel
from core.signal_simulator import SignalSimulator
from core.metrics import Metrics
from core.database import init_db, save_simulation

from gui.widgets.distance_slider import DistanceSlider
from gui.widgets.fiber_selector import FiberSelector

from utils.constants import INITIAL_POWER_MW, METAL_ATTENUATION_DB_PER_KM

# ── Paleta ────────────────────────────────────────────────────────────────────
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

STYLE = f"""
QWidget {{ background:{BG}; color:{TEXT}; font-family:'Segoe UI',Arial,sans-serif; }}
QGroupBox {{
    background:{SURFACE}; border:1px solid {BORDER}; border-radius:8px;
    margin-top:10px; padding:8px;
    font-size:10px; color:{DIM}; font-weight:600; letter-spacing:1px;
}}
QGroupBox::title {{ subcontrol-origin:margin; left:10px; padding:0 4px; }}
QPushButton#btnGuardar {{
    background:{GREEN}; color:#fff; border:none; border-radius:7px;
    padding:10px 22px; font-size:13px; font-weight:700;
}}
QPushButton#btnGuardar:hover {{ background:#15803d; }}
QPushButton#btnVoltar, QPushButton#btnComparar {{
    background:{SURFACE}; color:{TEXT}; border:1px solid {BORDER};
    border-radius:7px; padding:9px 18px; font-size:12px; font-weight:600;
}}
QPushButton#btnVoltar:hover, QPushButton#btnComparar:hover {{
    border-color:{ACCENT}; color:{ACCENT};
}}
"""


class MetricCard(QFrame):
    def __init__(self, label, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            f"QFrame{{background:{BG};border:1px solid {BORDER};border-radius:8px;}}"
        )
        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 8, 12, 8)
        lay.setSpacing(2)
        self._lbl = QLabel(label.upper())
        self._lbl.setStyleSheet(f"color:{DIM};font-size:9px;font-weight:600;letter-spacing:1px;")
        self._val = QLabel("—")
        self._val.setStyleSheet(f"color:{TEXT};font-size:17px;font-weight:700;")
        lay.addWidget(self._lbl)
        lay.addWidget(self._val)

    def set_value(self, text, color=None):
        self._val.setText(text)
        c = color or TEXT
        self._val.setStyleSheet(f"color:{c};font-size:17px;font-weight:700;")


class AttenuationCanvas(FigureCanvas):
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

    def update_plot(self, attenuation, fiber_name, current_dist):
        self.ax.cla()
        self._style()
        d = np.linspace(0, 50, 300)
        pf = INITIAL_POWER_MW * 10 ** (-attenuation * d / 10)
        pm = INITIAL_POWER_MW * 10 ** (-METAL_ATTENUATION_DB_PER_KM * d / 10)
        self.ax.plot(d, pf, color=ACCENT, lw=2, label=fiber_name)
        self.ax.plot(d, pm, color=ORANGE, lw=2, ls="--", label="Cabo Metálico")
        if current_dist > 0:
            cf = INITIAL_POWER_MW * 10 ** (-attenuation * current_dist / 10)
            cm = INITIAL_POWER_MW * 10 ** (-METAL_ATTENUATION_DB_PER_KM * current_dist / 10)
            self.ax.scatter([current_dist], [cf], color=ACCENT, s=55, zorder=5, edgecolors="white", lw=1)
            self.ax.scatter([current_dist], [cm], color=ORANGE, s=55, zorder=5, edgecolors="white", lw=1)
        self.ax.set_xlim(0, 50)
        self.ax.set_ylim(bottom=0)
        self.ax.legend(fontsize=8, facecolor=SURFACE, edgecolor=BORDER, labelcolor=TEXT)
        self.draw()


class SaveDialog(QDialog):
    def __init__(self, suggested, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Guardar Simulação")
        self.setMinimumWidth(340)
        self.setStyleSheet(f"background:{BG};color:{TEXT};font-family:'Segoe UI',Arial;")
        lay = QVBoxLayout(self)
        lay.setSpacing(12)
        lay.addWidget(QLabel("Nome da simulação:"))
        self.edit = QLineEdit(suggested)
        self.edit.setStyleSheet(
            f"border:1px solid {BORDER};border-radius:6px;padding:8px;"
            f"font-size:13px;background:{SURFACE};"
        )
        lay.addWidget(self.edit)
        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        lay.addWidget(btns)

    def get_name(self):
        return self.edit.text().strip()


class SimulationScreen(QWidget):
    def __init__(self, fiber_profiles: dict):
        super().__init__()
        self.fiber_profiles = fiber_profiles
        self.initial_power = INITIAL_POWER_MW
        self.signal_simulator = SignalSimulator(0.5, 0.1)
        self.metrics_calc = Metrics(self.initial_power)
        self._on_home = None
        self._on_compare = None
        self.setStyleSheet(STYLE)

        try:
            init_db()
        except Exception as e:
            pass  # DB indisponível — aviso aparece ao guardar

        self._build()
        self._update()

    def set_nav(self, on_home, on_compare):
        self._on_home = on_home
        self._on_compare = on_compare

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── topbar ──────────────────────────────────────────────────────────
        topbar = QWidget()
        topbar.setStyleSheet(f"background:{SURFACE};border-bottom:1px solid {BORDER};")
        topbar.setFixedHeight(50)
        tl = QHBoxLayout(topbar)
        tl.setContentsMargins(20, 0, 20, 0)
        tl.setSpacing(10)

        btn_back = QPushButton("← Início")
        btn_back.setObjectName("btnVoltar")
        btn_back.setCursor(Qt.PointingHandCursor)
        btn_back.clicked.connect(lambda: self._on_home and self._on_home())
        tl.addWidget(btn_back)

        tl.addStretch()
        t = QLabel("Simulação de Atenuação")
        t.setStyleSheet(f"font-size:14px;font-weight:700;color:{TEXT};")
        tl.addWidget(t)
        tl.addStretch()

        btn_cmp = QPushButton("📊 Comparações")
        btn_cmp.setObjectName("btnComparar")
        btn_cmp.setCursor(Qt.PointingHandCursor)
        btn_cmp.clicked.connect(lambda: self._on_compare and self._on_compare())
        tl.addWidget(btn_cmp)

        root.addWidget(topbar)

        # ── corpo ────────────────────────────────────────────────────────────
        body = QWidget()
        bl = QVBoxLayout(body)
        bl.setContentsMargins(16, 14, 16, 14)
        bl.setSpacing(10)

        # Linha de controlo
        ctrl = QGroupBox("CONFIGURAÇÃO")
        cl = QHBoxLayout(ctrl)
        cl.setSpacing(18)

        # seletor fibra
        fc = QVBoxLayout()
        fc.addWidget(_lbl("Tipo de Fibra", f"font-size:11px;color:{DIM};"))
        self.fiber_selector = FiberSelector(self.fiber_profiles.keys())
        self.fiber_selector.fiber_changed.connect(self._update)
        fc.addWidget(self.fiber_selector)
        self.desc_lbl = QLabel("")
        self.desc_lbl.setWordWrap(True)
        self.desc_lbl.setStyleSheet(f"color:{DIM};font-size:10px;")
        fc.addWidget(self.desc_lbl)
        cl.addLayout(fc, 3)

        vsep = QFrame(); vsep.setFrameShape(QFrame.VLine)
        vsep.setStyleSheet(f"color:{BORDER};"); cl.addWidget(vsep)

        # slider
        dc = QVBoxLayout()
        self.distance_slider = DistanceSlider(0, 50)
        self.distance_slider.distance_changed.connect(self._update)
        dc.addWidget(self.distance_slider)
        cl.addLayout(dc, 4)

        vsep2 = QFrame(); vsep2.setFrameShape(QFrame.VLine)
        vsep2.setStyleSheet(f"color:{BORDER};"); cl.addWidget(vsep2)

        # guardar
        gc = QVBoxLayout(); gc.setAlignment(Qt.AlignCenter)
        self.btn_save = QPushButton("💾  Guardar")
        self.btn_save.setObjectName("btnGuardar")
        self.btn_save.setFixedHeight(40)
        self.btn_save.setCursor(Qt.PointingHandCursor)
        self.btn_save.clicked.connect(self._save)
        gc.addWidget(self.btn_save)
        cl.addLayout(gc, 1)

        bl.addWidget(ctrl)

        # Métricas + gráfico
        mid = QHBoxLayout(); mid.setSpacing(10)

        met_box = QGroupBox("RESULTADOS")
        mg = QGridLayout(met_box)
        mg.setSpacing(8)
        self.c_power   = MetricCard("Potência Final (mW)")
        self.c_loss    = MetricCard("Perda Total (%)")
        self.c_quality = MetricCard("Qualidade")
        self.c_metal   = MetricCard("Potência Metal (mW)")
        mg.addWidget(self.c_power,   0, 0)
        mg.addWidget(self.c_loss,    0, 1)
        mg.addWidget(self.c_quality, 1, 0)
        mg.addWidget(self.c_metal,   1, 1)
        mid.addWidget(met_box, 2)

        chart_box = QGroupBox("GRÁFICO DE ATENUAÇÃO")
        ch = QVBoxLayout(chart_box)
        self.canvas = AttenuationCanvas()
        ch.addWidget(self.canvas)
        mid.addWidget(chart_box, 5)

        bl.addLayout(mid)

        # Descrição da fibra
        info_box = QGroupBox("INFORMAÇÃO DA FIBRA")
        il = QHBoxLayout(info_box)
        self.lbl_trans  = _lbl("", f"color:{DIM};font-size:12px;")
        self.lbl_fibras = _lbl("", f"color:{DIM};font-size:12px;")
        self.lbl_desc2  = _lbl("", f"color:{DIM};font-size:12px;")
        self.lbl_desc2.setWordWrap(True)
        il.addWidget(self.lbl_trans)
        il.addWidget(QFrame())  # spacer visual
        il.addWidget(self.lbl_fibras)
        il.addWidget(self.lbl_desc2, 2)
        bl.addWidget(info_box)

        root.addWidget(body, 1)

    # ── lógica ────────────────────────────────────────────────────────────────

    def _update(self):
        fiber_type = self.fiber_selector.current_fiber()
        profile    = self.fiber_profiles[fiber_type]
        attenuation = profile["attenuation"]
        distance    = self.distance_slider.value()

        optical_model  = FiberModel(self.initial_power, attenuation)
        metal_model    = FiberModel(self.initial_power, METAL_ATTENUATION_DB_PER_KM)
        optical_power  = optical_model.calculate_output_power(distance)
        metal_power    = metal_model.calculate_output_power(distance)
        optical_metrics = self.metrics_calc.calculate_metrics(optical_power)
        metal_metrics   = self.metrics_calc.calculate_metrics(metal_power)
        quality         = self.signal_simulator.evaluate_signal(optical_power)

        self.c_power.set_value(f"{optical_metrics['potencia_final_mw']:.4f}")
        loss = optical_metrics['perda_percentual']
        loss_col = GREEN if loss < 50 else (AMBER if loss < 80 else RED)
        self.c_loss.set_value(f"{loss:.1f}", color=loss_col)
        q_map = {"bom": ("BOM", GREEN), "medio": ("MÉDIO", AMBER), "ruim": ("FRACO", RED)}
        ql, qc = q_map.get(quality, ("—", DIM))
        self.c_quality.set_value(ql, color=qc)
        self.c_metal.set_value(f"{metal_metrics['potencia_final_mw']:.4f}", color=ORANGE)

        self.lbl_trans.setText(f"Transmissão: <b>{profile.get('transmissao','—')}</b>")
        self.lbl_fibras.setText(f"N.º de fibras: <b>{profile.get('fibras','—')}</b>")
        self.lbl_desc2.setText(profile.get("descricao", ""))

        self.canvas.update_plot(attenuation, fiber_type, distance)

        # guardar estado para save
        self._last = {
            "fibra": fiber_type,
            "distancia": distance,
            "potencia_mw": optical_metrics["potencia_final_mw"],
            "perda_pct": loss,
            "qualidade": ql,
        }

    def _save(self):
        if not hasattr(self, "_last"):
            return
        d = self._last
        suggested = f"{d['fibra']} – {d['distancia']} km"
        dlg = SaveDialog(suggested, self)
        if dlg.exec_() != QDialog.Accepted:
            return
        nome = dlg.get_name()
        if not nome:
            QMessageBox.warning(self, "Nome inválido", "Introduz um nome para a simulação.")
            return
        try:
            new_id = save_simulation(
                nome, d["fibra"], d["distancia"],
                d["potencia_mw"], d["perda_pct"], d["qualidade"]
            )
            QMessageBox.information(self, "Guardado",
                f"✅ Simulação «{nome}» guardada! (ID: {new_id})")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível guardar:\n{e}")


def _lbl(text, style, center=False):
    l = QLabel(text)
    l.setStyleSheet(style)
    if center:
        l.setAlignment(Qt.AlignCenter)
    return l
