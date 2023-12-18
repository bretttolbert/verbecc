# -*- coding: utf-8 -*-

import unicodedata


def strip_accents(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def starts_with_vowel(s: str) -> bool:
    if len(s) == 0:
        return False
    return strip_accents(s)[0] in ("a", "e", "i", "o", "u")


def unicodefix(s):
    # Fix Python 2.x.
    try:
        return s.decode("utf-8")
    except AttributeError:
        return s
