"""Persistent user preferences and conversion history storage."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


def get_config_dir() -> Path:
    """Return per-user AppData directory for Singlish Studio."""
    override = os.environ.get("SINGLISH_STUDIO_CONFIG_DIR")
    if override:
        base = Path(override)
        base.mkdir(parents=True, exist_ok=True)
        return base

    appdata = os.environ.get("APPDATA")
    candidates = [
        Path(appdata) / "SinglishStudio" if appdata else Path.home() / ".singlish_studio",
        Path.home() / ".singlish_studio",
    ]
    for base in candidates:
        try:
            base.mkdir(parents=True, exist_ok=True)
            return base
        except OSError:
            continue
    raise PermissionError("Unable to create configuration directory.")


@dataclass
class HistoryItem:
    """A saved Singlish -> Sinhala conversion snapshot."""

    timestamp: str
    singlish: str
    sinhala: str


@dataclass
class AppSettings:
    """Serializable application preferences."""

    theme: str = "dark"
    font_family: str = "Nirmala UI"
    font_size: int = 18
    input_font_size: int = 13
    preserve_backticks: bool = True
    live_convert: bool = True
    auto_copy: bool = False
    always_on_top: bool = False
    minimize_to_tray: bool = True
    split_orientation: str = "horizontal"
    scheme_panel_visible: bool = False
    history: list[dict[str, str]] = field(default_factory=list)

    @classmethod
    def load(cls, path: Path | None = None) -> "AppSettings":
        try:
            target = path or (get_config_dir() / "settings.json")
        except OSError:
            return cls()
        if not target.exists():
            return cls()
        try:
            raw: dict[str, Any] = json.loads(target.read_text(encoding="utf-8"))
            valid_fields = {f for f in cls.__dataclass_fields__}
            filtered = {k: v for k, v in raw.items() if k in valid_fields}
            return cls(**filtered)
        except Exception:
            return cls()

    def save(self, path: Path | None = None) -> None:
        target = path or (get_config_dir() / "settings.json")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json.dumps(asdict(self), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def add_history(self, singlish: str, sinhala: str, max_items: int = 50) -> None:
        s_clean = singlish.strip()
        o_clean = sinhala.strip()
        if not s_clean or not o_clean:
            return
        # Deduplicate consecutive identical entries
        if self.history and self.history[0].get("sinhala") == o_clean:
            return
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "singlish": singlish,
            "sinhala": sinhala,
        }
        self.history.insert(0, entry)
        self.history = self.history[:max_items]
