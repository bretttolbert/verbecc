# -*- coding: utf-8 -*-

import pytest
from lxml import etree
from mock import patch
from verbecc.conjugator import (
    Conjugator,
    get_verb_stem,
    ConjugatorError,
    InvalidMoodError)
from verbecc.tense_template import TenseTemplate
from verbecc.string_utils import prepend_with_que

conj = Conjugator()

test_verbs = [
    (u"manger"), 
    (u"venir"), 
    (u"être"), 
    (u"aller"), 
    (u"pouvoir"), 
    (u"finir"),
    (u"pleuvoir")
]

@pytest.mark.parametrize("infinitive", test_verbs)
def test_conjugator_conjugate(infinitive):
    for infinitive in test_verbs:
        output = conj.conjugate(infinitive)
        assert output

def test_conjugator_conjugate_specific_tense():
    verb_stem = u"man"
    tense_elem = etree.fromstring(
        u"""<present>
        <p><i>ge</i></p>
        <p><i>ges</i></p>
        <p><i>ge</i></p>
        <p><i>geons</i></p>
        <p><i>gez</i></p>
        <p><i>gent</i></p>
        </present>""")
    tense_name = 'present'
    tense = TenseTemplate(tense_name, tense_elem)
    out = conj._conjugate_specific_tense(verb_stem, 'indicative', tense)
    assert len(out) == 6
    assert out == [u"je mange", u"tu manges", u"il mange", u"nous mangeons", u"vous mangez", u"ils mangent"]

def test_conjugator_conjugate_passe_compose_with_avoir():
    assert conj.conjugate_passe_compose('manger') == [
    "j'ai mangé",
    "tu as mangé",
    "il a mangé",
    "nous avons mangé",
    "vous avez mangé",
    "ils ont mangé"
    ]

def test_conjugator_conjugate_passe_compose_with_etre():
    assert conj.conjugate_passe_compose('aller') == [
    "je suis allé",
    "tu es allé",
    "il est allé",
    "nous sommes allés",
    "vous êtes allés",
    "ils sont allés"
    ]

def test_conjugator_conjugate_subjunctive_past_with_avoir():
    assert conj.conjugate_subjunctive_past('manger') == [
    "que j'aie mangé",
    "que tu aies mangé",
    "qu'il ait mangé",
    "que nous ayons mangé",
    "que vous ayez mangé",
    "qu'ils aient mangé"
    ]

def test_conjugator_conjugate_subjunctive_past_with_etre():
    assert conj.conjugate_subjunctive_past('aller') == [
    "que je sois allé",
    "que tu sois allé",
    "qu'il soit allé",
    "que nous soyons allés",
    "que vous soyez allés",
    "qu'ils soient allés"
    ]

def test_conjugator_conjugate_conditional_past_with_avoir():
    assert conj.conjugate_conditional_past('manger') == [
    "j'aurais mangé",
    "tu aurais mangé",
    "il aurait mangé",
    "nous aurions mangé",
    "vous auriez mangé",
    "ils auraient mangé"
    ]

def test_conjugator_conjugate_conditional_past_with_etre():
    assert conj.conjugate_conditional_past('aller') == [
    "je serais allé",
    "tu serais allé",
    "il serait allé",
    "nous serions allés",
    "vous seriez allés",
    "ils seraient allés"
    ]

def test_conjugator_conjugate_pluperfect_with_avoir():
    assert conj.conjugate_pluperfect('manger') == [
    "j'avais mangé",
    "tu avais mangé",
    "il avait mangé",
    "nous avions mangé",
    "vous aviez mangé",
    "ils avaient mangé"
    ]

def test_conjugator_conjugate_pluperfect_with_etre():
    assert conj.conjugate_pluperfect('aller') == [
    "j'étais allé",
    "tu étais allé",
    "il était allé",
    "nous étions allés",
    "vous étiez allés",
    "ils étaient allés"
    ]

