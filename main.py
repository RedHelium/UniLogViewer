from PyQt6.QtWidgets import (
    QApplication,
)
import sys

from internal.styles.theme_loader import load_qss
from internal.utils.log_viewer import LogViewer


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(load_qss("material_dark.qss"))

    viewer = LogViewer()
    viewer.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
