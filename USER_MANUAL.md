# Singlish Studio — User Manual

Welcome to **Singlish Studio**, a real-time **Singlish to Sinhala Unicode** converter for Windows based on the UCSC phonetic transliteration scheme.

---

## 1. Installation

1. Run **`SinglishStudio-Setup-1.0.0.exe`** (located in `dist\installer\`).
2. Accept the license agreement and choose an installation folder (defaults to `LocalAppData\Programs\Singlish Studio` — no administrator rights required).
3. Optionally select:
   - **Create a desktop shortcut**
   - **Launch Singlish Studio automatically at Windows startup**
4. Click **Install**, then **Finish** to launch the app.

> **To uninstall:** Open **Windows Settings → Apps → Installed apps → Singlish Studio**, or run **Uninstall Singlish Studio** from the Start Menu.

---

## 2. Basic Usage

1. Type phonetic Singlish in the **left (Singlish Input)** box — for example:
   - `aayuboevan! oyaata kohomadha?` → `ආයුබෝවන්! ඔයාට කොහොමද?`
2. The **Sinhala Unicode** output appears automatically in the **right** box as you type.
3. Click **Copy Sinhala** (or press **`Ctrl + Enter`**) to copy the converted Sinhala text to your clipboard and save it to History.

---

## 3. Toolbar & Features

### Top Bar Controls
- **Samples ▾**: Load built-in example sentences to test the converter right away.
- **⚡ Live**: Converts text automatically while you type. Turn this off if you prefer to edit first and click **Convert**.
- **`` `English` ``**: Keeps any text inside backticks untransliterated.
  - Example: ``mama `Python` igena gannavaa`` → `මම Python ඉගෙන ගන්නවා`
- **Auto-Copy**: Automatically copies the Sinhala output to your clipboard shortly after you stop typing.
- **Split: ◫ / ☰**: Switch between **Side-by-Side** and **Stacked (Top/Bottom)** editor panes.
- **📌 Pin**: Keep Singlish Studio floating on top of other windows while you work.
- **🌙 Dark / ☀ Light**: Switch between Dark and Light themes (**`Ctrl + D`**).
- **Scheme**: Open or hide the searchable **Transliteration Scheme** panel (**`Ctrl + K`**). Click any tile in the panel to insert its Singlish key at the cursor.
- **History**: Open or hide saved conversions (**`Ctrl + H`**) to **Restore** or **Copy** past entries.

### Quick Keys & Editor Tools
- **Quick Keys Bar**: One-click buttons above the editor insert common special keys (`ං \n`, `ඃ \h`, `ඇ A`, `ඈ Aa`, `ඳ nndh`, `ඬ nnd`, `ඟ nng`, `ශ sh`, `ෂ Sh`, `ළු Lu`, `ඤ KN`, `ඥ GN`, `ර්‍ R`, `්‍ය Y`).
- **Word Preview Badge**: Displays the live Sinhala conversion of the word currently under your cursor.
- **Paste & Convert (`Ctrl + Shift + V`)**: Pastes Singlish from your clipboard, converts it, and immediately copies the Sinhala Unicode result back to your clipboard.
- **Import .txt / Export .txt / Export .html**: Open plain-text Singlish files or save Sinhala Unicode output as UTF-8 `.txt` or `.html`.
- **Sinhala Font & Size**: Pick an installed Sinhala font (such as `Nirmala UI` or `Iskoola Pota`) and adjust text size (`11–42 pt`).
- **Unicode Inspector**: Shows the exact Unicode codepoints (including `ZWJ` zero-width joiners) for selected Sinhala characters.

---

## 4. System Tray Options

Right-click the **Singlish Studio** icon in the Windows notification area (system tray) to:
- **Show / Restore Window**
- **Convert Clipboard Singlish → Sinhala** — Converts Singlish text currently on your clipboard directly into Sinhala Unicode without opening the window.
- **Minimize to Tray on Close** — When enabled, clicking the `X` button hides the app to the tray instead of exiting.
- **Quit** — Exits the application completely.

---

## 5. Quick Singlish Typing Cheat Sheet

| Sound / Symbol | Singlish Key(s) | Example |
|---|---|---|
| අ / ආ | `a` / `aa` or `a)` | `ammaa` → `අම්මා` |
| ඇ / ඈ | `A` or `\a` / `Aa`, `ae`, `A)` | `Atha` → `ඇත`, `Aath` / `aeth` → `ඈත්` |
| ඉ / ඊ | `i` / `ii`, `ie`, `ee`, `i)` | `shrie` → `ශ්‍රී` |
| උ / ඌ | `u` / `uu`, `oo`, `u)` | `aayuboevan` → `ආයුබෝවන්` |
| එ / ඒ | `e` / `ea`, `ei`, `e)` | `ekai` → `එකයි` |
| ඔ / ඕ | `o` / `oe`, `o)` | `oyaata` → `ඔයාට` |
| ං / ඃ | `\n` / `\h` | `si\nhala` → `සිංහල` |
| ඳ / ඬ / ඟ | `nndh` / `nnd` / `nng` | `hanndha` → `හඳ`, `hannda` → `හඬ`, `gannga` → `ගඟ` |
| ශ / ෂ / ෆ | `sh` / `Sh` / `f` | `shrie` → `ශ්‍රී` |
| ත / ද / ථ / ධ | `th` / `dh` / `Th` / `Dh` | `kohomadha` → `කොහොමද` |
| ට / ඩ / ණ / ළ | `t` / `d` / `N` / `L` | `ratak` → `රටක්`, `kaLu` → `කළු` |
| ළු / ළූ | `Lu` / `Luu` | `kaLu` → `කළු` |
| රකාරාංශය (`ක්‍ර`) | `<letter>r` | `krama` → `ක්‍රම` |
| යංශය (`්‍ය`) | `<letter>Y` or `<letter>\y` | `dhYaana` → `ධ්‍යාන` |
| රේඵය (`ර්`) | `R` or `\r` before letter | `maRma` → `මර්ම` |
| ගැයනුකිත්ත (`ෘ` / `ෲ`) | `<letter>ru` / `<letter>ruu` | `kruthi` → `කෘති` |

> **Tip:** Press **`Ctrl + K`** anytime inside the app to browse or search every character mapping interactively.

---

## 6. Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl + Enter` | Copy Sinhala output & save snapshot to History |
| `Ctrl + Shift + V` | Paste clipboard Singlish, convert, and copy Sinhala result |
| `Ctrl + K` | Toggle Transliteration Scheme Reference |
| `Ctrl + H` | Toggle Conversion History |
| `Ctrl + L` | Clear both editors |
| `Ctrl + D` | Switch Dark / Light theme |

---

## 7. Settings Location

Your preferences (theme, selected font, font sizes, toggles, and saved history) are stored automatically in:
`%APPDATA%\SinglishStudio\settings.json`
