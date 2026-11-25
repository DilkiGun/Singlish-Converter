"""Main application window for Singlish Studio."""

from __future__ import annotations

import html
from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import (
    QAction,
    QCloseEvent,
    QFont,
    QFontDatabase,
    QIcon,
    QKeySequence,
    QPixmap,
    QShortcut,
    QTextCursor,
)
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSpinBox,
    QSplitter,
    QStackedWidget,
    QStatusBar,
    QVBoxLayout,
    QWidget,
    QSystemTrayIcon,
)

from singlish_converter import __app_name__, __version__
from singlish_converter.assets import get_asset_path
from singlish_converter.scheme_data import QUICK_CHIPS, SAMPLE_PRESETS
from singlish_converter.settings import AppSettings
from singlish_converter.transliterator import (
    compute_stats,
    inspect_codepoints,
    transliterate,
)
from singlish_converter.ui.history_panel import HistoryPanel
from singlish_converter.ui.scheme_drawer import SchemeReferenceWidget
from singlish_converter.ui.theme import apply_windows_titlebar_theme, build_stylesheet


PREFERRED_SINHALA_FONTS = (
    "Nirmala UI",
    "Iskoola Pota",
    "Noto Sans Sinhala",
    "Noto Serif Sinhala",
    "Abhaya Libre",
    "Malithi Web",
    "Potha",
    "Segoe UI",
)


