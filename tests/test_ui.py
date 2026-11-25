"""Headless Qt UI smoke tests for Singlish Studio."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from singlish_converter.settings import AppSettings
from singlish_converter.ui.main_window import MainWindow


def _get_qapp() -> QApplication:
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_mainwindow_live_conversion_and_settings(tmp_path: Path) -> None:
    _get_qapp()
    cfg = tmp_path / "settings.json"
    settings = AppSettings(minimize_to_tray=False)
    win = MainWindow(settings=settings, settings_path=cfg)

    win._input_edit.setPlainText("aayuboevan `Python`")
    assert win._output_edit.toPlainText() == "ආයුබෝවන් Python"

    # Toggle backtick mode off
    win._backtick_btn.setChecked(False)
    assert "`" in win._output_edit.toPlainText()

    # Save snapshot to history
    win._save_snapshot()
    assert len(win.settings.history) == 1

    win._force_quit = True
    win.close()

    reloaded = AppSettings.load(cfg)
    assert reloaded.preserve_backticks is False
    assert len(reloaded.history) == 1
