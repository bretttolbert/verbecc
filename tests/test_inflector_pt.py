# -*- coding: utf-8 -*-

import pytest

from verbecc import inflector_pt

inf = inflector_pt.InflectorPt()

test_es_conjugate_mood_tense_data = [
    ('ter', 'Indicativo', 'Indicativo-presente',
        ['eu tenho', 'tu tens', 'ele tem', 'nós temos', 'vós tendes', 'eles têm']),
    ('ter', 'Indicativo', 'Indicativo-pretérito-perfeito-simples',
        ['eu tive', 'tu tiveste', 'ele teve', 'nós tivemos', 'vós tivestes', 'eles tiveram']),
    ('ter', 'Indicativo', 'Indicativo-pretérito-imperfeito',
        ['eu tinha', 'tu tinhas', 'ele tinha', 'nós tínhamos', 'vós tínheis', 'eles tinham']),
    ('ter', 'Indicativo', 'Indicativo-Pretérito-Mais-que-Perfeito-Simples',
        ['eu tivera', 'tu tiveras', 'ele tivera', 'nós tivéramos', 'vós tivéreis', 'eles tiveram'])
]

@pytest.mark.parametrize("infinitive,mood,tense,expected_result",
                         test_es_conjugate_mood_tense_data)
def test_inflector_pt_conjugate_mood_tense(infinitive, mood, tense, expected_result):
    assert inf.conjugate_mood_tense(infinitive, mood, tense) == expected_result
