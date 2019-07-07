# -*- coding: utf-8 -*-

from verbecc.string_utils import (
    prepend_with_que,
    prepend_with_se,
    split_reflexive,
    starts_with_vowel,
    strip_accents,
    unicodefix
)

def test_prepend_with_que():
    assert prepend_with_que("tu manges") == "que tu manges"
    assert prepend_with_que("il mange") == "qu'il mange"
    assert prepend_with_que("elles mangent") == "qu'elles mangent"

def test_prepend_with_se():
    assert prepend_with_se("lever") == "se lever"
    assert prepend_with_se("écrouler") == "s'écrouler"

def test_split_reflexive():
    assert split_reflexive("se lever") == (True, "lever")
    assert split_reflexive("s'écrouler") == (True, "écrouler")
    assert split_reflexive("secouer") == (False, "secouer")

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
