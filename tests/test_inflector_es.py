# -*- coding: utf-8 -*-

import pytest
from lxml import etree

from verbecc import inflector_es
from verbecc.tense_template import TenseTemplate

inf = inflector_es.InflectorEs()

def test_inflector_es_conjugate():
    expected = ['yo abaño', 'tú abañas', 'él abaña', 'nosotros abañamos', 'vosotros abañáis', 'ellos abañan']
    assert inf.conjugate_mood_tense('abañar', 'Indicativo', 'Indicativo-presente') == expected

def test_inflector_es_get_conj_obs():
    co = inf._get_conj_obs('abañar')
    assert co.verb.infinitive == "abañar"
    assert co.verb_stem == "abañ"

def test_inflector_es_get_verb_stem():
    verb_stem = inf._get_verb_stem(u"abañar", u"cort:ar")
    assert verb_stem == u"abañ", repr(conj_obs)

def test_inflector_es_conjugate_simple_mood_tense():
    verb_stem = u"abañ"
    tense_elem = etree.fromstring(
        u"""<Indicativo-presente>
            <p><i>o</i></p>
            <p><i>as</i></p>
            <p><i>a</i></p>
            <p><i>amos</i></p>
            <p><i>áis</i></p>
            <p><i>an</i></p>
        </Indicativo-presente>""")
    tense_name = 'présent'
    tense_template = TenseTemplate(tense_elem)
    out = inf._conjugate_simple_mood_tense(verb_stem, 'Indicativo', tense_template)
    assert len(out) == 6
    assert out == ['yo abaño', 'tú abañas', 'él abaña', 'nosotros abañamos', 'vosotros abañáis', 'ellos abañan']
