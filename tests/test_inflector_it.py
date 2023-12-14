# -*- coding: utf-8 -*-

import pytest

from verbecc import Conjugator

cg = Conjugator(lang='it')

def test_all_verbs_have_templates():
    verbs = cg.get_verbs()
    template_names = cg.get_template_names()
    missing_templates = set()
    for verb in verbs:
        if verb.template not in template_names:
            missing_templates.add(verb.template)
    assert len(missing_templates) == 0

test_it_conjugate_mood_tense_data = [
    ('avere', 'indicativo', 'presente',
        ['io ho', 'tu hai', 'lui ha', 'noi abbiamo', 'voi avete', 'loro hanno']),
    ('avere', 'indicativo', 'imperfetto',
        ['io avevo', 'tu avevi', 'lui aveva', 'noi avevamo', 'voi avevate', 'loro avevano']),
    ('avere', 'indicativo', 'passato-remoto',
        ['io ebbi', 'tu avesti', 'lui ebbe', 'noi avemmo', 'voi aveste', 'loro ebbero']),
    ('avere', 'indicativo', 'futuro',
        ['io avrò', 'tu avrai', 'lui avrà', 'noi avremo', 'voi avrete', 'loro avranno'])
]

@pytest.mark.parametrize("infinitive,mood,tense,expected_result",
                         test_it_conjugate_mood_tense_data)
def test_inflector_it_conjugate_mood_tense(infinitive, mood, tense, expected_result):
    assert cg.conjugate_mood_tense(infinitive, mood, tense) == expected_result

def test_inflector_it_conjugate():
    assert cg.conjugate('avere') != None

def test_inflector_it_add_subjunctive_relative_pronoun():
    assert cg._inflector._add_subjunctive_relative_pronoun('io abbia', '') == 'che io abbia'

test_inflector_it_get_default_pronoun_data = [
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
    ('3p', 'm', False, 'loro'),
    ('3p', 'm', True, 'si'),
    ('3p', 'f', False, 'loro'),
    ('3p', 'f', True, 'si')
]

@pytest.mark.parametrize("person,gender,is_reflexive,expected_result",
                         test_inflector_it_get_default_pronoun_data)
def test_inflector_it_get_default_pronoun(person, gender, is_reflexive, expected_result):
    assert cg._inflector._get_default_pronoun(person, gender, is_reflexive=is_reflexive) == expected_result
