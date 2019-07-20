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
