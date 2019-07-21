# -*- coding: utf-8 -*-

import pytest

from verbecc import Conjugator

cg = Conjugator(lang='it')

test_it_conjugate_mood_tense_data = [
    ('avere', 'indicativo', 'Indicativo-presente',
        ['io ho', 'tu hai', 'lui ha', 'noi abbiamo', 'voi avete', 'loro hanno'])
]

@pytest.mark.parametrize("infinitive,mood,tense,expected_result",
                         test_it_conjugate_mood_tense_data)
def test_inflector_it_conjugate_mood_tense(infinitive, mood, tense, expected_result):
    assert cg.conjugate_mood_tense(infinitive, mood, tense) == expected_result

def test_inflector_it_conjugate():
    assert cg.conjugate('avere') != None

def test_inflector_it_add_subjunctive_relative_pronoun():
    assert cg._inflector._add_subjunctive_relative_pronoun('io abbia', '') == 'che io abbia'

test_inflector_pt_get_default_pronoun_data = [
    ('1s', 'm', False, 'io'),
    ('1s', 'm', True, 'mi'),
    ('2s', 'm', False, 'tu'),
    ('2s', 'm', True, 'ti'),
    ('3s', 'm', False, 'lui'),
    ('3s', 'm', True, 'si'),
    ('3s', 'f', False, 'lei'),
    ('3s', 'f', True, 'si'),
    ('1p', 'm', False, 'noi'),
    ('1p', 'm', True, 'ci'),
    ('2p', 'm', False, 'voi'),
    ('2p', 'm', True, 'vi'),
    ('3s', 'm', False, 'loro'),
    ('3s', 'm', True, 'si'),
    ('3s', 'f', False, 'loro'),
    ('3s', 'f', True, 'si')
]

@pytest.mark.parametrize("person,gender,is_reflexive,expected_result",
                         test_inflector_pt_get_default_pronoun_data)
def test_inflector_pt_get_default_pronoun(person, gender, is_reflexive, expected_result):
    cg._inflector._get_default_pronoun(person, is_reflexive=is_reflexive) == expected_result
