"""Unit tests for the Singlish-to-Sinhala transliteration engine."""

from singlish_converter.transliterator import ZWJ, compute_stats, inspect_codepoints, transliterate


def test_short_and_long_vowels() -> None:
    assert transliterate("a aa A Aa i ii u uu e ea o oe I au") == (
        "අ ආ ඇ ඈ ඉ ඊ උ ඌ එ ඒ ඔ ඕ ඓ ඖ"
    )
    assert transliterate("a) A) i) ie ee e) ei o) u) oo ae") == (
        "ආ ඈ ඊ ඊ ඊ ඒ ඒ ඕ ඌ ඌ ඈ"
    )
    assert transliterate(r"\a") == "ඇ"


def test_consonants_and_modifiers() -> None:
    assert transliterate("k ka kaa kA kAa ki kie ku kuu ke kei ko koe kau") == (
        "ක් ක කා කැ කෑ කි කී කු කූ කෙ කේ කො කෝ කෞ"
    )


def test_nasalized_consonants() -> None:
    assert transliterate("hannda") == "හඬ"
    assert transliterate("hanndha") == "හඳ"
    assert transliterate("gannga") == "ගඟ"


def test_rakaransha_and_special_vowel_signs() -> None:
    assert transliterate("kra kraa krA krAa kri krie kru kruu kre krei kro kroe") == (
        f"ක්{ZWJ}ර ක්{ZWJ}රා ක්{ZWJ}රැ ක්{ZWJ}රෑ ක්{ZWJ}රි ක්{ZWJ}රී කෘ කෲ ක්{ZWJ}රෙ ක්{ZWJ}රේ ක්{ZWJ}රො ක්{ZWJ}රෝ"
    )
    assert transliterate("shrie") == f"ශ්{ZWJ}රී"


def test_special_auxiliaries_and_standalone() -> None:
    assert transliterate(r"\n \h \N \R") == "ං ඃ ඞ ඍ"
    assert transliterate(r"maRma ma\rma") == f"මර්{ZWJ}ම මර්{ZWJ}ම"
    assert transliterate(r"dhYa dh\ya") == f"ද්{ZWJ}ය ද්{ZWJ}ය"
    assert transliterate("Lu Luu") == "ළු ළූ"


def test_backtick_english_preservation() -> None:
    text = "mama `Python 3.13` saha `Unicode` igena gannavaa."
    assert transliterate(text, preserve_backticks=True) == (
        "මම Python 3.13 සහ Unicode ඉගෙන ගන්නවා."
    )
    # Without backtick preservation, backticks remain literal and text converts
    assert "`" in transliterate(text, preserve_backticks=False)


def test_stats_and_inspector() -> None:
    src = "aayuboevan\nla\\nkaa"
    out = transliterate(src)
    stats = compute_stats(src, out)
    assert stats.input_chars == len(src)
    assert stats.output_chars == len(out)
    assert stats.words == 2
    assert stats.lines == 2
    assert "U+0D9A" in inspect_codepoints("ක්‍ර")