class MainWindow(QMainWindow):
    """Advanced Real-Time Singlish to Sinhala Unicode Converter Window."""

    def __init__(
        self,
        settings: AppSettings | None = None,
        settings_path: Path | None = None,
    ) -> None:
        super().__init__()
        self.settings_path = settings_path
        self.settings = settings or AppSettings.load(self.settings_path)
        self._force_quit = False
        self._syncing_output = False

        self.setWindowTitle(f"{__app_name__} — Real-Time Singlish to Sinhala Converter")
        self.resize(1240, 760)
        self.setMinimumSize(900, 580)

        icon_path = get_asset_path("app_icon.png")
        if icon_path.exists():
            self._app_icon = QIcon(str(icon_path))
            self.setWindowIcon(self._app_icon)
        else:
            self._app_icon = self.windowIcon()

        self._auto_copy_timer = QTimer(self)
        self._auto_copy_timer.setSingleShot(True)
        self._auto_copy_timer.setInterval(650)
        self._auto_copy_timer.timeout.connect(self._perform_auto_copy)

        self._copy_feedback_timer = QTimer(self)
        self._copy_feedback_timer.setSingleShot(True)
        self._copy_feedback_timer.setInterval(1600)
        self._copy_feedback_timer.timeout.connect(self._reset_copy_button)

        self._build_ui()
        self._build_shortcuts()
        self._build_tray()
        self._apply_settings()
        self._apply_theme()

    # ------------------------------------------------------------------
    # UI Construction
    # ------------------------------------------------------------------
    def _build_ui(self) -> None:
        root_widget = QWidget()
        root_widget.setObjectName("RootWidget")
        self.setCentralWidget(root_widget)

        outer = QVBoxLayout(root_widget)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        outer.addWidget(self._build_header_bar())
        outer.addWidget(self._build_quick_key_bar())

        # Workspace body (main splitter + optional side drawer)
        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(14, 12, 14, 10)
        body_layout.setSpacing(10)

        self._main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self._editor_splitter = QSplitter(Qt.Orientation.Horizontal)

        self._editor_splitter.addWidget(self._build_input_card())
        self._editor_splitter.addWidget(self._build_output_card())
        self._editor_splitter.setStretchFactor(0, 1)
        self._editor_splitter.setStretchFactor(1, 1)

        self._side_stack = QStackedWidget()
        self._side_stack.setMinimumWidth(330)
        self._side_stack.setMaximumWidth(480)
        self._scheme_widget = SchemeReferenceWidget()
        self._scheme_widget.insert_requested.connect(self._insert_singlish_snippet)
        self._history_widget = HistoryPanel()
        self._history_widget.restore_requested.connect(self._restore_from_history)
        self._history_widget.copy_requested.connect(self._copy_text)
        self._history_widget.clear_requested.connect(self._clear_history)
        self._side_stack.addWidget(self._scheme_widget)
        self._side_stack.addWidget(self._history_widget)

        self._main_splitter.addWidget(self._editor_splitter)
        self._main_splitter.addWidget(self._side_stack)
        self._main_splitter.setStretchFactor(0, 3)
        self._main_splitter.setStretchFactor(1, 1)
        self._side_stack.hide()

        body_layout.addWidget(self._main_splitter, 1)
        outer.addWidget(body, 1)

        # Status Bar
        status = QStatusBar()
        self.setStatusBar(status)
        self._status_label = QLabel("Ready · UCSC Real-Time Scheme")
        self._shortcut_hint = QLabel(
            "Ctrl+Enter Copy  |  Ctrl+Shift+V Paste & Convert  |  Ctrl+K Scheme  |  Ctrl+H History"
        )
        status.addWidget(self._status_label, 1)
        status.addPermanentWidget(self._shortcut_hint)

    def _build_header_bar(self) -> QWidget:
        bar = QWidget()
        bar.setObjectName("HeaderBar")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(10)

        # Brand badge + title
        icon_lbl = QLabel()
        icon_path = get_asset_path("app_icon.png")
        if icon_path.exists():
            pix = QPixmap(str(icon_path)).scaled(
                34, 34, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            )
            icon_lbl.setPixmap(pix)
        layout.addWidget(icon_lbl)

        title_col = QVBoxLayout()
        title_col.setSpacing(0)
        title = QLabel(f"{__app_name__} v{__version__}")
        title.setObjectName("AppTitle")
        subtitle = QLabel("Real-Time UCSC Singlish → Sinhala Unicode Studio")
        subtitle.setObjectName("AppSubtitle")
        title_col.addWidget(title)
        title_col.addWidget(subtitle)
        layout.addLayout(title_col)

        layout.addStretch(1)

        # Samples dropdown
        self._samples_btn = QPushButton("Samples ▾")
        self._samples_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        samples_menu = QMenu(self._samples_btn)
        for label, snippet in SAMPLE_PRESETS:
            act = samples_menu.addAction(label)
            act.triggered.connect(lambda _c=False, s=snippet: self._load_sample(s))
        self._samples_btn.setMenu(samples_menu)
        layout.addWidget(self._samples_btn)

        # Live Conversion toggle
        self._live_btn = QPushButton("⚡ Live")
        self._live_btn.setCheckable(True)
        self._live_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._live_btn.setToolTip("Convert automatically as you type")
        self._live_btn.toggled.connect(self._on_live_toggled)
        layout.addWidget(self._live_btn)

        self._manual_convert_btn = QPushButton("Convert")
        self._manual_convert_btn.setObjectName("PrimaryButton")
        self._manual_convert_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._manual_convert_btn.clicked.connect(self._convert_now)
        self._manual_convert_btn.hide()
        layout.addWidget(self._manual_convert_btn)

        # Preserve backticks toggle
        self._backtick_btn = QPushButton("`English`")
        self._backtick_btn.setCheckable(True)
        self._backtick_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._backtick_btn.setToolTip(
            "Wrap words in `backticks` to keep English words untransliterated inline"
        )
        self._backtick_btn.toggled.connect(self._on_backtick_toggled)
        layout.addWidget(self._backtick_btn)

        # Auto-Copy toggle
        self._autocopy_btn = QPushButton("Auto-Copy")
        self._autocopy_btn.setCheckable(True)
        self._autocopy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._autocopy_btn.setToolTip("Automatically copy Sinhala Unicode after a short pause")
        self._autocopy_btn.toggled.connect(self._on_autocopy_toggled)
        layout.addWidget(self._autocopy_btn)

        # Layout Orientation toggle
        self._layout_btn = QPushButton("Split: ◫")
        self._layout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._layout_btn.setToolTip("Switch between Side-by-Side and Stacked panes")
        self._layout_btn.clicked.connect(self._toggle_split_orientation)
        layout.addWidget(self._layout_btn)

        # Pin Always on Top
        self._pin_btn = QPushButton("📌 Pin")
        self._pin_btn.setCheckable(True)
        self._pin_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._pin_btn.setToolTip("Keep window always on top")
        self._pin_btn.toggled.connect(self._on_pin_toggled)
        layout.addWidget(self._pin_btn)

        # Theme toggle
        self._theme_btn = QPushButton("🌙 Dark")
        self._theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._theme_btn.setToolTip("Toggle Dark / Light theme (Ctrl+D)")
        self._theme_btn.clicked.connect(self._toggle_theme)
        layout.addWidget(self._theme_btn)

        # Side drawer toggles
        self._scheme_btn = QPushButton("Scheme")
        self._scheme_btn.setCheckable(True)
        self._scheme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._scheme_btn.setToolTip("Toggle Transliteration Scheme Reference (Ctrl+K)")
        self._scheme_btn.clicked.connect(lambda: self._toggle_side_panel(0))
        layout.addWidget(self._scheme_btn)

        self._history_btn = QPushButton("History")
        self._history_btn.setCheckable(True)
        self._history_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._history_btn.setToolTip("Toggle Saved History (Ctrl+H)")
        self._history_btn.clicked.connect(lambda: self._toggle_side_panel(1))
        layout.addWidget(self._history_btn)

        return bar

    def _build_quick_key_bar(self) -> QWidget:
        bar = QWidget()
        bar.setObjectName("KeyBar")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(16, 6, 16, 6)
        layout.setSpacing(6)

        lbl = QLabel("Quick Keys:")
        lbl.setObjectName("MutedLabel")
        layout.addWidget(lbl)

        for sinhala, key in QUICK_CHIPS:
            chip = QPushButton(f"{sinhala}  {key}")
            chip.setObjectName("QuickChip")
            chip.setCursor(Qt.CursorShape.PointingHandCursor)
            chip.setToolTip(f"Insert '{key}' → {sinhala}")
            chip.clicked.connect(lambda _c=False, k=key: self._insert_singlish_snippet(k))
            layout.addWidget(chip)

        layout.addStretch(1)
        return bar

    def _build_input_card(self) -> QFrame:
        card = QFrame()
        card.setObjectName("CardPanel")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(8)

        # Card Header
        top = QHBoxLayout()
        title = QLabel("Singlish Input (Phonetic)")
        title.setObjectName("CardTitle")
        self._word_hint_badge = QLabel("Type Singlish...")
        self._word_hint_badge.setObjectName("WordHintBadge")
        top.addWidget(title)
        top.addStretch(1)
        top.addWidget(self._word_hint_badge)
        layout.addLayout(top)

        # Action toolbar
        tools = QHBoxLayout()
        tools.setSpacing(6)

        paste_btn = QPushButton("Paste & Convert")
        paste_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        paste_btn.clicked.connect(self._paste_and_convert)

        import_btn = QPushButton("Import .txt")
        import_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        import_btn.clicked.connect(self._import_text_file)

        undo_btn = QPushButton("Undo")
        undo_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        redo_btn = QPushButton("Redo")
        redo_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        clear_btn = QPushButton("Clear")
        clear_btn.setObjectName("DangerButton")
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_btn.clicked.connect(self._clear_all)

        tools.addWidget(paste_btn)
        tools.addWidget(import_btn)
        tools.addStretch(1)
        tools.addWidget(undo_btn)
        tools.addWidget(redo_btn)
        tools.addWidget(clear_btn)
        layout.addLayout(tools)

        # Editor
        self._input_edit = QPlainTextEdit()
        self._input_edit.setPlaceholderText(
            "Type Singlish here (e.g. aayuboevan! oyaata kohomadha?)...\n\n"
            "Tips:\n"
            "• Use Shift/capitals for special sounds: A (ඇ), Aa (ඈ), N (ණ), L (ළ), R (ර්‍), Y (්‍ය)\n"
            "• Prefix backslash for anusvara/visarga: \\n (ං), \\h (ඃ), \\N (ඞ), \\R (ඍ)\n"
            "• Wrap inline English words in `backticks` when `English` mode is active"
        )
        self._input_edit.textChanged.connect(self._on_input_changed)
        self._input_edit.cursorPositionChanged.connect(self._update_word_hint)
        undo_btn.clicked.connect(self._input_edit.undo)
        redo_btn.clicked.connect(self._input_edit.redo)
        layout.addWidget(self._input_edit, 1)

        # Footer stats + font size controls
        footer = QHBoxLayout()
        self._input_stats_lbl = QLabel("0 chars · 0 words · 0 lines")
        self._input_stats_lbl.setObjectName("MutedLabel")

        in_font_lbl = QLabel("Text Size:")
        in_font_lbl.setObjectName("MutedLabel")
        self._input_font_spin = QSpinBox()
        self._input_font_spin.setRange(10, 28)
        self._input_font_spin.setSuffix(" pt")
        self._input_font_spin.valueChanged.connect(self._on_input_font_size_changed)

        footer.addWidget(self._input_stats_lbl)
        footer.addStretch(1)
        footer.addWidget(in_font_lbl)
        footer.addWidget(self._input_font_spin)
        layout.addLayout(footer)

        return card

    def _build_output_card(self) -> QFrame:
        card = QFrame()
        card.setObjectName("CardPanel")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(8)

        # Card Header with Font picker + size
        top = QHBoxLayout()
        title = QLabel("Sinhala Unicode (සිංහල යුනිකෝඩ්)")
        title.setObjectName("CardTitle")
        top.addWidget(title)
        top.addStretch(1)

        self._font_combo = QComboBox()
        self._font_combo.setMinimumWidth(160)
        self._populate_sinhala_fonts()
        self._font_combo.currentTextChanged.connect(self._on_output_font_changed)
        top.addWidget(self._font_combo)

        self._output_font_spin = QSpinBox()
        self._output_font_spin.setRange(11, 42)
        self._output_font_spin.setSuffix(" pt")
        self._output_font_spin.valueChanged.connect(self._on_output_font_size_changed)
        top.addWidget(self._output_font_spin)
        layout.addLayout(top)

        # Action toolbar
        tools = QHBoxLayout()
        tools.setSpacing(6)

        self._copy_btn = QPushButton("Copy Sinhala")
        self._copy_btn.setObjectName("PrimaryButton")
        self._copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._copy_btn.clicked.connect(self._copy_output_and_record)

        snapshot_btn = QPushButton("Save Snapshot")
        snapshot_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        snapshot_btn.clicked.connect(self._save_snapshot)

        export_txt_btn = QPushButton("Export .txt")
        export_txt_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        export_txt_btn.clicked.connect(self._export_txt)

        export_html_btn = QPushButton("Export .html")
        export_html_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        export_html_btn.clicked.connect(self._export_html)

        tools.addWidget(self._copy_btn)
        tools.addWidget(snapshot_btn)
        tools.addStretch(1)
        tools.addWidget(export_txt_btn)
        tools.addWidget(export_html_btn)
        layout.addLayout(tools)

        # Output Editor
        self._output_edit = QPlainTextEdit()
        self._output_edit.setObjectName("SinhalaEditor")
        self._output_edit.setPlaceholderText("සිංහල යුනිකෝඩ් පෙළ මෙහි දිස්වනු ඇත...")
        self._output_edit.cursorPositionChanged.connect(self._update_codepoint_inspector)
        self._output_edit.selectionChanged.connect(self._update_codepoint_inspector)
        self._output_edit.textChanged.connect(self._update_output_stats)
        layout.addWidget(self._output_edit, 1)

        # Unicode Codepoint Inspector + stats
        self._codepoint_lbl = QLabel("Unicode Inspector: Select text or place cursor to inspect codepoints")
        self._codepoint_lbl.setObjectName("CodepointBar")
        self._codepoint_lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self._codepoint_lbl)

        footer = QHBoxLayout()
        self._output_stats_lbl = QLabel("0 chars · 0 words · 0 lines")
        self._output_stats_lbl.setObjectName("MutedLabel")
        footer.addWidget(self._output_stats_lbl)
        footer.addStretch(1)
        layout.addLayout(footer)

        return card

    def _populate_sinhala_fonts(self) -> None:
        families = set(QFontDatabase.families())
        ordered: list[str] = [f for f in PREFERRED_SINHALA_FONTS if f in families]
        remaining = sorted(families - set(ordered))
        self._font_combo.addItems(ordered + remaining)

    def _build_shortcuts(self) -> None:
        QShortcut(QKeySequence("Ctrl+Return"), self, self._copy_output_and_record)
        QShortcut(QKeySequence("Ctrl+Enter"), self, self._copy_output_and_record)
        QShortcut(QKeySequence("Ctrl+Shift+V"), self, self._paste_and_convert)
        QShortcut(QKeySequence("Ctrl+K"), self, lambda: self._toggle_side_panel(0))
        QShortcut(QKeySequence("Ctrl+H"), self, lambda: self._toggle_side_panel(1))
        QShortcut(QKeySequence("Ctrl+L"), self, self._clear_all)
        QShortcut(QKeySequence("Ctrl+D"), self, self._toggle_theme)

    def _build_tray(self) -> None:
        if not QSystemTrayIcon.isSystemTrayAvailable():
            self._tray = None
            return
        self._tray = QSystemTrayIcon(self._app_icon, self)
        self._tray.setToolTip(__app_name__)

        menu = QMenu(self)
        show_act = menu.addAction("Show / Restore Window")
        show_act.triggered.connect(self._show_from_tray)

        clip_act = menu.addAction("Convert Clipboard Singlish → Sinhala")
        clip_act.triggered.connect(self._convert_clipboard_in_place)

        menu.addSeparator()
        self._tray_close_act = QAction("Minimize to Tray on Close", self, checkable=True)
        self._tray_close_act.setChecked(self.settings.minimize_to_tray)
        self._tray_close_act.toggled.connect(self._on_tray_close_toggled)
        menu.addAction(self._tray_close_act)

        menu.addSeparator()
        quit_act = menu.addAction("Quit")
        quit_act.triggered.connect(self._quit_application)

        self._tray.setContextMenu(menu)
        self._tray.activated.connect(self._on_tray_activated)
        self._tray.show()

    # ------------------------------------------------------------------
    # Settings & Theme Sync
    # ------------------------------------------------------------------
    def _apply_settings(self) -> None:
        self._live_btn.setChecked(self.settings.live_convert)
        self._manual_convert_btn.setVisible(not self.settings.live_convert)
        self._backtick_btn.setChecked(self.settings.preserve_backticks)
        self._autocopy_btn.setChecked(self.settings.auto_copy)
        self._pin_btn.setChecked(self.settings.always_on_top)

        if self.settings.split_orientation == "vertical":
            self._editor_splitter.setOrientation(Qt.Orientation.Vertical)
            self._layout_btn.setText("Split: ☰")
        else:
            self._editor_splitter.setOrientation(Qt.Orientation.Horizontal)
            self._layout_btn.setText("Split: ◫")

        self._input_font_spin.setValue(self.settings.input_font_size)
        self._output_font_spin.setValue(self.settings.font_size)

        idx = self._font_combo.findText(self.settings.font_family)
        if idx >= 0:
            self._font_combo.setCurrentIndex(idx)
        elif self._font_combo.count() > 0:
            self.settings.font_family = self._font_combo.currentText()

        self._apply_editor_fonts()
        self._history_widget.set_items(self.settings.history)

        if self.settings.scheme_panel_visible:
            self._side_stack.setCurrentIndex(0)
            self._side_stack.show()
            self._scheme_btn.setChecked(True)

    def _apply_theme(self) -> None:
        is_dark = self.settings.theme == "dark"
        self.setStyleSheet(build_stylesheet(self.settings.theme))
        self._theme_btn.setText("🌙 Dark" if is_dark else "☀ Light")
        apply_windows_titlebar_theme(self, is_dark)

    def _apply_editor_fonts(self) -> None:
        in_font = QFont("Consolas", self.settings.input_font_size)
        in_font.setStyleHint(QFont.StyleHint.Monospace)
        self._input_edit.setFont(in_font)

        out_font = QFont(self.settings.font_family, self.settings.font_size)
        self._output_edit.setFont(out_font)

    # ------------------------------------------------------------------
    # Conversion & Editor Handlers
    # ------------------------------------------------------------------
    def _on_input_changed(self) -> None:
        if self.settings.live_convert:
            self._convert_now()
        else:
            self._update_input_stats()
        self._update_word_hint()

    def _convert_now(self) -> None:
        src = self._input_edit.toPlainText()
        converted = transliterate(src, preserve_backticks=self.settings.preserve_backticks)
        self._syncing_output = True
        self._output_edit.setPlainText(converted)
        self._syncing_output = False

        stats = compute_stats(src, converted)
        self._input_stats_lbl.setText(
            f"{stats.input_chars} chars · {len(src.split()) if src.strip() else 0} words · {src.count(chr(10)) + 1 if src else 0} lines"
        )
        self._output_stats_lbl.setText(
            f"{stats.output_chars} chars · {stats.words} words · {stats.lines} lines"
        )
        self._update_codepoint_inspector()

        if self.settings.auto_copy and converted:
            self._auto_copy_timer.start()

    def _update_input_stats(self) -> None:
        src = self._input_edit.toPlainText()
        self._input_stats_lbl.setText(
            f"{len(src)} chars · {len(src.split()) if src.strip() else 0} words · {src.count(chr(10)) + 1 if src else 0} lines"
        )

    def _update_output_stats(self) -> None:
        if self._syncing_output:
            return
        out = self._output_edit.toPlainText()
        words = len(out.split()) if out.strip() else 0
        lines = out.count("\n") + 1 if out else 0
        self._output_stats_lbl.setText(f"{len(out)} chars · {words} words · {lines} lines")

    def _update_word_hint(self) -> None:
        cursor = self._input_edit.textCursor()
        cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        word = cursor.selectedText().strip()
        if not word:
            self._word_hint_badge.setText("Type Singlish...")
            return
        preview = transliterate(word, preserve_backticks=self.settings.preserve_backticks)
        self._word_hint_badge.setText(f"{word} → {preview}")

    def _update_codepoint_inspector(self) -> None:
        cursor = self._output_edit.textCursor()
        selected = cursor.selectedText().replace("\u2029", "\n")
        if selected:
            self._codepoint_lbl.setText(f"Selection: {inspect_codepoints(selected)}")
            return
        pos = cursor.position()
        text = self._output_edit.toPlainText()
        if not text:
            self._codepoint_lbl.setText(
                "Unicode Inspector: Select text or place cursor to inspect codepoints"
            )
            return
        idx = max(0, min(pos - 1, len(text) - 1))
        ch = text[idx]
        self._codepoint_lbl.setText(f"Cursor Char: {inspect_codepoints(ch, limit=1)}")

    def _insert_singlish_snippet(self, snippet: str) -> None:
        cursor = self._input_edit.textCursor()
        cursor.insertText(snippet)
        self._input_edit.setTextCursor(cursor)
        self._input_edit.setFocus()

    # ------------------------------------------------------------------
    # Toolbar & Drawer Actions
    # ------------------------------------------------------------------
    def _load_sample(self, snippet: str) -> None:
        self._input_edit.setPlainText(snippet)
        self._input_edit.setFocus()
        self._status_label.setText("Loaded sample text")

    def _on_live_toggled(self, checked: bool) -> None:
        self.settings.live_convert = checked
        self._manual_convert_btn.setVisible(not checked)
        if checked:
            self._convert_now()

    def _on_backtick_toggled(self, checked: bool) -> None:
        self.settings.preserve_backticks = checked
        self._convert_now()

    def _on_autocopy_toggled(self, checked: bool) -> None:
        self.settings.auto_copy = checked
        self._status_label.setText(
            "Auto-copy enabled" if checked else "Auto-copy disabled"
        )

    def _toggle_split_orientation(self) -> None:
        if self._editor_splitter.orientation() == Qt.Orientation.Horizontal:
            self._editor_splitter.setOrientation(Qt.Orientation.Vertical)
            self.settings.split_orientation = "vertical"
            self._layout_btn.setText("Split: ☰")
        else:
            self._editor_splitter.setOrientation(Qt.Orientation.Horizontal)
            self.settings.split_orientation = "horizontal"
            self._layout_btn.setText("Split: ◫")

    def _on_pin_toggled(self, checked: bool) -> None:
        self.settings.always_on_top = checked
        was_visible = self.isVisible()
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, checked)
        if was_visible:
            self.show()
            apply_windows_titlebar_theme(self, self.settings.theme == "dark")

    def _toggle_theme(self) -> None:
        self.settings.theme = "light" if self.settings.theme == "dark" else "dark"
        self._apply_theme()

    def _toggle_side_panel(self, index: int) -> None:
        currently_visible = self._side_stack.isVisible()
        current_idx = self._side_stack.currentIndex()
        if currently_visible and current_idx == index:
            self._side_stack.hide()
            self._scheme_btn.setChecked(False)
            self._history_btn.setChecked(False)
            self.settings.scheme_panel_visible = False
        else:
            self._side_stack.setCurrentIndex(index)
            self._side_stack.show()
            self._scheme_btn.setChecked(index == 0)
            self._history_btn.setChecked(index == 1)
            self.settings.scheme_panel_visible = index == 0
            if index == 0:
                self._scheme_widget.focus_search()

    def _on_input_font_size_changed(self, size: int) -> None:
        self.settings.input_font_size = size
        self._apply_editor_fonts()

    def _on_output_font_changed(self, family: str) -> None:
        self.settings.font_family = family
        self._apply_editor_fonts()

    def _on_output_font_size_changed(self, size: int) -> None:
        self.settings.font_size = size
        self._apply_editor_fonts()

    # ------------------------------------------------------------------
    # Clipboard, Files & History
    # ------------------------------------------------------------------
    def _copy_text(self, text: str) -> None:
        if not text:
            return
        QApplication.clipboard().setText(text)
        self._status_label.setText(f"Copied {len(text)} Sinhala characters to clipboard")

    def _copy_output_and_record(self) -> None:
        out = self._output_edit.toPlainText()
        if not out:
            self._status_label.setText("Nothing to copy yet")
            return
        self._copy_text(out)
        self._save_snapshot()
        self._copy_btn.setText("✓ Copied!")
        self._copy_feedback_timer.start()

    def _perform_auto_copy(self) -> None:
        out = self._output_edit.toPlainText()
        if out:
            QApplication.clipboard().setText(out)
            self._status_label.setText("Auto-copied Sinhala Unicode to clipboard")

    def _reset_copy_button(self) -> None:
        self._copy_btn.setText("Copy Sinhala")

    def _save_snapshot(self) -> None:
        src = self._input_edit.toPlainText()
        out = self._output_edit.toPlainText()
        if not src.strip() or not out.strip():
            return
        self.settings.add_history(src, out)
        self._history_widget.set_items(self.settings.history)
        self._status_label.setText("Saved conversion to history")

    def _restore_from_history(self, singlish: str) -> None:
        self._input_edit.setPlainText(singlish)
        if not self.settings.live_convert:
            self._convert_now()
        self._status_label.setText("Restored conversion from history")

    def _clear_history(self) -> None:
        self.settings.history.clear()
        self._history_widget.set_items(self.settings.history)
        self._status_label.setText("Cleared conversion history")

    def _paste_and_convert(self) -> None:
        clip_text = QApplication.clipboard().text()
        if not clip_text:
            self._status_label.setText("Clipboard is empty")
            return
        self._input_edit.setPlainText(clip_text)
        self._convert_now()
        out = self._output_edit.toPlainText()
        if out:
            QApplication.clipboard().setText(out)
            self._status_label.setText("Pasted Singlish, converted, and copied Sinhala Unicode!")

    def _clear_all(self) -> None:
        self._input_edit.clear()
        self._output_edit.clear()
        self._input_edit.setFocus()
        self._status_label.setText("Cleared editors")

    def _import_text_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Singlish Text File",
            "",
            "Text Files (*.txt *.md);;All Files (*)",
        )
        if not path:
            return
        try:
            content = Path(path).read_text(encoding="utf-8")
            self._input_edit.setPlainText(content)
            self._convert_now()
            self._status_label.setText(f"Imported {Path(path).name}")
        except Exception as exc:
            QMessageBox.warning(self, "Import Failed", f"Could not read file:\n{exc}")

    def _export_txt(self) -> None:
        out = self._output_edit.toPlainText()
        if not out:
            QMessageBox.information(self, "Nothing to Export", "Convert some text before exporting.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Sinhala Unicode Text",
            "sinhala_output.txt",
            "UTF-8 Text File (*.txt)",
        )
        if not path:
            return
        Path(path).write_text(out, encoding="utf-8")
        self._status_label.setText(f"Exported UTF-8 text to {Path(path).name}")

    def _export_html(self) -> None:
        out = self._output_edit.toPlainText()
        if not out:
            QMessageBox.information(self, "Nothing to Export", "Convert some text before exporting.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Sinhala Unicode HTML",
            "sinhala_output.html",
            "HTML Document (*.html)",
        )
        if not path:
            return
        escaped = html.escape(out).replace("\n", "<br>\n")
        doc = f"""<!DOCTYPE html>
<html lang="si">
<head>
  <meta charset="UTF-8">
  <title>Singlish Studio Export</title>
  <style>
    body {{ font-family: '{html.escape(self.settings.font_family)}', 'Nirmala UI', 'Iskoola Pota', sans-serif;
           font-size: {self.settings.font_size}pt; line-height: 1.7; max-width: 820px; margin: 40px auto; padding: 0 20px; color: #0f172a; }}
  </style>
</head>
<body>
{escaped}
</body>
</html>
"""
        Path(path).write_text(doc, encoding="utf-8")
        self._status_label.setText(f"Exported HTML to {Path(path).name}")

    # ------------------------------------------------------------------
    # Tray & Lifecycle
    # ------------------------------------------------------------------
    def _on_tray_close_toggled(self, checked: bool) -> None:
        self.settings.minimize_to_tray = checked

    def _on_tray_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason in (
            QSystemTrayIcon.ActivationReason.Trigger,
            QSystemTrayIcon.ActivationReason.DoubleClick,
        ):
            self._show_from_tray()

    def _show_from_tray(self) -> None:
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def _convert_clipboard_in_place(self) -> None:
        text = QApplication.clipboard().text()
        if not text:
            return
        converted = transliterate(text, preserve_backticks=self.settings.preserve_backticks)
        QApplication.clipboard().setText(converted)
        if self._tray is not None:
            self._tray.showMessage(
                __app_name__,
                f"Converted clipboard to Sinhala:\n{converted[:90]}",
                QSystemTrayIcon.MessageIcon.Information,
                2500,
            )

    def _quit_application(self) -> None:
        self._force_quit = True
        self.close()

    def closeEvent(self, event: QCloseEvent) -> None:  # noqa: N802
        try:
            self.settings.save(self.settings_path)
        except OSError:
            pass
        if (
            not self._force_quit
            and self._tray is not None
            and self._tray.isVisible()
            and self.settings.minimize_to_tray
        ):
            event.ignore()
            self.hide()
            self._tray.showMessage(
                __app_name__,
                "Running in background. Click the tray icon to restore or convert clipboard text.",
                QSystemTrayIcon.MessageIcon.Information,
                2000,
            )
            return
        if self._tray is not None:
            self._tray.hide()
        super().closeEvent(event)
