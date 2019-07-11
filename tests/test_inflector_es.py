# -*- coding: utf-8 -*-

import pytest
from lxml import etree

from verbecc import inflector_es
from verbecc.tense_template import TenseTemplate

inf = inflector_es.InflectorEs()

test_es_conjugate_mood_tense_data = [
    ('abañar', 'Indicativo', 'Indicativo-presente', 
        ['yo abaño', 'tú abañas', 'él abaña', 'nosotros abañamos', 'vosotros abañáis', 'ellos abañan']),
    ('estar', 'Indicativo', 'Indicativo-presente', 
        ['yo estoy', 'tú estás', 'él está', 'nosotros estamos', 'vosotros estáis', 'ellos están']),
    ('ser', 'Indicativo', 'Indicativo-presente', 
        ['yo soy', 'tú eres', 'él es', 'nosotros somos', 'vosotros sois', 'ellos son']),
    ('tener', 'Indicativo', 'Indicativo-presente', 
        ['yo tengo', 'tú tienes', 'él tiene', 'nosotros tenemos', 'vosotros tenéis', 'ellos tienen']),
    ('haber', 'Indicativo', 'Indicativo-presente', 
        ['yo he', 'tú has', 'él hay', 'nosotros hemos', 'vosotros habéis', 'ellos han']),
    ('haber', 'Indicativo', 'Indicativo-pretérito-imperfecto', 
        ['yo había', 'tú habías', 'él había', 'nosotros habíamos', 'vosotros habíais', 'ellos habían']),
    ('haber', 'Indicativo', 'Indicativo-pretérito-perfecto-simple',
        ['yo hube', 'tú hubiste', 'él hubo', 'nosotros hubimos', 'vosotros hubisteis', 'ellos hubieron']),
    ('haber', 'Indicativo', 'Indicativo-futuro',
        ['yo habré', 'tú habrás', 'él habrá', 'nosotros habremos', 'vosotros habréis', 'ellos habrán']),
    ('haber', 'Condicional', 'Condicional-condicional',
        ['yo habría', 'tú habrías', 'él habría', 'nosotros habríamos', 'vosotros habríais', 'ellos habrían']),
    ('hacer', 'Indicativo', 'Indicativo-presente', 
        ['yo hago', 'tú haces', 'él hace', 'nosotros hacemos', 'vosotros hacéis', 'ellos hacen']),
    ('ir', 'Indicativo', 'Indicativo-presente',
        ['yo voy', 'tú vas', 'él va', 'nosotros vamos', 'vosotros vais', 'ellos van']),
    ('comer', 'Indicativo', 'Indicativo-presente', 
        ['yo como', 'tú comes', 'él come', 'nosotros comemos', 'vosotros coméis', 'ellos comen']),
    ('comer', 'Indicativo', 'Indicativo-pretérito-perfecto-simple',
        ['yo comí', 'tú comiste', 'él comió', 'nosotros comimos', 'vosotros comisteis', 'ellos comieron']),
    ('comer', 'Indicativo', 'Indicativo-pretérito-imperfecto',
        ['yo comía', 'tú comías', 'él comía', 'nosotros comíamos', 'vosotros comíais', 'ellos comían']),
    ('comer', 'Condicional', 'Condicional-condicional',
        ['yo comería', 'tú comerías', 'él comería', 'nosotros comeríamos', 'vosotros comeríais', 'ellos comerían']),
    ('comer', 'Indicativo', 'Indicativo-pretérito-perfecto-compuesto',
        ['yo he comido', 'tú has comido', 'él ha comido', 'nosotros hemos comido', 'vosotros habéis comido', 'ellos han comido']),
    ('comer', 'Indicativo', 'Indicativo-pretérito-pluscuamperfecto',
        ['yo había comido', 'tú habías comido', 'él había comido', 'nosotros habíamos comido', 'vosotros habíais comido', 'ellos habían comido']),
    ('comer', 'Indicativo', 'Indicativo-pretérito-anterior',
        ['yo hube comido', 'tú hubiste comido', 'él hubo comido', 'nosotros hubimos comido', 'vosotros hubisteis comido', 'ellos hubieron comido']),
    ('comer', 'Indicativo', 'Indicativo-futuro-perfecto',
        ['yo habré comido', 'tú habrás comido', 'él habrá comido', 'nosotros habremos comido', 'vosotros habréis comido', 'ellos habrán comido']),
    ('comer', 'Condicional', 'Condicional-perfecto',
        ['yo habría comido', 'tú habrías comido', 'él habría comido', 'nosotros habríamos comido', 'vosotros habríais comido', 'ellos habrían comido'])
]

"""

"""

@pytest.mark.parametrize("infinitive,mood,tense,expected_result",
                         test_es_conjugate_mood_tense_data)
def test_inflector_es_conjugate_mood_tense(infinitive, mood, tense, expected_result):
    assert inf.conjugate_mood_tense(infinitive, mood, tense) == expected_result

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
