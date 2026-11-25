# Singlish Studio

A modern, real-time **Singlish to Sinhala Unicode** desktop application and Windows installer built with **Python**, **PySide6 (Qt 6)**, **PyInstaller**, and **Inno Setup**, implementing the classic UCSC Real Time Unicode Converter phonetic scheme with modern desktop ergonomics.

## Features

- **Real-Time UCSC Transliteration Engine**: Faithful mapping for all vowels, modifiers, consonants, aspirated/special characters, nasalized consonants (`nnd`, `nndh`, `nng`), Rakaransha (`ක්‍ර`), Repaya (`ර්\u200D`), Yansaya (`්‍ය`), and Gayanukitta (`ෘ`, `ෲ`) using proper Unicode Zero-Width Joiners (`U+200D`).
- **Inline English Escape Mode**: Toggle `` `English` `` to keep words wrapped in backticks (e.g., ``mama `Python` igena gannavaa`` → `මම Python ඉගෙන ගන්නවා`).
- **Interactive Transliteration Reference Studio (`Ctrl+K`)**: Searchable, categorized card grid (Vowels, Consonants, Auxiliaries, k-Family derivatives). Click any tile to insert its Singlish key directly at the cursor.
- **Quick Singlish Keybar & Live Word Preview**: One-click chips for tricky keys (`ං \n`, `ඃ \h`, `ඇ A`, `ඳ nndh`, etc.) plus a real-time badge showing the transliteration of the word under your cursor.
- **Unicode Codepoint Inspector**: Inspect exact UTF codepoints (including `ZWJ` and `HAL`) of selected Sinhala text.
- **Typography & Layout Controls**: Switch Sinhala fonts (`Nirmala UI`, `Iskoola Pota`, `Noto Sans Sinhala`, etc.), adjust font sizes independently, toggle Dark / Light themes (`Ctrl+D`), switch between Side-by-Side and Stacked split views, and pin Always-on-Top.
- **History, File Import/Export & System Tray**: Save snapshots (`Ctrl+Enter` / Copy), restore from history (`Ctrl+H`), import `.txt`, export `.txt` or `.html`, and optionally convert clipboard Singlish directly from the Windows System Tray.

## Running from Source

```powershell
.venv\Scripts\python.exe -m pip install -e .
.venv\Scripts\python.exe -m singlish_converter.app
```

## Running Tests

```powershell
.venv\Scripts\python.exe -m pytest -v
```

## Building the Windows Installer

```powershell
.\build.ps1
```

This runs the test suite, generates the application icon and wizard graphics, bundles `SinglishStudio.exe` with PyInstaller, and compiles `dist\installer\SinglishStudio-Setup-1.0.0.exe` via Inno Setup.
"# Singlish-Converter" 
