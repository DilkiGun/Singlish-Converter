"""Application entry point for Singlish Studio."""

from __future__ import annotations

import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from singlish_converter import __app_name__, __version__
from singlish_converter.assets import get_asset_path
from singlish_converter.settings import AppSettings
from singlish_converter.ui.main_window import MainWindow


def main() -> int:
    """Launch the Singlish Studio desktop application."""
    app = QApplication(sys.argv)
    app.setApplicationName(__app_name__)
    app.setApplicationVersion(__version__)
    app.setStyle("Fusion")

    icon_path = get_asset_path("app_icon.png")
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    settings = AppSettings.load()
    window = MainWindow(settings=settings)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
