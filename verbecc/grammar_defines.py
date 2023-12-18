# -*- coding: utf-8 -*-

from typing import Tuple

# This refers to grammatical person ('usted' is 3s despite being semantically 2p)
PERSONS: Tuple[str, str, str, str, str, str] = ("1s", "2s", "3s", "1p", "2p", "3p")

IMPERATIVE_PRESENT_PERSONS: Tuple[str, str, str] = ("2s", "1p", "2p")

PARTICIPLE_INFLECTIONS: Tuple[str, str, str, str] = ("ms", "mp", "fs", "fp")

ALPHABET = {
    "fr": {"vowels": "aáàâeêéèiîïoôöœuûùy", "consonants": "bcçdfghjklmnpqrstvwxyz"},
    "en": {"vowels": "aeiouy", "consonants": "bcdfghjklmnpqrstvwxyz"},
    "ca": {"vowels": "aáàâeéèiïoôuûùy", "consonants": "bcdfghjklmnñpqrstvwxyz"},
    "es": {"vowels": "aáeiíoóuúy", "consonants": "bcdfghjklmnñpqrstvwxyz"},
    "it": {"vowels": "aàeéèiìîoóòuùy", "consonants": "bcdfghjklmnpqrstvwxyz"},
    "pt": {"vowels": "aàãááeêéiíoóõuúy", "consonants": "bcçdfghjklmnpqrstvwxyz"},
    "ro": {"vowels": "aăâeiîouy", "consonants": "bcdfghjklmnpqrsșştțţvwxyz"},
}
