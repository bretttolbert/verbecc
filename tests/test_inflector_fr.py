# -*- coding: utf-8 -*-

import pytest
from lxml import etree

from verbecc import inflector_fr
from verbecc.tense_template import TenseTemplate
from verbecc.exceptions import ConjugatorError

inf = inflector_fr.InflectorFr()

def test_add_subjunctive_relative_prounoun():
    assert inf._add_subjunctive_relative_pronoun("tu manges") == "que tu manges"
    assert inf._add_subjunctive_relative_pronoun("il mange") == "qu'il mange"
    assert inf._add_subjunctive_relative_pronoun("elles mangent") == "qu'elles mangent"

def test_prepend_with_se():
    assert inf._prepend_with_se("lever") == "se lever"
    assert inf._prepend_with_se("écrouler") == "s'écrouler"

def test_split_reflexive():
    assert inf._split_reflexive("se lever") == (True, "lever")
    assert inf._split_reflexive("s'écrouler") == (True, "écrouler")
    assert inf._split_reflexive("secouer") == (False, "secouer")

inf = inflector_fr.InflectorFr()

test_inflector_fr_verb_can_be_reflexive_data = [
    ("être", False),
    ("lever", True),
    ("pleuvoir", False),
    ("manger", True)
]
@pytest.mark.parametrize("infinitive,expected_result", 
                         test_inflector_fr_verb_can_be_reflexive_data)
def test_inflector_fr_verb_can_be_reflexive(infinitive, expected_result):
    assert inf._verb_can_be_reflexive(infinitive) == expected_result

def test_inflector_fr_impersonal_verbs():
    impersonal_verbs = \
        [v.infinitive for v in inf._verb_parser.verbs
        if inf._is_impersonal_verb(v.infinitive)]
    assert set(impersonal_verbs) == set([
    "advenir",
    "apparoir",
    "bruiner",
    "bruire",
    "chaloir",
    "clore",
    "déclore",
    "échoir",
    "éclore",
    "enclore",
    "falloir",
    "forclore",
    "frire",
    "grêler",
    "messeoir",
    "neiger",
    "pleuvoir",
    "seoir",
    "sourdre"])

def test_inflector_fr_conjugate_simple_mood_tense():
    verb_stem = u"man"
    tense_elem = etree.fromstring(
        u"""<présent>
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
    assert out == [u"je mange", u"tu manges", u"il mange", u"nous mangeons", u"vous mangez", u"ils mangent"]

def test_inflector_fr_get_verb_stem():
    verb_stem = inf._get_verb_stem(u"manger", u"man:ger")
    assert verb_stem == u"man"
    verb_stem = inf._get_verb_stem(u"téléphoner", u"aim:er")
    assert verb_stem == u"téléphon"
    verb_stem = inf._get_verb_stem(u"vendre", u"ten:dre")
    assert verb_stem == u"ven"
    # In the case of irregular verbs, the verb stem is empty string
    verb_stem = inf._get_verb_stem(u"aller", u":aller")
    assert verb_stem == u""
    # The infinitive ending must match the template ending
    with pytest.raises(ConjugatorError):
        verb_stem = inf._get_verb_stem(u"vendre", u"man:ger")
