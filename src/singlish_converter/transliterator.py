"""UCSC Singlish-to-Sinhala Unicode transliteration engine.

Implements the classic UCSC Real Time Unicode Converter mapping with proper
Unicode Zero-Width Joiners (U+200D), accurate longest-match ordering for
nasalized consonants (nndh before nnd) and Luu/Lu, and optional inline
raw-text preservation using backticks (`...`).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

ZWJ = "\u200D"
HAL = "\u0DCA"

# Vowels: (singlish_pattern_regex, independent_sinhala, dependent_modifier)
# Ordered from longest/most-specific to shortest so multi-char forms match first.
VOWELS: tuple[tuple[str, str, str], ...] = (
    (r"oo", "ඌ", "ූ"),
    (r"o\)", "ඕ", "ෝ"),
    (r"oe", "ඕ", "ෝ"),
    (r"aa", "ආ", "ා"),
    (r"a\)", "ආ", "ා"),
    (r"Aa", "ඈ", "ෑ"),
    (r"A\)", "ඈ", "ෑ"),
    (r"ae", "ඈ", "ෑ"),
    (r"ii", "ඊ", "ී"),
    (r"i\)", "ඊ", "ී"),
    (r"ie", "ඊ", "ී"),
    (r"ee", "ඊ", "ී"),
    (r"ea", "ඒ", "ේ"),
    (r"e\)", "ඒ", "ේ"),
    (r"ei", "ඒ", "ේ"),
    (r"uu", "ඌ", "ූ"),
    (r"u\)", "ඌ", "ූ"),
    (r"au", "ඖ", "ෞ"),
    (r"/\\a", "ඇ", "ැ"),
    (r"\\a", "ඇ", "ැ"),
    (r"/a", "ඇ", "ැ"),
    (r"a", "අ", ""),
    (r"A", "ඇ", "ැ"),
    (r"i", "ඉ", "ි"),
    (r"e", "එ", "ෙ"),
    (r"u", "උ", "ු"),
    (r"o", "ඔ", "ො"),
    (r"I", "ඓ", "ෛ"),
)

# Special standalone characters and Repaya
SPECIAL_CONSONANTS: tuple[tuple[str, str], ...] = (
    (r"\\n", "ං"),
    (r"\\h", "ඃ"),
    (r"\\N", "ඞ"),
    (r"\\R", "ඍ"),
    (r"R", f"ර්{ZWJ}"),
    (r"\\r", f"ර්{ZWJ}"),
)

# Consonants: (singlish_regex, sinhala_base)
# Ordered so longer sequences (e.g. nndh before nnd, th/dh/sh before t/d/s) match first.
# 'r' is placed last so Rakaransha combinations resolve cleanly.
CONSONANTS: tuple[tuple[str, str], ...] = (
    (r"nndh", "ඳ"),
    (r"nnd", "ඬ"),
    (r"nng", "ඟ"),
    (r"Th", "ථ"),
    (r"Dh", "ධ"),
    (r"gh", "ඝ"),
    (r"Ch", "ඡ"),
    (r"ph", "ඵ"),
    (r"bh", "භ"),
    (r"sh", "ශ"),
    (r"Sh", "ෂ"),
    (r"GN", "ඥ"),
    (r"KN", "ඤ"),
    (r"dh", "ද"),
    (r"ch", "ච"),
    (r"kh", "ඛ"),
    (r"th", "ත"),
    (r"t", "ට"),
    (r"k", "ක"),
    (r"d", "ඩ"),
    (r"n", "න"),
    (r"p", "ප"),
    (r"b", "බ"),
    (r"m", "ම"),
    (r"\\y", f"{ZWJ}ය"),
    (r"Y", f"{ZWJ}ය"),
    (r"y", "ය"),
    (r"j", "ජ"),
    (r"l", "ල"),
    (r"v", "ව"),
    (r"w", "ව"),
    (r"s", "ස"),
    (r"h", "හ"),
    (r"N", "ණ"),
    (r"L", "ළ"),
    (r"K", "ඛ"),
    (r"G", "ඝ"),
    (r"T", "ඨ"),
    (r"D", "ඪ"),
    (r"P", "ඵ"),
    (r"B", "ඹ"),
    (r"f", "ෆ"),
    (r"q", "ඣ"),
    (r"g", "ග"),
    (r"r", "ර"),
)

# Special pre-combined syllables that include inherent vowel u/uu
FIXED_SYLLABLES: tuple[tuple[str, str], ...] = (
    (r"Luu", "ළූ"),
    (r"Lu", "ළු"),
)

# Special vowel-sign auxiliaries attached to consonants (ruu -> ෲ, ru -> ෘ)
SPECIAL_CHARS: tuple[tuple[str, str], ...] = (
    (r"ruu", "ෲ"),
    (r"ru", "ෘ"),
)


def _build_rules() -> list[tuple[re.Pattern[str], str]]:
    """Pre-compile ordered regex substitution rules for fast real-time conversion."""
    rules: list[tuple[re.Pattern[str], str]] = []

    # 1. Special consonants (anusvara, visarga, repaya, etc.)
    for pat, uni in SPECIAL_CONSONANTS:
        rules.append((re.compile(pat), uni))

    # 2. Fixed syllables (Luu, Lu) before general L consonant rules
    for pat, uni in FIXED_SYLLABLES:
        rules.append((re.compile(pat), uni))

    # 3. Consonants + special chars (e.g., kru -> කෘ, kruu -> කෲ)
    for sp_pat, sp_uni in SPECIAL_CHARS:
        for c_pat, c_uni in CONSONANTS:
            rules.append((re.compile(c_pat + sp_pat), c_uni + sp_uni))

    # 4. Consonants + Rakaransha + vowel modifiers (e.g., kra -> ක්‍ර, krie -> ක්‍රී)
    #    Skip 'r' consonant itself so 'rr' isn't malformed before 'r' rules.
    for c_pat, c_uni in CONSONANTS:
        if c_pat == "r":
            continue
        for v_pat, _, v_mod in VOWELS:
            rules.append(
                (re.compile(f"{c_pat}r{v_pat}"), f"{c_uni}{HAL}{ZWJ}ර{v_mod}")
            )
        rules.append((re.compile(f"{c_pat}r"), f"{c_uni}{HAL}{ZWJ}ර"))

    # 5. Consonants + vowel modifiers (e.g., ka -> ක, kaa -> කා, ki -> කි)
    for c_pat, c_uni in CONSONANTS:
        for v_pat, _, v_mod in VOWELS:
            rules.append((re.compile(c_pat + v_pat), c_uni + v_mod))

    # 6. Remaining bare consonants + HAL (virama ්)
    for c_pat, c_uni in CONSONANTS:
        rules.append((re.compile(c_pat), c_uni + HAL))

    # 7. Independent vowels
    for v_pat, v_uni, _ in VOWELS:
        rules.append((re.compile(v_pat), v_uni))

    return rules


_COMPILED_RULES = _build_rules()
_BACKTICK_SPAN_RE = re.compile(r"(`[^`]*`)")


@dataclass(frozen=True)
class ConversionStats:
    """Summary metrics for a Singlish-to-Sinhala conversion."""

    input_chars: int
    output_chars: int
    words: int
    lines: int


def convert_segment(text: str) -> str:
    """Convert a plain Singlish string segment into Sinhala Unicode."""
    if not text:
        return ""
    result = text
    for pattern, replacement in _COMPILED_RULES:
        result = pattern.sub(replacement, result)
    return result


def transliterate(text: str, preserve_backticks: bool = False) -> str:
    """Transliterate Singlish text to Sinhala Unicode.

    Args:
        text: Source Singlish text.
        preserve_backticks: When True, spans wrapped in backticks (`like this`)
            are kept verbatim in English/ASCII without the backticks.
    """
    if not text:
        return ""

    if not preserve_backticks or "`" not in text:
        return convert_segment(text)

    parts = _BACKTICK_SPAN_RE.split(text)
    out: list[str] = []
    for part in parts:
        if len(part) >= 2 and part.startswith("`") and part.endswith("`"):
            out.append(part[1:-1])
        else:
            out.append(convert_segment(part))
    return "".join(out)


def compute_stats(source: str, converted: str) -> ConversionStats:
    """Compute character, word, and line counts for source and converted text."""
    words = len(converted.split()) if converted.strip() else 0
    lines = converted.count("\n") + 1 if converted else 0
    return ConversionStats(
        input_chars=len(source),
        output_chars=len(converted),
        words=words,
        lines=lines,
    )


def inspect_codepoints(text: str, limit: int = 12) -> str:
    """Return a compact Unicode codepoint breakdown for the first `limit` chars."""
    if not text:
        return "No selection"
    sample = text[:limit]
    parts = [f"{ch if ch not in (' ', '\n', '\t', ZWJ) else ('ZWJ' if ch == ZWJ else repr(ch))} (U+{ord(ch):04X})" for ch in sample]
    suffix = " ..." if len(text) > limit else ""
    return "  ·  ".join(parts) + suffix
