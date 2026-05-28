import sys
import json
import os
from PyQt5.QtWidgets import QApplication

from gui.main_window import MainWindow



def load_fiber_profiles():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    with open(
        os.path.join(BASE_DIR, "config", "fiber_profiles.json"),
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def main():
    app = QApplication(sys.argv)

    fiber_profiles = load_fiber_profiles()

    window = MainWindow(fiber_profiles)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
