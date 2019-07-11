# -*- coding: utf-8 -*-

import pytest
from lxml import etree

from verbecc import inflector_es
from verbecc.tense_template import TenseTemplate

inf = inflector_es.InflectorEs()

# presente = Subjunctive Present (yo haya)
# pretérito-perfecto = Subjunctive Perfect (yo haya habido)
# pretérito-imperfecto-1 = Subjunctive Past 1 (yo hubiera)
# pretérito-imperfecto-2 = Subjunctive Past 2 (yo hubiese)
# pretérito-pluscuamperfecto-1 = Subjunctive Pluperfect 1 (yo hubiera habido)
# pretérito-pluscuamperfecto-2 = Subjunctive Pluperfect 2 (yo hubiese habido)
# futuro = Subjunctive Future (yo hubiere)
# futuro-perfecto = Subjunctive Future Perfect (yo hubiere habido)

test_es_conjugate_mood_tense_data = [
    ('abañar', 'indicativo', 'presente', 
        ['yo abaño', 'tú abañas', 'él abaña', 'nosotros abañamos', 'vosotros abañáis', 'ellos abañan']),
    ('estar', 'indicativo', 'presente', 
        ['yo estoy', 'tú estás', 'él está', 'nosotros estamos', 'vosotros estáis', 'ellos están']),
    ('ser', 'indicativo', 'presente', 
        ['yo soy', 'tú eres', 'él es', 'nosotros somos', 'vosotros sois', 'ellos son']),
    ('tener', 'indicativo', 'presente', 
        ['yo tengo', 'tú tienes', 'él tiene', 'nosotros tenemos', 'vosotros tenéis', 'ellos tienen']),
    ('haber', 'indicativo', 'presente', 
        ['yo he', 'tú has', 'él hay', 'nosotros hemos', 'vosotros habéis', 'ellos han']),
    ('haber', 'indicativo', 'pretérito-imperfecto', 
        ['yo había', 'tú habías', 'él había', 'nosotros habíamos', 'vosotros habíais', 'ellos habían']),
    ('haber', 'indicativo', 'pretérito-perfecto-simple',
        ['yo hube', 'tú hubiste', 'él hubo', 'nosotros hubimos', 'vosotros hubisteis', 'ellos hubieron']),
    ('haber', 'indicativo', 'futuro',
        ['yo habré', 'tú habrás', 'él habrá', 'nosotros habremos', 'vosotros habréis', 'ellos habrán']),
    ('haber', 'condicional', 'condicional-present',
        ['yo habría', 'tú habrías', 'él habría', 'nosotros habríamos', 'vosotros habríais', 'ellos habrían']),
    ('haber', 'subjuntivo', 'presente',
        ['yo haya', 'tú hayas', 'él haya', 'nosotros hayamos', 'vosotros hayáis', 'ellos hayan']),
    ('haber', 'subjuntivo', 'pretérito-imperfecto-1',
        ['yo hubiera', 'tú hubieras', 'él hubiera', 'nosotros hubiéramos', 'vosotros hubierais', 'ellos hubieran']),
    ('haber', 'subjuntivo', 'pretérito-imperfecto-2',
        ['yo hubiese', 'tú hubieses', 'él hubiese', 'nosotros hubiésemos', 'vosotros hubieseis', 'ellos hubiesen']),
    ('haber', 'subjuntivo', 'futuro',
        ['yo hubiere', 'tú hubieres', 'él hubiere', 'nosotros hubiéremos', 'vosotros hubiereis', 'ellos hubieren']),
    ('hacer', 'indicativo', 'presente', 
        ['yo hago', 'tú haces', 'él hace', 'nosotros hacemos', 'vosotros hacéis', 'ellos hacen']),
    ('ir', 'indicativo', 'presente',
        ['yo voy', 'tú vas', 'él va', 'nosotros vamos', 'vosotros vais', 'ellos van']),
    ('comer', 'indicativo', 'presente', 
        ['yo como', 'tú comes', 'él come', 'nosotros comemos', 'vosotros coméis', 'ellos comen']),
    ('comer', 'indicativo', 'pretérito-perfecto-simple',
        ['yo comí', 'tú comiste', 'él comió', 'nosotros comimos', 'vosotros comisteis', 'ellos comieron']),
    ('comer', 'indicativo', 'pretérito-imperfecto',
        ['yo comía', 'tú comías', 'él comía', 'nosotros comíamos', 'vosotros comíais', 'ellos comían']),
    ('comer', 'condicional', 'condicional-present',
        ['yo comería', 'tú comerías', 'él comería', 'nosotros comeríamos', 'vosotros comeríais', 'ellos comerían']),
    ('comer', 'indicativo', 'indicativo-pretérito-perfecto-compuesto',
        ['yo he comido', 'tú has comido', 'él ha comido', 'nosotros hemos comido', 'vosotros habéis comido', 'ellos han comido']),
    ('comer', 'indicativo', 'indicativo-pretérito-pluscuamperfecto',
        ['yo había comido', 'tú habías comido', 'él había comido', 'nosotros habíamos comido', 'vosotros habíais comido', 'ellos habían comido']),
    ('comer', 'indicativo', 'indicativo-pretérito-anterior',
        ['yo hube comido', 'tú hubiste comido', 'él hubo comido', 'nosotros hubimos comido', 'vosotros hubisteis comido', 'ellos hubieron comido']),
    ('comer', 'indicativo', 'futuro-perfecto',
        ['yo habré comido', 'tú habrás comido', 'él habrá comido', 'nosotros habremos comido', 'vosotros habréis comido', 'ellos habrán comido']),
    ('comer', 'condicional', 'condicional-perfecto',
        ['yo habría comido', 'tú habrías comido', 'él habría comido', 'nosotros habríamos comido', 'vosotros habríais comido', 'ellos habrían comido']),
    ('comer', 'subjuntivo', 'pretérito-perfecto',
        ['yo haya comido', 'tú hayas comido', 'él haya comido', 'nosotros hayamos comido', 'vosotros hayáis comido', 'ellos hayan comido']),
    ('comer', 'subjuntivo', 'pretérito-pluscuamperfecto-1',
        ['yo hubiera comido', 'tú hubieras comido', 'él hubiera comido', 'nosotros hubiéramos comido', 'vosotros hubierais comido', 'ellos hubieran comido']),
    ('comer', 'subjuntivo', 'pretérito-pluscuamperfecto-2',
        ['yo hubiese comido', 'tú hubieses comido', 'él hubiese comido', 'nosotros hubiésemos comido', 'vosotros hubieseis comido', 'ellos hubiesen comido']),
    ('comer', 'subjuntivo', 'futuro-perfecto',
        ['yo hubiere comido', 'tú hubieres comido', 'él hubiere comido', 'nosotros hubiéremos comido', 'vosotros hubiereis comido', 'ellos hubieren comido'])
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
        u"""<presente>
            <p><i>o</i></p>
            <p><i>as</i></p>
            <p><i>a</i></p>
            <p><i>amos</i></p>
            <p><i>áis</i></p>
            <p><i>an</i></p>
        </presente>""")
    tense_name = 'présent'
    tense_template = TenseTemplate(tense_elem)
    out = inf._conjugate_simple_mood_tense(verb_stem, 'indicativo', tense_template)
    assert len(out) == 6
    assert out == ['yo abaño', 'tú abañas', 'él abaña', 'nosotros abañamos', 'vosotros abañáis', 'ellos abañan']
