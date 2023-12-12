# -*- coding: utf-8 -*-

import pytest
from lxml import etree

from verbecc import Conjugator
from verbecc.tense_template import TenseTemplate

cg = Conjugator(lang='ca')

"""
    ('estar', 'indicatiu', 'present', 
        ['jo estic', 'tu estás', 'ell está', 'nosaltres estem', 'vosaltres esteu', 'ells estan']),
    ('tenir', 'indicatiu', 'present', 
        ['jo tinc', 'tu tens', 'ell té', 'nosaltres tenim', 'vosaltres teniu', 'ells tenen']),
    ('haver', 'indicatiu', 'present', 
        ['jo he', 'tu has', 'ell ha', 'nosaltres havem', 'vosaltres haveu', 'ells han']),
    ('haver', 'indicatiu', 'imperfet', 
        ['jo havia', 'tu havies', 'ell havia', 'nosaltres havíem', 'vosaltres habíeu', 'ells habien']),
    ('haver', 'indicatiu', 'pretèrit',
        ['jo haguí', 'tu hagueres', 'ell hagué', 'nosaltres haguérem', 'vosaltres hubisteis', 'ells hubieron']),
    ('haver', 'indicatiu', 'futuro',
        ['jo hauré', 'tu hauràs', 'ell haurà', 'nosaltres haurem', 'vosaltres haureu', 'ells hauran']),
    ('haver', 'condicional', 'present',
        ['jo hauria', 'tu hauries', 'ell habria', 'nosaltres hauríem', 'vosaltres hauríeu', 'ells haurien']),
    ('haver', 'subjuntiu', 'present',
        ['jo hagi', 'tu hagis', 'ell hagi', 'nosaltres hàgim', 'vosaltres hàgiu', 'ells hagin']),
"""

test_ca_conjugate_mood_tense_data = [
    ('ser', 'indicatiu', 'present', 
        ['jo sóc', 'tu ets', 'ell és', 'nosaltres som', 'vosaltres sou', 'ells són']),
    ('ser', 'indicatiu', 'imperfet',
        ['jo era', 'tu eres', 'ell era', 'nosaltres érem', 'vosaltres éreu', 'ells eren']),
    ('ser', 'indicatiu', 'pretèrit',
        ['jo fui', 'tu fores', 'ell fou', 'nosaltres fórem', 'vosaltres fóreu', 'ells foren']),
    ('ser', 'indicatiu', 'futur',
        ['jo seré', 'tu seràs', 'ell serà', 'nosaltres serem', 'vosaltres sereu', 'ells seran']),
    ('ser', 'subjuntiu', 'present',
        ['jo sigui', 'tu siguis', 'ell sigui', 'nosaltres siguem', 'vosaltres sigueu', 'ells siguin']),
    ('ser', 'subjuntiu', 'imperfet',
        ['jo fos', 'tu fossis', 'ell fos', 'nosaltres fóssim', 'vosaltres fóssiu', 'ells fossin']),
    ('ser', 'condicional', 'present',
        ['jo seria', 'tu series', 'ell seria', 'nosaltres seríem', 'vosaltres seríeu', 'ells serien']),
    ('ser', 'imperatiu', 'imperatiu-present',
        ['sigues', 'sigui', 'siguem', 'sigueu', 'siguin']),
    ('parlar', 'indicatiu', 'present',
        ['jo parlo', 'tu parles', 'ell parla', 'nosaltres parlem', 'vosaltres parleu', 'ells parlen']),
    ('parlar', 'indicatiu', 'imperfet',
        ['jo parlava', 'tu parlaves', 'ell parlava', 'nosaltres parlàvem', 'vosaltres parlàveu', 'ells parlaven']),
    ('parlar', 'indicatiu', 'pretèrit',
        ['jo parlí', 'tu parlares', 'ell parlà', 'nosaltres parlàrem', 'vosaltres parlàreu', 'ells parlaren']),
    ('parlar', 'indicatiu', 'futur',
        ['jo parlaré', 'tu parlaràs', 'ell parlarà', 'nosaltres parlarem', 'vosaltres parlareu', 'ells parlaran'])
]

@pytest.mark.parametrize("infinitive,mood,tense,expected_result",
                         test_ca_conjugate_mood_tense_data)
def test_inflector_ca_conjugate_mood_tense(infinitive, mood, tense, expected_result):
    assert cg.conjugate_mood_tense(infinitive, mood, tense) == expected_result

def test_inflector_ca_get_conj_obs():
    co = cg._inflector._get_conj_obs('parlar')
    assert co.verb.infinitive == "parlar"
    assert co.verb_stem == "parl"

def test_inflector_ca_get_verb_stem():
    verb_stem = cg._inflector._get_verb_stem(u"parlar", u"cant:ar")
    assert verb_stem == u"parl"

def test_inflector_ca_conjugate_simple_mood_tense():
    verb_stem = u"parl"
    tense_elem = etree.fromstring(
        u"""<present>
            <p><i>o</i></p>
            <p><i>es</i></p>
            <p><i>a</i></p>
            <p><i>em</i></p>
            <p><i>eu</i></p>
            <p><i>en</i></p>
        </present>""")
    tense_name = 'present'
    tense_template = TenseTemplate(tense_elem)
    out = cg._inflector._conjugate_simple_mood_tense(verb_stem, 'indicatiu', tense_template)
    assert len(out) == 6
    assert out == ['jo parlo', 'tu parles', 'ell parla', 'nosaltres parlem', 'vosaltres parleu', 'ells parlen']


test_inflector_ca_get_default_pronoun_data = [
    ('1s', 'm', False, 'jo'),
    ('1s', 'm', True, 'jo me'),
    ('2s', 'm', False, 'tu'),
    ('2s', 'm', True, 'tu te'),
    ('3s', 'm', False, 'ell'),
    ('3s', 'm', True, 'ell se'),
    ('3s', 'f', False, 'ella'),
    ('3s', 'f', True, 'ella se'),
    ('1p', 'm', False, 'nosaltres'),
    ('1p', 'm', True, 'nosaltres nos'),
    ('2p', 'm', False, 'vosaltres'),
    ('2p', 'm', True, 'vosaltres os'),
    ('3p', 'm', False, 'ells'),
    ('3p', 'm', True, 'ells se'),
    ('3p', 'f', False, 'elles'),
    ('3p', 'f', True, 'elles se')
]

@pytest.mark.parametrize("person,gender,is_reflexive,expected_result",
                         test_inflector_ca_get_default_pronoun_data)
def test_inflector_ca_get_default_pronoun(person, gender, is_reflexive, expected_result):
    assert cg._inflector._get_default_pronoun(person, gender, is_reflexive=is_reflexive) == expected_result
