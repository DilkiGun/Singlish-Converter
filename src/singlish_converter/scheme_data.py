"""Structured UCSC Singlish transliteration scheme data and sample presets."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SchemeEntry:
    """Single transliteration mapping card for the interactive reference."""

    category: str
    sub_group: str
    sinhala: str
    keys: tuple[str, ...]
    example_sinhala: str = ""
    example_key: str = ""
    note: str = ""


VOWEL_ENTRIES: tuple[SchemeEntry, ...] = (
    SchemeEntry("Vowels", "Short", "අ", ("a",)),
    SchemeEntry("Vowels", "Long", "ආ", ("aa", "a)")),
    SchemeEntry("Vowels", "Short", "ඇ", ("A", r"\a")),
    SchemeEntry("Vowels", "Long", "ඈ", ("Aa", "A)", "ae")),
    SchemeEntry("Vowels", "Short", "ඉ", ("i",)),
    SchemeEntry("Vowels", "Long", "ඊ", ("ii", "i)", "ie", "ee")),
    SchemeEntry("Vowels", "Short", "උ", ("u",)),
    SchemeEntry("Vowels", "Long", "ඌ", ("uu", "u)", "oo")),
    SchemeEntry("Vowels", "Short", "එ", ("e",)),
    SchemeEntry("Vowels", "Long", "ඒ", ("ea", "e)", "ei")),
    SchemeEntry("Vowels", "Short", "ඔ", ("o",)),
    SchemeEntry("Vowels", "Long", "ඕ", ("oe", "o)")),
    SchemeEntry("Vowels", "Diphthong", "ඓ", ("I",)),
    SchemeEntry("Vowels", "Diphthong", "ඖ", ("au",)),
)

AUXILIARY_ENTRIES: tuple[SchemeEntry, ...] = (
    SchemeEntry("Auxiliaries", "Special", "ර්\u200D", (r"\r", "R"), "මර්\u200Dම", r"ma\rma / maRma", "Repaya (before consonant)"),
    SchemeEntry("Auxiliaries", "Special", "්\u200Dය", ("Y", r"\y"), "ධ්\u200Dය", r"dhYa / dh\ya", "Yansaya (after consonant)"),
    SchemeEntry("Auxiliaries", "Special", "ක්\u200Dර", ("r",), "ක්‍රම", "krama", "Rakaransha (after consonant)"),
    SchemeEntry("Auxiliaries", "Vowel Signs", "ෘ", ("ru",), "කෘති", "kruthi", "Gayanukitta"),
    SchemeEntry("Auxiliaries", "Vowel Signs", "ෲ", ("ruu",), "කෲර", "kruura", "Long Gayanukitta"),
    SchemeEntry("Auxiliaries", "Vowel Signs", "ෞ", ("au",), "චෞර", "chaura"),
    SchemeEntry("Auxiliaries", "Vowel Signs", "ෛ", ("I",), "මෛත්‍රී", "mIthrie"),
    SchemeEntry("Auxiliaries", "Nasal (Sanyaka)", "ඬ", ("nnd",), "හඬ", "hannda"),
    SchemeEntry("Auxiliaries", "Nasal (Sanyaka)", "ඳ", ("nndh",), "හඳ", "hanndha"),
    SchemeEntry("Auxiliaries", "Nasal (Sanyaka)", "ඟ", ("nng",), "ගඟ", "gannga"),
)

CONSONANT_ENTRIES: tuple[SchemeEntry, ...] = (
    # Common
    SchemeEntry("Consonants", "Common", "ක", ("k",)),
    SchemeEntry("Consonants", "Common", "ග", ("g",)),
    SchemeEntry("Consonants", "Common", "ච", ("ch",)),
    SchemeEntry("Consonants", "Common", "ජ", ("j",)),
    SchemeEntry("Consonants", "Common", "ට", ("t",)),
    SchemeEntry("Consonants", "Common", "ඩ", ("d",)),
    SchemeEntry("Consonants", "Common", "ත", ("th",)),
    SchemeEntry("Consonants", "Common", "ද", ("dh",)),
    SchemeEntry("Consonants", "Common", "න", ("n",)),
    SchemeEntry("Consonants", "Common", "ප", ("p",)),
    SchemeEntry("Consonants", "Common", "බ", ("b",)),
    SchemeEntry("Consonants", "Common", "ම", ("m",)),
    SchemeEntry("Consonants", "Common", "ය", ("y",)),
    SchemeEntry("Consonants", "Common", "ර", ("r",)),
    SchemeEntry("Consonants", "Common", "ල", ("l",)),
    SchemeEntry("Consonants", "Common", "ව", ("w", "v")),
    SchemeEntry("Consonants", "Common", "ස", ("s",)),
    SchemeEntry("Consonants", "Common", "හ", ("h",)),
    SchemeEntry("Consonants", "Common", "ණ", ("N",)),
    SchemeEntry("Consonants", "Common", "ළ", ("L",)),
    # Aspirated
    SchemeEntry("Consonants", "Aspirated", "ඛ", ("kh", "K")),
    SchemeEntry("Consonants", "Aspirated", "ඝ", ("gh", "G")),
    SchemeEntry("Consonants", "Aspirated", "ඡ", ("Ch",)),
    SchemeEntry("Consonants", "Aspirated", "ඨ", ("T",)),
    SchemeEntry("Consonants", "Aspirated", "ඪ", ("D",)),
    SchemeEntry("Consonants", "Aspirated", "ථ", ("Th",)),
    SchemeEntry("Consonants", "Aspirated", "ධ", ("Dh",)),
    SchemeEntry("Consonants", "Aspirated", "ඵ", ("ph", "P")),
    SchemeEntry("Consonants", "Aspirated", "භ", ("bh",)),
    # Special
    SchemeEntry("Consonants", "Special", "ඹ", ("B",)),
    SchemeEntry("Consonants", "Special", "ශ", ("sh",)),
    SchemeEntry("Consonants", "Special", "ෂ", ("Sh",)),
    SchemeEntry("Consonants", "Special", "ෆ", ("f",)),
    SchemeEntry("Consonants", "Special", "ඥ", ("GN",)),
    SchemeEntry("Consonants", "Special", "ඤ", ("KN",)),
    SchemeEntry("Consonants", "Special", "ඣ", ("q",)),
    SchemeEntry("Consonants", "Special", "ළු", ("Lu",)),
    SchemeEntry("Consonants", "Special", "ළූ", ("Luu",)),
    # Standalone
    SchemeEntry("Consonants", "Standalone", "ං", (r"\n",)),
    SchemeEntry("Consonants", "Standalone", "ඃ", (r"\h",)),
    SchemeEntry("Consonants", "Standalone", "ඞ", (r"\N",)),
    SchemeEntry("Consonants", "Standalone", "ඍ", (r"\R",)),
)

DERIVING_CONSONANTS: tuple[tuple[str, str], ...] = (
    ("ක්", "k"),
    ("ක", "ka"),
    ("කා", "kaa"),
    ("කැ", "kA"),
    ("කෑ", "kAa"),
    ("කි", "ki"),
    ("කී", "kie"),
    ("කු", "ku"),
    ("කූ", "kuu"),
    ("කෙ", "ke"),
    ("කේ", "kei"),
    ("කො", "ko"),
    ("කෝ", "koe"),
    ("කෞ", "kau"),
    ("ක්\u200Dර", "kra"),
    ("ක්\u200Dරා", "kraa"),
    ("ක්\u200Dරැ", "krA"),
    ("ක්\u200Dරෑ", "krAa"),
    ("ක්\u200Dරි", "kri"),
    ("ක්\u200Dරී", "krie"),
    ("කෘ", "kru"),
    ("කෲ", "kruu"),
    ("ක්\u200Dරෙ", "kre"),
    ("ක්\u200Dරේ", "krei"),
    ("ක්\u200Dරො", "kro"),
    ("ක්\u200Dරෝ", "kroe"),
)

QUICK_CHIPS: tuple[tuple[str, str], ...] = (
    ("ං", r"\n"),
    ("ඃ", r"\h"),
    ("ඇ", "A"),
    ("ඈ", "Aa"),
    ("ඳ", "nndh"),
    ("ඬ", "nnd"),
    ("ඟ", "nng"),
    ("ශ", "sh"),
    ("ෂ", "Sh"),
    ("ළු", "Lu"),
    ("ඤ", "KN"),
    ("ඥ", "GN"),
    ("ර්‍", "R"),
    ("්‍ය", "Y"),
)

SAMPLE_PRESETS: tuple[tuple[str, str], ...] = (
    (
        "Greeting (ආයුබෝවන්)",
        "aayuboevan! oyaata kohomadha? mama ho\\ndhi\\n innavaa.",
    ),
    (
        "Sri Lanka & Culture",
        "shrie la\\nkaava kiyannee harima lassana ratak. api si\\nhala yunikoeD bhaavithaa karamu.",
    ),
    (
        "Conjuncts (Rakaransha / Yansaya / Repaya)",
        "krama, shrie, dhYaana, maRma, kruthi, kruura, hannda, hanndha, gannga.",
    ),
    (
        "Mixed English (Use `...` toggle)",
        "mama adha `Python` saha `PySide6` valin aluth `Singlish Studio` app ekak hAdhuvaa.",
    ),
)

ALL_SCHEME_ENTRIES: tuple[SchemeEntry, ...] = (
    VOWEL_ENTRIES + AUXILIARY_ENTRIES + CONSONANT_ENTRIES
)
