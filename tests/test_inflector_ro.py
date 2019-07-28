# -*- coding: utf-8 -*-

import pytest

from verbecc import Conjugator

cg = Conjugator(lang='ro')

test_ro_conjugate_mood_tense_data = [
    ('avea', 'prezent', 'Prezent-Prezent',
        ['eu am', 'tu ai', 'el a', 'noi am', 'voi aţi', 'ei au'])
]

@pytest.mark.parametrize("infinitive,mood,tense,expected_result",
                         test_ro_conjugate_mood_tense_data)
def test_inflector_ro_conjugate_mood_tense(infinitive, mood, tense, expected_result):
    assert cg.conjugate_mood_tense(infinitive, mood, tense) == expected_result

test_inflector_ro_get_default_pronoun_data = [
    ('1s', 'm', False, 'eu'),
    ('1s', 'm', True, 'eu mă'),
    ('2s', 'm', False, 'tu'),
    ('2s', 'm', True, 'tu te'),
    ('3s', 'm', False, 'el'),
    ('3s', 'm', True, 'el se'),
    ('3s', 'f', False, 'ea'),
    ('3s', 'f', True, 'ea se'),
    ('1p', 'm', False, 'noi'),
    ('1p', 'm', True, 'noi ne'),
    ('2p', 'm', False, 'voi'),
    ('2p', 'm', True, 'voi vă'),
    ('3p', 'm', False, 'ei'),
    ('3p', 'm', True, 'ei se'),
    ('3p', 'f', False, 'ele'),
    ('3p', 'f', True, 'ele se')
]

@pytest.mark.parametrize("person,gender,is_reflexive,expected_result",
                         test_inflector_ro_get_default_pronoun_data)
def test_inflector_ro_get_default_pronoun(person, gender, is_reflexive, expected_result):
    assert cg._inflector._get_default_pronoun(person, gender, is_reflexive=is_reflexive) == expected_result
