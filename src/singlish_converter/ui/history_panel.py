"""Conversion history drawer for restoring or copying previous translations."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class HistoryPanel(QFrame):
    """Displays saved Singlish -> Sinhala history entries with restore/copy."""

    restore_requested = Signal(str)
    copy_requested = Signal(str)
    clear_requested = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("SidePanel")
        self._items: list[dict[str, str]] = []
        self._filter = ""

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(10)

        header = QHBoxLayout()
        title = QLabel("Conversion History")
        title.setObjectName("CardTitle")
        clear_btn = QPushButton("Clear All")
        clear_btn.setObjectName("DangerButton")
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_btn.clicked.connect(self.clear_requested.emit)
        header.addWidget(title)
        header.addStretch()
        header.addWidget(clear_btn)
        root.addLayout(header)

        self._search = QLineEdit()
        self._search.setPlaceholderText("Filter saved conversions...")
        self._search.setClearButtonEnabled(True)
        self._search.textChanged.connect(self._on_filter)
        root.addWidget(self._search)

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._list_widget = QWidget()
        self._list_layout = QVBoxLayout(self._list_widget)
        self._list_layout.setContentsMargins(0, 0, 0, 0)
        self._list_layout.setSpacing(8)
        self._scroll.setWidget(self._list_widget)
        root.addWidget(self._scroll, 1)

    def set_items(self, items: list[dict[str, str]]) -> None:
        self._items = list(items)
        self._rebuild()

    def _on_filter(self, text: str) -> None:
        self._filter = text.strip().lower()
        self._rebuild()

    def _rebuild(self) -> None:
        while self._list_layout.count():
            item = self._list_layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

        matched = 0
        for entry in self._items:
            singlish = entry.get("singlish", "")
            sinhala = entry.get("sinhala", "")
            ts = entry.get("timestamp", "")
            if self._filter and (
                self._filter not in singlish.lower()
                and self._filter not in sinhala.lower()
            ):
                continue

            matched += 1
            card = QFrame()
            card.setObjectName("CardPanel")
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(10, 8, 10, 8)
            card_layout.setSpacing(4)

            top_row = QHBoxLayout()
            ts_lbl = QLabel(ts)
            ts_lbl.setObjectName("MutedLabel")
            restore_btn = QPushButton("Restore")
            restore_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            restore_btn.clicked.connect(lambda _c=False, s=singlish: self.restore_requested.emit(s))
            copy_btn = QPushButton("Copy")
            copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            copy_btn.clicked.connect(lambda _c=False, o=sinhala: self.copy_requested.emit(o))
            top_row.addWidget(ts_lbl)
            top_row.addStretch()
            top_row.addWidget(restore_btn)
            top_row.addWidget(copy_btn)
            card_layout.addLayout(top_row)

            out_preview = QLabel(sinhala[:140] + ("..." if len(sinhala) > 140 else ""))
            out_preview.setWordWrap(True)
            out_preview.setStyleSheet("font-size: 11pt; font-weight: 500;")
            card_layout.addWidget(out_preview)

            in_preview = QLabel(singlish[:120] + ("..." if len(singlish) > 120 else ""))
            in_preview.setWordWrap(True)
            in_preview.setObjectName("MutedLabel")
            card_layout.addWidget(in_preview)

            self._list_layout.addWidget(card)

        if matched == 0:
            empty = QLabel("No saved conversions yet.\nUse Copy (Ctrl+Enter) or Snapshot to save.")
            empty.setObjectName("MutedLabel")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._list_layout.addWidget(empty)

        self._list_layout.addStretch(1)
