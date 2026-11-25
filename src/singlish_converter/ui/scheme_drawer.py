"""Interactive, searchable Singlish transliteration scheme reference drawer."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from singlish_converter.scheme_data import (
    ALL_SCHEME_ENTRIES,
    DERIVING_CONSONANTS,
    SchemeEntry,
)


class SchemeReferenceWidget(QFrame):
    """Searchable grid of UCSC Singlish mappings with click-to-insert support."""

    insert_requested = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("SidePanel")
        self._active_category = "All"
        self._search_text = ""

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(10)

        header = QHBoxLayout()
        title = QLabel("Transliteration Scheme")
        title.setObjectName("CardTitle")
        subtitle = QLabel("Click any tile to insert")
        subtitle.setObjectName("MutedLabel")
        header.addWidget(title)
        header.addStretch()
        header.addWidget(subtitle)
        root.addLayout(header)

        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText("Search key or Sinhala (e.g. nndh, sh, ඳ, ru)...")
        self._search_input.setClearButtonEnabled(True)
        self._search_input.textChanged.connect(self._on_search_changed)
        root.addWidget(self._search_input)

        # Category filter pills
        cat_row = QHBoxLayout()
        cat_row.setSpacing(6)
        self._cat_group = QButtonGroup(self)
        self._cat_group.setExclusive(True)
        for cat in ("All", "Vowels", "Consonants", "Auxiliaries", "k-Family"):
            btn = QPushButton(cat)
            btn.setCheckable(True)
            btn.setChecked(cat == "All")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _checked=False, c=cat: self._set_category(c))
            self._cat_group.addButton(btn)
            cat_row.addWidget(btn)
        root.addLayout(cat_row)

        # Scrollable tile grid
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._grid_container = QWidget()
        self._grid_layout = QGridLayout(self._grid_container)
        self._grid_layout.setContentsMargins(2, 2, 2, 2)
        self._grid_layout.setSpacing(6)
        self._scroll.setWidget(self._grid_container)
        root.addWidget(self._scroll, 1)

        self._rebuild_grid()

    def focus_search(self) -> None:
        self._search_input.setFocus()
        self._search_input.selectAll()

    def _set_category(self, category: str) -> None:
        self._active_category = category
        self._rebuild_grid()

    def _on_search_changed(self, text: str) -> None:
        self._search_text = text.strip().lower()
        self._rebuild_grid()

    def _clear_grid(self) -> None:
        while self._grid_layout.count():
            item = self._grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _matches(self, entry: SchemeEntry) -> bool:
        if self._active_category != "All" and entry.category != self._active_category:
            return False
        if not self._search_text:
            return True
        haystack = " ".join(
            [
                entry.sinhala,
                entry.sub_group,
                " ".join(entry.keys),
                entry.example_sinhala,
                entry.example_key,
                entry.note,
            ]
        ).lower()
        return self._search_text in haystack

    def _create_tile(self, sinhala: str, key_text: str, insert_key: str, tooltip: str) -> QPushButton:
        btn = QPushButton(f"{sinhala}\n{key_text}")
        btn.setObjectName("SchemeTile")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(54)
        btn.setToolTip(tooltip)
        btn.clicked.connect(lambda _checked=False, k=insert_key: self.insert_requested.emit(k))
        return btn

    def _rebuild_grid(self) -> None:
        self._clear_grid()
        cols = 4
        row = 0
        col = 0

        if self._active_category == "k-Family":
            for sinhala, key in DERIVING_CONSONANTS:
                if self._search_text and (
                    self._search_text not in sinhala.lower()
                    and self._search_text not in key.lower()
                ):
                    continue
                tile = self._create_tile(
                    sinhala,
                    key,
                    key,
                    f"Click to insert '{key}' → {sinhala}",
                )
                self._grid_layout.addWidget(tile, row, col)
                col += 1
                if col >= cols:
                    col = 0
                    row += 1
        else:
            filtered = [e for e in ALL_SCHEME_ENTRIES if self._matches(e)]
            for entry in filtered:
                keys_display = " / ".join(entry.keys)
                primary_key = entry.keys[0]
                tip_lines = [f"{entry.category} · {entry.sub_group}", f"Type: {keys_display} → {entry.sinhala}"]
                if entry.example_sinhala:
                    tip_lines.append(f"Example: {entry.example_key} → {entry.example_sinhala}")
                if entry.note:
                    tip_lines.append(entry.note)
                tile = self._create_tile(
                    entry.sinhala,
                    keys_display,
                    primary_key,
                    "\n".join(tip_lines),
                )
                self._grid_layout.addWidget(tile, row, col)
                col += 1
                if col >= cols:
                    col = 0
                    row += 1

        if row == 0 and col == 0:
            empty = QLabel("No matching Singlish mappings found.")
            empty.setObjectName("MutedLabel")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._grid_layout.addWidget(empty, 0, 0, 1, cols)

        self._grid_layout.setRowStretch(row + 1, 1)
