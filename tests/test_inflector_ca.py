# -*- coding: utf-8 -*-

import pytest
from lxml import etree

from verbecc import Conjugator
from verbecc.tense_template import TenseTemplate

cg = Conjugator(lang='ca')

@pytest.mark.skip("known failure")
def test_all_verbs_have_templates():
    """Have not finished adding templates for all verbs, so this should fail"""
    verbs = cg.get_verbs()
    template_names = cg.get_template_names()
    missing_templates = set()
    for verb in verbs:
        if verb.template not in template_names:
            missing_templates.add(verb.template)
    assert len(missing_templates) == 0

def test_find_verb_by_infinitive():
    v = cg.find_verb_by_infinitive('abandonar')
    assert v.infinitive == 'abandonar'
    assert v.template == 'cant:ar'

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
        ['jo parlaré', 'tu parlaràs', 'ell parlarà', 'nosaltres parlarem', 'vosaltres parlareu', 'ells parlaran']),
    ('parlar', 'subjuntiu', 'present',
        ['jo parli', 'tu parlis', 'ell parli', 'nosaltres parlem', 'vosaltres parleu', 'ells parlin']),
    ('parlar', 'subjuntiu', 'imperfet',
        ['jo parlés', 'tu parlessis', 'ell parlés', 'nosaltres parléssim', 'vosaltres parléssiu', 'ells parlessin']),
    ('parlar', 'condicional', 'present',
        ['jo parlaria', 'tu parlaries', 'ell parlaria', 'nosaltres parlaríem', 'vosaltres parlaríeu', 'ells parlarien']),
    ('estar', 'indicatiu', 'present',
        ['jo estic', 'tu estàs', 'ell està', 'nosaltres estem', 'vosaltres esteu', 'ells estan']),
    ('estar', 'indicatiu', 'imperfet',
        ['jo estava', 'tu estaves', 'ell estava', 'nosaltres estàvem', 'vosaltres estàveu', 'ells estaven']),
    ('estar', 'indicatiu', 'pretèrit',
        ['jo estiguí', 'tu estigueres', 'ell estigué', 'nosaltres estiguérem', 'vosaltres estiguéreu', 'ells estigueren']),
    ('estar', 'indicatiu', 'futur',
        ['jo estaré', 'tu estaràs', 'ell estarà', 'nosaltres estarem', 'vosaltres estareu', 'ells estaran']),
    ('estar', 'subjuntiu', 'present',
        ['jo estigui', 'tu estiguis', 'ell estigui', 'nosaltres estiguem', 'vosaltres estigueu', 'ells estiguin']),
    ('estar', 'subjuntiu', 'imperfet',
        ['jo estigués', 'tu estiguessis', 'ell estigués', 'nosaltres estiguéssim', 'vosaltres estiguéssiu', 'ells estiguessin']),
    ('estar', 'condicional', 'present',
        ['jo estaria', 'tu estaries', 'ell estaria', 'nosaltres estaríem', 'vosaltres estaríeu', 'ells estarien']),
    ('haver', 'indicatiu', 'present', 
        ['jo he', 'tu has', 'ell ha', 'nosaltres havem', 'vosaltres haveu', 'ells han']),
    ('haver', 'indicatiu', 'imperfet', 
        ['jo havia', 'tu havies', 'ell havia', 'nosaltres havíem', 'vosaltres havíeu', 'ells havien']),
    ('haver', 'indicatiu', 'pretèrit',
        ['jo haguí', 'tu hagueres', 'ell hagué', 'nosaltres haguérem', 'vosaltres haguéreu', 'ells hagueren']),
    ('haver', 'indicatiu', 'futur',
        ['jo hauré', 'tu hauràs', 'ell haurà', 'nosaltres haurem', 'vosaltres haureu', 'ells hauran']),
    ('haver', 'condicional', 'present',
        ['jo hauria', 'tu hauries', 'ell hauria', 'nosaltres hauríem', 'vosaltres hauríeu', 'ells haurien']),
    ('haver', 'subjuntiu', 'present',
        ['jo hagi', 'tu hagis', 'ell hagi', 'nosaltres hàgim', 'vosaltres hàgiu', 'ells hagin']),
    ('tenir', 'indicatiu', 'present', 
        ['jo tinc', 'tu tens', 'ell té', 'nosaltres tenim', 'vosaltres teniu', 'ells tenen']),
    ('fer', 'indicatiu', 'present', 
        ['jo faig', 'tu fas', 'ell fa', 'nosaltres fem', 'vosaltres feu', 'ells fan']),
    ('fer', 'indicatiu', 'imperfet', 
        ['jo feia', 'tu feies', 'ell feia', 'nosaltres fèiem', 'vosaltres fèieu', 'ells feien']),
    ('servir', 'indicatiu', 'present', 
        ['jo serveixo', 'tu serveixes', 'ell serveix', 'nosaltres servim', 'vosaltres serviu', 'ells serveixen']),
    ('veure', 'indicatiu', 'present', 
        ['jo veig', 'tu veus', 'ell veu', 'nosaltres veiem', 'vosaltres veieu', 'ells veuen']),
    ('abandonar', 'indicatiu', 'present', 
        ['jo abandono', 'tu abandones', 'ell abandona', 'nosaltres abandonem', 'vosaltres abandoneu', 'ells abandonen']),
    ('rebre', 'indicatiu', 'present', 
        ['jo rebo', 'tu reps', 'ell rep', 'nosaltres rebem', 'vosaltres rebeu', 'ells reben']),
    ('cabre', 'indicatiu', 'present', 
        ['jo cabo', 'tu caps', 'ell cap', 'nosaltres cabem', 'vosaltres cabeu', 'ells caben']),
    ('començar', 'indicatiu', 'present',
        ['jo començo',  'tu comences', 'ell comença', 'nosaltres comencem', 'vosaltres comenceu', 'ells comencen']),
    ('enaiguar', 'indicatiu', 'present',
        ['jo enaiguo', 'tu enaigües', 'ell enaigua', 'nosaltres enaigüem', 'vosaltres enaigüeu', 'ells enaigüen'])
]

@pytest.mark.parametrize("infinitive,mood,tense,expected_result",
                         test_ca_conjugate_mood_tense_data)
def test_inflector_ca_conjugate_mood_tense(infinitive, mood, tense, expected_result):
    assert cg.conjugate_mood_tense(infinitive, mood, tense) == expected_result

def test_inflector_ca_get_conj_obs():
    co = cg._inflector._get_conj_obs('parlar')
    assert co.verb.infinitive == "parlar"
    assert co.verb_stem == "parl"
    assert co.template.name == "cant:ar"

def test_inflector_ca_get_conj_obs_2():
    co = cg._inflector._get_conj_obs('abandonar')
    assert co.verb.infinitive == "abandonar"
    assert co.verb_stem == "abandon"
    assert co.template.name == "cant:ar"

def test_inflector_ca_get_verb_stem():
    verb_stem = cg._inflector._get_verb_stem(u"parlar", u"cant:ar")
    assert verb_stem == u"parl"

def test_inflector_ca_get_verb_stem_2():
    verb_stem = cg._inflector._get_verb_stem(u"abandonar", u"cant:ar")
    assert verb_stem == u"abandon"

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
