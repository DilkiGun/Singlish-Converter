"""Asset path resolution for development and PyInstaller frozen builds."""

from __future__ import annotations

import sys
from pathlib import Path


def get_base_dir() -> Path:
    """Return the application base directory (handles PyInstaller _MEIPASS)."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)  # type: ignore[attr-defined]
    return Path(__file__).resolve().parent.parent.parent


def get_asset_path(relative_path: str) -> Path:
    """Resolve a path inside the project's assets directory."""
    return get_base_dir() / "assets" / relative_path