def test_conjugator_conjugate_subjunctive_pluperfect_with_avoir():
    assert conj.conjugate_subjunctive_pluperfect('manger') == [
    "que j'eusse mangé",
    "que tu eusses mangé",
    "qu'il eût mangé",
    "que nous eussions mangé",
    "que vous eussiez mangé",
    "qu'ils eussent mangé"
    ]

def test_conjugator_conjugate_subjunctive_pluperfect_with_etre():
    assert conj.conjugate_subjunctive_pluperfect('aller') == [
    "que je fusse allé",
    "que tu fusses allé",
    "qu'il fût allé",
    "que nous fussions allés",
    "que vous fussiez allés",
    "qu'ils fussent allés"
    ]

def test_conjugator_conjugate_future_perfect_with_avoir():
    assert conj.conjugate_future_perfect('manger') == [
    "j'aurai mangé",
    "tu auras mangé",
    "il aura mangé",
    "nous aurons mangé",
    "vous aurez mangé",
    "ils auront mangé"
    ]

def test_conjugator_conjugate_future_perfect_with_etre():
    assert conj.conjugate_future_perfect('aller') == [
    "je serai allé",
    "tu seras allé",
    "il sera allé",
    "nous serons allés",
    "vous serez allés",
    "ils seront allés"
    ]

def test_conjugator_conjugate_anterior_past_with_avoir():
    assert conj.conjugate_anterior_past('manger') == [
    "j'eus mangé",
    "tu eus mangé",
    "il eut mangé",
    "nous eûmes mangé",
    "vous eûtes mangé",
    "ils eurent mangé"
    ]

def test_conjugator_conjugate_anterior_past_with_etre():
    assert conj.conjugate_anterior_past('aller') == [
    "je fus allé",
    "tu fus allé",
    "il fut allé",
    "nous fûmes allés",
    "vous fûtes allés",
    "ils furent allés"
    ]

def test_conjugator_conjugate_imperative_past_with_avoir():
    assert conj.conjugate_imperative_past('manger') == [
    "aie mangé",
    "ayons mangé",
    "ayez mangé"
    ]

def test_conjugator_conjugate_imperative_past_with_etre():
    assert conj.conjugate_imperative_past('aller') == [
    "sois allé",
    "soyons allés",
    "soyez allés"
    ]

@patch('verbecc.person_ending.PersonEnding')
def test_conjugator_conjugate_specific_tense_pronoun(mock_person):
    verb_stem = u"man"
    pronoun = u"je"
    ending = u"ge"
    conjugation = conj._conjugate_specific_tense_pronoun(verb_stem, ending, pronoun)
    assert conjugation == u"je mange"

def test_conjugator_prepend_with_que():
    assert prepend_with_que("tu manges") == "que tu manges"
    assert prepend_with_que("il mange") == "qu'il mange"
    assert prepend_with_que("elles mangent") == "qu'elles mangent"

def test_conjugator_get_verb_stem():
    verb_stem = get_verb_stem(u"manger", u"man:ger")
    assert verb_stem == u"man"
    verb_stem = get_verb_stem(u"téléphoner", u"aim:er")
    assert verb_stem == u"téléphon"
    verb_stem = get_verb_stem(u"vendre", u"ten:dre")
    assert verb_stem == u"ven"
    # In the case of irregular verbs, the verb stem is empty string
    verb_stem = get_verb_stem(u"aller", u":aller")
    assert verb_stem == u""
    # The infinitive ending must match the template ending
    with pytest.raises(ConjugatorError):
        verb_stem = get_verb_stem(u"vendre", u"man:ger")

def test_conjugator_impersonal_verbs():
    assert conj.impersonal_verbs == [
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
        "sourdre"]

test_conjugator_verb_can_be_reflexive_data = [
    ("être", False),
    ("lever", True),
    ("pleuvoir", False),
    ("manger", True)
]
@pytest.mark.parametrize("infinitive,expected_result", 
                         test_conjugator_verb_can_be_reflexive_data)
def test_conjugator_verb_can_be_reflexive(infinitive, expected_result):
    assert conj.verb_can_be_reflexive(infinitive) == expected_result
