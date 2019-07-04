# -*- coding: utf-8 -*-

import unicodedata


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')

VOWELS = ('a', 'e', 'i', 'o', 'u')

def starts_with_vowel(s):
    if len(s) == 0:
        return False
    return strip_accents(s)[0] in VOWELS

def split_reflexive(infinitive):
    is_reflexive = False
    if infinitive.startswith("se "):
        is_reflexive = True
        infinitive = infinitive[3:]
    elif infinitive.startswith("s'"):
        is_reflexive = True
        infinitive = infinitive[2:]
    return is_reflexive, infinitive

def prepend_with_que(pronoun_string):
    if starts_with_vowel(pronoun_string):
        return "qu'" + pronoun_string
    else:
        return "que " + pronoun_string

def prepend_with_se(s):
    if starts_with_vowel(s):
        return "s'" + s
    else:
        return "se " + s

def unicodefix(s):
    # Fix Python 2.x.
    try:
        return s.decode('utf-8')
    except AttributeError:
        return s
