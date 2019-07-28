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
