"""Modern Dark and Light QSS themes plus Windows titlebar integration."""

from __future__ import annotations

import ctypes
import sys
from PySide6.QtWidgets import QWidget


DARK_PALETTE = {
    "bg_root": "#0B1120",
    "bg_surface": "#111827",
    "bg_card": "#162032",
    "bg_elevated": "#1E293B",
    "bg_input": "#0F172A",
    "border": "#263348",
    "border_focus": "#14B8A6",
    "text_primary": "#F1F5F9",
    "text_secondary": "#94A3B8",
    "text_muted": "#64748B",
    "accent": "#0D9488",
    "accent_hover": "#14B8A6",
    "accent_pressed": "#0F766E",
    "accent_soft": "rgba(20, 184, 166, 0.14)",
    "accent_text": "#5EEAD4",
    "sinhala_text": "#E2E8F0",
    "danger": "#EF4444",
    "danger_soft": "rgba(239, 68, 68, 0.14)",
    "badge_bg": "#1E293B",
}

LIGHT_PALETTE = {
    "bg_root": "#F1F5F9",
    "bg_surface": "#FFFFFF",
    "bg_card": "#FFFFFF",
    "bg_elevated": "#F8FAFC",
    "bg_input": "#F8FAFC",
    "border": "#CBD5E1",
    "border_focus": "#0D9488",
    "text_primary": "#0F172A",
    "text_secondary": "#475569",
    "text_muted": "#64748B",
    "accent": "#0D9488",
    "accent_hover": "#0F766E",
    "accent_pressed": "#115E59",
    "accent_soft": "rgba(13, 148, 136, 0.10)",
    "accent_text": "#0F766E",
    "sinhala_text": "#0F172A",
    "danger": "#DC2626",
    "danger_soft": "rgba(220, 38, 38, 0.10)",
    "badge_bg": "#E2E8F0",
}


