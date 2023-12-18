# -*- coding: utf-8 -*-

from verbecc.string_utils import starts_with_vowel, strip_accents, unicodefix


def test_starts_with_vowel():
    assert starts_with_vowel("aller")
    assert not starts_with_vowel("banane")
    assert starts_with_vowel("éparpiller")
    assert not starts_with_vowel("yodler")
    assert not starts_with_vowel("")


def test_strip_accents():
    assert (
        strip_accents("français, être, égalité, très")
        == "francais, etre, egalite, tres"
    )


def test_unicodefix():
    assert unicodefix("éparpiller") == "éparpiller"
