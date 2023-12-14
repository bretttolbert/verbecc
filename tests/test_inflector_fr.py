# -*- coding: utf-8 -*-

import pytest
from lxml import etree

from verbecc import Conjugator
from verbecc import inflector_fr
from verbecc.tense_template import TenseTemplate
from verbecc.exceptions import ConjugatorError

cg = Conjugator(lang='fr')

def test_all_verbs_have_templates():
    verbs = cg.get_verbs()
    template_names = cg.get_template_names()
    missing_templates = set()
    for verb in verbs:
        if verb.template not in template_names:
            missing_templates.add(verb.template)
    assert len(missing_templates) == 0

inf = inflector_fr.InflectorFr()

def test_add_subjunctive_relative_prounoun():
    assert inf._add_subjunctive_relative_pronoun('tu manges', '') == 'que tu manges'
    assert inf._add_subjunctive_relative_pronoun('il mange', '') == 'qu\'il mange'
    assert inf._add_subjunctive_relative_pronoun('elles mangent', '') == 'qu\'elles mangent'

def test_add_reflexive_pronoun():
    assert inf._add_reflexive_pronoun('lever') == 'se lever'
    assert inf._add_reflexive_pronoun('écrouler') == 's\'écrouler'

def test_split_reflexive():
    assert inf._split_reflexive('se lever') == (True, 'lever')
    assert inf._split_reflexive('s\'écrouler') == (True, 'écrouler')
    assert inf._split_reflexive('secouer') == (False, 'secouer')

inf = inflector_fr.InflectorFr()

test_inflector_fr_verb_can_be_reflexive_data = [
    ('être', False),
    ('lever', True),
    ('pleuvoir', False),
    ('manger', True)
]
@pytest.mark.parametrize('infinitive,expected_result', 
                         test_inflector_fr_verb_can_be_reflexive_data)
def test_inflector_fr_verb_can_be_reflexive(infinitive, expected_result):
    assert inf._verb_can_be_reflexive(infinitive) == expected_result

def test_inflector_fr_impersonal_verbs():
    impersonal_verbs = \
        [v.infinitive for v in inf._verb_parser.verbs
        if inf._is_impersonal_verb(v.infinitive)]
    assert set(impersonal_verbs) == set([
    'advenir',
    'apparoir',
    'bruiner',
    'bruire',
    'chaloir',
    'clore',
    'déclore',
    'échoir',
    'éclore',
    'enclore',
    'falloir',
    'forclore',
    'frire',
    'grêler',
    'messeoir',
    'neiger',
    'pleuvoir',
    'seoir',
    'sourdre'])

def test_inflector_fr_conjugate_simple_mood_tense():
    verb_stem = 'man'
    tense_elem = etree.fromstring(
        """<présent>
        <p><i>ge</i></p>
        <p><i>ges</i></p>
        <p><i>ge</i></p>
        <p><i>geons</i></p>
        <p><i>gez</i></p>
        <p><i>gent</i></p>
        </présent>""")
    tense_name = 'présent'
    tense_template = TenseTemplate(tense_elem)
    out = inf._conjugate_simple_mood_tense(verb_stem, 'indicatif', tense_template)
    assert len(out) == 6
    assert out == ['je mange', 'tu manges', 'il mange', 'nous mangeons', 'vous mangez', 'ils mangent']

def test_inflector_fr_get_verb_stem():
    verb_stem = inf._get_verb_stem('manger', 'man:ger')
    assert verb_stem == 'man'
    verb_stem = inf._get_verb_stem('téléphoner', 'aim:er')
    assert verb_stem == 'téléphon'
    verb_stem = inf._get_verb_stem('vendre', 'ten:dre')
    assert verb_stem == 'ven'
    # In the case of irregular verbs, the verb stem is empty string
    verb_stem = inf._get_verb_stem('aller', ':aller')
    assert verb_stem == ''
    # The infinitive ending must match the template ending
    with pytest.raises(ConjugatorError):
        verb_stem = inf._get_verb_stem('vendre', 'man:ger')

test_inflector_fr_get_default_pronoun_data = [
    ('1s', 'm', False, 'je'),
    ('1s', 'm', True, 'je me'),
    ('2s', 'm', False, 'tu'),
    ('2s', 'm', True, 'tu te'),
    ('3s', 'm', False, 'il'),
    ('3s', 'm', True, 'il se'),
    ('3s', 'f', False, 'elle'),
    ('3s', 'f', True, 'elle se'),
    ('1p', 'm', False, 'nous'),
    ('1p', 'm', True, 'nous nous'),
    ('2p', 'm', False, 'vous'),
    ('2p', 'm', True, 'vous vous'),
    ('3p', 'm', False, 'ils'),
    ('3p', 'm', True, 'ils se'),
    ('3p', 'f', False, 'elles'),
    ('3p', 'f', True, 'elles se')
]

@pytest.mark.parametrize("person,gender,is_reflexive,expected_result",
                         test_inflector_fr_get_default_pronoun_data)
def test_inflector_fr_get_default_pronoun(person, gender, is_reflexive, expected_result):
    assert inf._get_default_pronoun(person, gender, is_reflexive=is_reflexive) == expected_result