def build_stylesheet(theme_name: str) -> str:
    p = DARK_PALETTE if theme_name == "dark" else LIGHT_PALETTE
    return f"""
    QMainWindow, QWidget#RootWidget {{
        background-color: {p["bg_root"]};
        color: {p["text_primary"]};
        font-family: "Segoe UI", "Nirmala UI", sans-serif;
        font-size: 10pt;
    }}

    QWidget#HeaderBar {{
        background-color: {p["bg_surface"]};
        border-bottom: 1px solid {p["border"]};
    }}

    QWidget#KeyBar {{
        background-color: {p["bg_surface"]};
        border-bottom: 1px solid {p["border"]};
    }}

    QFrame#CardPanel {{
        background-color: {p["bg_card"]};
        border: 1px solid {p["border"]};
        border-radius: 12px;
    }}

    QFrame#SidePanel {{
        background-color: {p["bg_surface"]};
        border: 1px solid {p["border"]};
        border-radius: 12px;
    }}

    QLabel#AppTitle {{
        font-size: 13pt;
        font-weight: 700;
        color: {p["text_primary"]};
    }}

    QLabel#AppSubtitle {{
        font-size: 8.5pt;
        color: {p["text_secondary"]};
    }}

    QLabel#CardTitle {{
        font-size: 10.5pt;
        font-weight: 600;
        color: {p["text_primary"]};
    }}

    QLabel#MutedLabel {{
        font-size: 8.5pt;
        color: {p["text_secondary"]};
    }}

    QLabel#WordHintBadge {{
        background-color: {p["accent_soft"]};
        color: {p["accent_text"]};
        border: 1px solid {p["border_focus"]};
        border-radius: 8px;
        padding: 3px 10px;
        font-size: 9.5pt;
        font-weight: 600;
    }}

    QLabel#CodepointBar {{
        background-color: {p["bg_elevated"]};
        color: {p["text_secondary"]};
        border: 1px solid {p["border"]};
        border-radius: 6px;
        padding: 4px 8px;
        font-family: "Consolas", "Cascadia Mono", monospace;
        font-size: 8.5pt;
    }}

    QPlainTextEdit, QTextEdit {{
        background-color: {p["bg_input"]};
        color: {p["text_primary"]};
        border: 1px solid {p["border"]};
        border-radius: 8px;
        padding: 10px;
        selection-background-color: {p["accent"]};
        selection-color: #FFFFFF;
    }}

    QPlainTextEdit:focus, QTextEdit:focus {{
        border: 1.5px solid {p["border_focus"]};
    }}

    QPlainTextEdit#SinhalaEditor {{
        color: {p["sinhala_text"]};
    }}

    QLineEdit {{
        background-color: {p["bg_input"]};
        color: {p["text_primary"]};
        border: 1px solid {p["border"]};
        border-radius: 7px;
        padding: 6px 10px;
    }}

    QLineEdit:focus {{
        border: 1.5px solid {p["border_focus"]};
    }}

    QPushButton {{
        background-color: {p["bg_elevated"]};
        color: {p["text_primary"]};
        border: 1px solid {p["border"]};
        border-radius: 7px;
        padding: 6px 12px;
        font-weight: 500;
    }}

    QPushButton:hover {{
        border-color: {p["border_focus"]};
        background-color: {p["accent_soft"]};
    }}

    QPushButton:pressed {{
        background-color: {p["accent_pressed"]};
        color: #FFFFFF;
    }}

    QPushButton:checked {{
        background-color: {p["accent_soft"]};
        color: {p["accent_text"]};
        border: 1px solid {p["border_focus"]};
        font-weight: 600;
    }}

    QPushButton#PrimaryButton {{
        background-color: {p["accent"]};
        color: #FFFFFF;
        border: none;
        font-weight: 600;
        padding: 7px 16px;
    }}

    QPushButton#PrimaryButton:hover {{
        background-color: {p["accent_hover"]};
    }}

    QPushButton#PrimaryButton:pressed {{
        background-color: {p["accent_pressed"]};
    }}

    QPushButton#DangerButton {{
        background-color: transparent;
        color: {p["danger"]};
        border: 1px solid {p["border"]};
    }}

    QPushButton#DangerButton:hover {{
        background-color: {p["danger_soft"]};
        border-color: {p["danger"]};
    }}

    QPushButton#QuickChip {{
        background-color: {p["bg_elevated"]};
        color: {p["text_primary"]};
        border: 1px solid {p["border"]};
        border-radius: 6px;
        padding: 3px 8px;
        font-size: 9pt;
    }}

    QPushButton#QuickChip:hover {{
        background-color: {p["accent_soft"]};
        border-color: {p["border_focus"]};
        color: {p["accent_text"]};
    }}

    QPushButton#SchemeTile {{
        background-color: {p["bg_elevated"]};
        border: 1px solid {p["border"]};
        border-radius: 8px;
        padding: 6px;
        text-align: center;
    }}

    QPushButton#SchemeTile:hover {{
        background-color: {p["accent_soft"]};
        border-color: {p["border_focus"]};
    }}

    QComboBox, QSpinBox {{
        background-color: {p["bg_elevated"]};
        color: {p["text_primary"]};
        border: 1px solid {p["border"]};
        border-radius: 7px;
        padding: 4px 8px;
    }}

    QComboBox::drop-down {{
        border: none;
        width: 20px;
    }}

    QComboBox QAbstractItemView {{
        background-color: {p["bg_card"]};
        color: {p["text_primary"]};
        border: 1px solid {p["border"]};
        selection-background-color: {p["accent"]};
    }}

    QSplitter::handle {{
        background-color: transparent;
    }}

    QSplitter::handle:horizontal {{
        width: 8px;
    }}

    QSplitter::handle:vertical {{
        height: 8px;
    }}

    QScrollArea {{
        border: none;
        background-color: transparent;
    }}

    QScrollBar:vertical {{
        background: transparent;
        width: 8px;
        margin: 2px;
    }}

    QScrollBar::handle:vertical {{
        background: {p["border"]};
        border-radius: 4px;
        min-height: 24px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: {p["text_muted"]};
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    QStatusBar {{
        background-color: {p["bg_surface"]};
        color: {p["text_secondary"]};
        border-top: 1px solid {p["border"]};
        font-size: 8.5pt;
    }}

    QMenu {{
        background-color: {p["bg_card"]};
        color: {p["text_primary"]};
        border: 1px solid {p["border"]};
        padding: 4px;
    }}

    QMenu::item {{
        padding: 6px 18px;
        border-radius: 4px;
    }}

    QMenu::item:selected {{
        background-color: {p["accent"]};
        color: #FFFFFF;
    }}
    """


def apply_windows_titlebar_theme(window: QWidget, dark: bool) -> None:
    """Enable Windows 10/11 immersive dark mode on the native window frame."""
    if sys.platform != "win32":
        return
    try:
        hwnd = int(window.winId())
        value = ctypes.c_int(1 if dark else 0)
        # DWMWA_USE_IMMERSIVE_DARK_MODE = 20 (Win 10 20H1+ / Win 11), fallback 19
        dwmapi = ctypes.windll.dwmapi
        res = dwmapi.DwmSetWindowAttribute(
            hwnd, 20, ctypes.byref(value), ctypes.sizeof(value)
        )
        if res != 0:
            dwmapi.DwmSetWindowAttribute(
                hwnd, 19, ctypes.byref(value), ctypes.sizeof(value)
            )
    except Exception:
        pass
