from collections import Counter
from typing import Dict
import unicodedata


def strip_accents(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def starts_with_vowel(s: str, h_is_vowel=False) -> bool:
    if len(s) == 0:
        return False
    vowels = ["a", "e", "i", "o", "u"]
    if h_is_vowel:
        vowels.append("h")
    return strip_accents(s)[0] in vowels


def get_common_letters(s1: str, s2: str) -> Dict[str, int]:
    common_letters = Counter(s1) & Counter(s2)  # => {'q': 2, 'r': 1}
    return common_letters


def get_common_letter_count(s1: str, s2: str) -> int:
    return sum(get_common_letters(s1, s2).values())


def unicodefix(s):
    # Fix Python 2.x.
    try:
        return s.decode("utf-8")
    except AttributeError:
        return s
