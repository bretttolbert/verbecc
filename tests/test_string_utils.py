# -*- coding: utf-8 -*-

from verbecc.string_utils import (
    starts_with_vowel,
    strip_accents,
    unicodefix
)


def test_starts_with_vowel():
    assert starts_with_vowel(u"aller")
    assert not starts_with_vowel(u"banane")
    assert starts_with_vowel(u"éparpiller")
    assert not starts_with_vowel(u"yodler")


def test_strip_accents():
    assert strip_accents(u"français, être, égalité, très") \
        == u"francais, etre, egalite, tres"


def test_unicodefix():
    assert unicodefix("éparpiller") == u'éparpiller'
