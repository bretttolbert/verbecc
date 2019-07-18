# -*- coding: utf-8 -*-

import pytest

from verbecc import Conjugator

cg = Conjugator(lang='pt')

test_es_conjugate_mood_tense_data = [
    ('ter', 'indicativo', 'presente',
        ['eu tenho', 'tu tens', 'ele tem', 'nós temos', 'vós tendes', 'eles têm']),
    ('ter', 'indicativo', 'pretérito-perfeito',
        ['eu tive', 'tu tiveste', 'ele teve', 'nós tivemos', 'vós tivestes', 'eles tiveram']),
    ('ter', 'indicativo', 'pretérito-imperfeito',
        ['eu tinha', 'tu tinhas', 'ele tinha', 'nós tínhamos', 'vós tínheis', 'eles tinham']),
    ('ter', 'indicativo', 'pretérito-mais-que-perfeito',
        ['eu tivera', 'tu tiveras', 'ele tivera', 'nós tivéramos', 'vós tivéreis', 'eles tiveram']),
    ('ter', 'indicativo', 'pretérito-perfeito-composto',
        ['eu tenho tido', 'tu tens tido', 'ele tem tido', 'nós temos tido', 'vós tendes tido', 'eles têm tido']),
    ('ter', 'indicativo', 'pretérito-mais-que-perfeito-composto',
        ['eu tinha tido', 'tu tinhas tido', 'ele tinha tido', 'nós tínhamos tido', 'vós tínheis tido', 'eles tinham tido']),
    ('ter', 'indicativo', 'pretérito-mais-que-perfeito-anterior',
        ['eu tivera tido', 'tu tiveras tido', 'ele tivera tido', 'nós tivéramos tido', 'vós tivéreis tido', 'eles tiveram tido']),
    ('ter', 'indicativo', 'futuro-do-presente',
        ['eu terei', 'tu terás', 'ele terá', 'nós teremos', 'vós tereis', 'eles terão']),
    ('ter', 'indicativo', 'futuro-do-presente-composto',
        ['eu terei tido', 'tu terás tido', 'ele terá tido', 'nós teremos tido', 'vós tereis tido', 'eles terão tido']),
    ('ter', 'subjuntivo', 'presente',
        ['que eu tenha', 'que tu tenhas', 'que ele tenha', 'que nós tenhamos', 'que vós tenhais', 'que eles tenham']),
    ('ter', 'subjuntivo', 'pretérito-perfeito',
        ['eu tenha tido', 'tu tenhas tido', 'ele tenha tido', 'nós tenhamos tido', 'vós tenhais tido', 'eles tenham tido']),
    ('ter', 'subjuntivo', 'pretérito-imperfeito',
        ['se eu tivesse', 'se tu tivesses', 'se ele tivesse', 'se nós tivéssemos', 'se vós tivésseis', 'se eles tivessem']),
    ('ter', 'subjuntivo', 'pretérito-mais-que-perfeito',
        ['eu tivesse tido', 'tu tivesses tido', 'ele tivesse tido', 'nós tivéssemos tido', 'vós tivésseis tido', 'eles tivessem tido']),
    ('ter', 'subjuntivo', 'futuro',
        ['quando eu tiver', 'quando tu tiveres', 'quando ele tiver', 'quando nós tivermos', 'quando vós tiverdes', 'quando eles tiverem']),
    ('ter', 'subjuntivo', 'futuro-composto',
        ['eu tiver tido', 'tu tiveres tido', 'ele tiver tido', 'nós tivermos tido', 'vós tiverdes tido', 'eles tiverem tido']),
    ('ter', 'condicional', 'futuro-do-pretérito',
        ['eu teria', 'tu terias', 'ele teria', 'nós teríamos', 'vós teríeis', 'eles teriam']),
    ('ter', 'condicional', 'futuro-do-pretérito-composto',
        ['eu teria tido', 'tu terias tido', 'ele teria tido', 'nós teríamos tido', 'vós teríeis tido', 'eles teriam tido']),
    ('ter', 'infinitivo', 'infinitivo-pessoal-presente',
        ['por ter eu', 'por teres tu', 'por ter ele', 'por termos nós', 'por terdes vós', 'por terem eles']),
    ('ter', 'infinitivo', 'infinitivo-pessoal-composto',
        ['ter tido', 'teres tido', 'ter tido', 'termos tido', 'terdes tido', 'terem tido']),
    ('ter', 'imperativo', 'afirmativo',
        ['-', 'tem tu', 'tenha você', 'tenhamos nós', 'tende vós', 'tenham vocês']),
    ('ter', 'imperativo', 'negativo',
        ['-', 'não tenhas tu', 'não tenha você', 'não tenhamos nós', 'não tenhais vós', 'não tenham vocês'])
]

@pytest.mark.parametrize("infinitive,mood,tense,expected_result",
                         test_es_conjugate_mood_tense_data)
def test_inflector_pt_conjugate_mood_tense(infinitive, mood, tense, expected_result):
    assert cg.conjugate_mood_tense(infinitive, mood, tense) == expected_result

test_inflector_pt_get_default_pronoun_data = [
    ('1s', 'm', False, 'eu'),
    ('1s', 'm', True, 'eu me'),
    ('2s', 'm', False, 'tu'),
    ('2s', 'm', True, 'tu te'),
    ('3s', 'm', False, 'ele'),
    ('3s', 'm', True, 'ele se'),
    ('3s', 'f', False, 'ela'),
    ('3s', 'f', True, 'ela se'),
    ('1p', 'm', False, 'nós'),
    ('1p', 'm', True, 'nós nos'),
    ('2p', 'm', False, 'vós'),
    ('2p', 'm', True, 'vós se'),
    ('3s', 'm', False, 'eles'),
    ('3s', 'm', True, 'eles se'),
    ('3s', 'f', False, 'elas'),
    ('3s', 'f', True, 'elas se')
]

@pytest.mark.parametrize("person,gender,is_reflexive,expected_result",
                         test_inflector_pt_get_default_pronoun_data)
def test_inflector_pt_get_default_pronoun(person, gender, is_reflexive, expected_result):
    cg._inflector._get_default_pronoun(person, is_reflexive=is_reflexive) == expected_result
