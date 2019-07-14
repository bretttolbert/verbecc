# -*- coding: utf-8 -*-

import pytest

from verbecc import inflector_pt

inf = inflector_pt.InflectorPt()

test_es_conjugate_mood_tense_data = [
    ('ter', 'Indicativo', 'presente',
        ['eu tenho', 'tu tens', 'ele tem', 'nós temos', 'vós tendes', 'eles têm']),
    ('ter', 'Indicativo', 'pretérito-perfeito',
        ['eu tive', 'tu tiveste', 'ele teve', 'nós tivemos', 'vós tivestes', 'eles tiveram']),
    ('ter', 'Indicativo', 'pretérito-imperfeito',
        ['eu tinha', 'tu tinhas', 'ele tinha', 'nós tínhamos', 'vós tínheis', 'eles tinham']),
    ('ter', 'Indicativo', 'pretérito-mais-que-perfeito',
        ['eu tivera', 'tu tiveras', 'ele tivera', 'nós tivéramos', 'vós tivéreis', 'eles tiveram']),
    ('ter', 'Indicativo', 'pretérito-perfeito-composto',
        ['eu tenho tido', 'tu tens tido', 'ele tem tido', 'nós temos tido', 'vós tendes tido', 'eles têm tido']),
    ('ter', 'Indicativo', 'pretérito-mais-que-perfeito-composto',
        ['eu tinha tido', 'tu tinhas tido', 'ele tinha tido', 'nós tínhamos tido', 'vós tínheis tido', 'eles tinham tido']),
    ('ter', 'Indicativo', 'pretérito-mais-que-perfeito-anterior',
        ['eu tivera tido', 'tu tiveras tido', 'ele tivera tido', 'nós tivéramos tido', 'vós tivéreis tido', 'eles tiveram tido']),
    ('ter', 'Indicativo', 'futuro-do-presente',
        ['eu terei', 'tu terás', 'ele terá', 'nós teremos', 'vós tereis', 'eles terão']),
    ('ter', 'Indicativo', 'futuro-do-presente-composto',
        ['eu terei tido', 'tu terás tido', 'ele terá tido', 'nós teremos tido', 'vós tereis tido', 'eles terão tido']),
    ('ter', 'Subjuntivo', 'presente',
        ['que eu tenha', 'que tu tenhas', 'que ele tenha', 'que nós tenhamos', 'que vós tenhais', 'que eles tenham']),
    ('ter', 'Subjuntivo', 'pretérito-perfeito',
        ['eu tenha tido', 'tu tenhas tido', 'ele tenha tido', 'nós tenhamos tido', 'vós tenhais tido', 'eles tenham tido']),
    ('ter', 'Subjuntivo', 'pretérito-imperfeito',
        ['se eu tivesse', 'se tu tivesses', 'se ele tivesse', 'se nós tivéssemos', 'se vós tivésseis', 'se eles tivessem']),
    ('ter', 'Subjuntivo', 'pretérito-mais-que-perfeito',
        ['eu tivesse tido', 'tu tivesses tido', 'ele tivesse tido', 'nós tivéssemos tido', 'vós tivésseis tido', 'eles tivessem tido']),
    ('ter', 'Subjuntivo', 'futuro',
        ['quando eu tiver', 'quando tu tiveres', 'quando ele tiver', 'quando nós tivermos', 'quando vós tiverdes', 'quando eles tiverem']),
    ('ter', 'Subjuntivo', 'futuro-composto',
        ['eu tiver tido', 'tu tiveres tido', 'ele tiver tido', 'nós tivermos tido', 'vós tiverdes tido', 'eles tiverem tido']),
    ('ter', 'Condicional', 'futuro-do-pretérito',
        ['eu teria', 'tu terias', 'ele teria', 'nós teríamos', 'vós teríeis', 'eles teriam']),
    ('ter', 'Condicional', 'futuro-do-pretérito-composto',
        ['eu teria tido', 'tu terias tido', 'ele teria tido', 'nós teríamos tido', 'vós teríeis tido', 'eles teriam tido']),
    ('ter', 'Infinitivo', 'infinitivo-pessoal-presente',
        ['ter', 'teres', 'ter', 'termos', 'terdes', 'terem']),
    ('ter', 'Infinitivo', 'infinitivo-pessoal-composto',
        ['ter tido', 'teres tido', 'ter tido', 'termos tido', 'terdes tido', 'terem tido'])
]

@pytest.mark.parametrize("infinitive,mood,tense,expected_result",
                         test_es_conjugate_mood_tense_data)
def test_inflector_pt_conjugate_mood_tense(infinitive, mood, tense, expected_result):
    assert inf.conjugate_mood_tense(infinitive, mood, tense) == expected_result
