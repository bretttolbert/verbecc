# -*- coding: utf-8 -*-

import pytest
from lxml import etree

from verbecc import Conjugator
from verbecc.tense_template import TenseTemplate

cg = Conjugator(lang="es")


def test_all_verbs_have_templates():
    verbs = cg.get_verbs()
    template_names = cg.get_template_names()
    missing_templates = set()
    for verb in verbs:
        if verb.template not in template_names:
            missing_templates.add(verb.template)
    assert len(missing_templates) == 0


# presente = Subjunctive Present (yo haya)
# pretérito-perfecto = Subjunctive Perfect (yo haya habido)
# pretérito-imperfecto-1 = Subjunctive Past 1 (yo hubiera)
# pretérito-imperfecto-2 = Subjunctive Past 2 (yo hubiese)
# pretérito-pluscuamperfecto-1 = Subjunctive Pluperfect 1 (yo hubiera habido)
# pretérito-pluscuamperfecto-2 = Subjunctive Pluperfect 2 (yo hubiese habido)
# futuro = Subjunctive Future (yo hubiere)
# futuro-perfecto = Subjunctive Future Perfect (yo hubiere habido)

test_es_conjugate_mood_tense_data = [
    (
        "abañar",
        "indicativo",
        "presente",
        [
            "yo abaño",
            "tú abañas",
            "él abaña",
            "nosotros abañamos",
            "vosotros abañáis",
            "ellos abañan",
        ],
    ),
    (
        "estar",
        "indicativo",
        "presente",
        [
            "yo estoy",
            "tú estás",
            "él está",
            "nosotros estamos",
            "vosotros estáis",
            "ellos están",
        ],
    ),
    (
        "ser",
        "indicativo",
        "presente",
        ["yo soy", "tú eres", "él es", "nosotros somos", "vosotros sois", "ellos son"],
    ),
    (
        "tener",
        "indicativo",
        "presente",
        [
            "yo tengo",
            "tú tienes",
            "él tiene",
            "nosotros tenemos",
            "vosotros tenéis",
            "ellos tienen",
        ],
    ),
    (
        "haber",
        "indicativo",
        "presente",
        ["yo he", "tú has", "él hay", "nosotros hemos", "vosotros habéis", "ellos han"],
    ),
    (
        "haber",
        "indicativo",
        "pretérito-imperfecto",
        [
            "yo había",
            "tú habías",
            "él había",
            "nosotros habíamos",
            "vosotros habíais",
            "ellos habían",
        ],
    ),
    (
        "haber",
        "indicativo",
        "pretérito-perfecto-simple",
        [
            "yo hube",
            "tú hubiste",
            "él hubo",
            "nosotros hubimos",
            "vosotros hubisteis",
            "ellos hubieron",
        ],
    ),
    (
        "haber",
        "indicativo",
        "futuro",
        [
            "yo habré",
            "tú habrás",
            "él habrá",
            "nosotros habremos",
            "vosotros habréis",
            "ellos habrán",
        ],
    ),
    (
        "haber",
        "condicional",
        "presente",
        [
            "yo habría",
            "tú habrías",
            "él habría",
            "nosotros habríamos",
            "vosotros habríais",
            "ellos habrían",
        ],
    ),
    (
        "haber",
        "subjuntivo",
        "presente",
        [
            "yo haya",
            "tú hayas",
            "él haya",
            "nosotros hayamos",
            "vosotros hayáis",
            "ellos hayan",
        ],
    ),
    (
        "haber",
        "subjuntivo",
        "pretérito-imperfecto-1",
        [
            "yo hubiera",
            "tú hubieras",
            "él hubiera",
            "nosotros hubiéramos",
            "vosotros hubierais",
            "ellos hubieran",
        ],
    ),
    (
        "haber",
        "subjuntivo",
        "pretérito-imperfecto-2",
        [
            "yo hubiese",
            "tú hubieses",
            "él hubiese",
            "nosotros hubiésemos",
            "vosotros hubieseis",
            "ellos hubiesen",
        ],
    ),
    (
        "haber",
        "subjuntivo",
        "futuro",
        [
            "yo hubiere",
            "tú hubieres",
            "él hubiere",
            "nosotros hubiéremos",
            "vosotros hubiereis",
            "ellos hubieren",
        ],
    ),
    (
        "hacer",
        "indicativo",
        "presente",
        [
            "yo hago",
            "tú haces",
            "él hace",
            "nosotros hacemos",
            "vosotros hacéis",
            "ellos hacen",
        ],
    ),
    (
        "ir",
        "indicativo",
        "presente",
        ["yo voy", "tú vas", "él va", "nosotros vamos", "vosotros vais", "ellos van"],
    ),
    (
        "comer",
        "indicativo",
        "presente",
        [
            "yo como",
            "tú comes",
            "él come",
            "nosotros comemos",
            "vosotros coméis",
            "ellos comen",
        ],
    ),
    (
        "comer",
        "indicativo",
        "pretérito-perfecto-simple",
        [
            "yo comí",
            "tú comiste",
            "él comió",
            "nosotros comimos",
            "vosotros comisteis",
            "ellos comieron",
        ],
    ),
    (
        "comer",
        "indicativo",
        "pretérito-imperfecto",
        [
            "yo comía",
            "tú comías",
            "él comía",
            "nosotros comíamos",
            "vosotros comíais",
            "ellos comían",
        ],
    ),
    (
        "comer",
        "condicional",
        "presente",
        [
            "yo comería",
            "tú comerías",
            "él comería",
            "nosotros comeríamos",
            "vosotros comeríais",
            "ellos comerían",
        ],
    ),
    (
        "comer",
        "indicativo",
        "pretérito-perfecto-compuesto",
        [
            "yo he comido",
            "tú has comido",
            "él ha comido",
            "nosotros hemos comido",
            "vosotros habéis comido",
            "ellos han comido",
        ],
    ),
    (
        "comer",
        "indicativo",
        "pretérito-pluscuamperfecto",
        [
            "yo había comido",
            "tú habías comido",
            "él había comido",
            "nosotros habíamos comido",
            "vosotros habíais comido",
            "ellos habían comido",
        ],
    ),
    (
        "comer",
        "indicativo",
        "pretérito-anterior",
        [
            "yo hube comido",
            "tú hubiste comido",
            "él hubo comido",
            "nosotros hubimos comido",
            "vosotros hubisteis comido",
            "ellos hubieron comido",
        ],
    ),
    (
        "comer",
        "indicativo",
        "futuro-perfecto",
        [
            "yo habré comido",
            "tú habrás comido",
            "él habrá comido",
            "nosotros habremos comido",
            "vosotros habréis comido",
            "ellos habrán comido",
        ],
    ),
    (
        "comer",
        "condicional",
        "perfecto",
        [
            "yo habría comido",
            "tú habrías comido",
            "él habría comido",
            "nosotros habríamos comido",
            "vosotros habríais comido",
            "ellos habrían comido",
        ],
    ),
    (
        "comer",
        "subjuntivo",
        "pretérito-perfecto",
        [
            "yo haya comido",
            "tú hayas comido",
            "él haya comido",
            "nosotros hayamos comido",
            "vosotros hayáis comido",
            "ellos hayan comido",
        ],
    ),
    (
        "comer",
        "subjuntivo",
        "pretérito-pluscuamperfecto-1",
        [
            "yo hubiera comido",
            "tú hubieras comido",
            "él hubiera comido",
            "nosotros hubiéramos comido",
            "vosotros hubierais comido",
            "ellos hubieran comido",
        ],
    ),
    (
        "comer",
        "subjuntivo",
        "pretérito-pluscuamperfecto-2",
        [
            "yo hubiese comido",
            "tú hubieses comido",
            "él hubiese comido",
            "nosotros hubiésemos comido",
            "vosotros hubieseis comido",
            "ellos hubiesen comido",
        ],
    ),
    (
        "comer",
        "subjuntivo",
        "futuro-perfecto",
        [
            "yo hubiere comido",
            "tú hubieres comido",
            "él hubiere comido",
            "nosotros hubiéremos comido",
            "vosotros hubiereis comido",
            "ellos hubieren comido",
        ],
    ),
    (
        "comer",
        "imperativo",
        "afirmativo",
        ["come", "coma", "comamos", "comed", "coman"],
    ),
    (
        "comer",
        "imperativo",
        "negativo",
        ["no comas", "no coma", "no comamos", "no comáis", "no coman"],
    ),
    (
        "parecer",
        "indicativo",
        "presente",
        [
            "yo parezco",
            "tú pareces",
            "él parece",
            "nosotros parecemos",
            "vosotros parecéis",
            "ellos parecen",
        ],
    ),
    (
        "parecer",
        "indicativo",
        "pretérito-imperfecto",
        [
            "yo parecía",
            "tú parecías",
            "él parecía",
            "nosotros parecíamos",
            "vosotros parecíais",
            "ellos parecían",
        ],
    ),
    (
        "parecer",
        "indicativo",
        "pretérito-perfecto-simple",
        [
            "yo parecí",
            "tú pareciste",
            "él pareció",
            "nosotros parecimos",
            "vosotros parecisteis",
            "ellos parecieron",
        ],
    ),
    (
        "parecer",
        "indicativo",
        "futuro",
        [
            "yo pareceré",
            "tú parecerás",
            "él parecerá",
            "nosotros pareceremos",
            "vosotros pareceréis",
            "ellos parecerán",
        ],
    ),
    (
        "parecer",
        "subjuntivo",
        "presente",
        [
            "yo parezca",
            "tú parezcas",
            "él parezca",
            "nosotros parezcamos",
            "vosotros parezcáis",
            "ellos parezcan",
        ],
    ),
    (
        "parecer",
        "subjuntivo",
        "pretérito-imperfecto-1",
        [
            "yo pareciera",
            "tú parecieras",
            "él pareciera",
            "nosotros pareciéramos",
            "vosotros parecierais",
            "ellos parecieran",
        ],
    ),
    (
        "parecer",
        "subjuntivo",
        "pretérito-imperfecto-2",
        [
            "yo pareciese",
            "tú parecieses",
            "él pareciese",
            "nosotros pareciésemos",
            "vosotros parecieseis",
            "ellos pareciesen",
        ],
    ),
    (
        "parecer",
        "subjuntivo",
        "futuro",
        [
            "yo pareciere",
            "tú parecieres",
            "él pareciere",
            "nosotros pareciéremos",
            "vosotros pareciereis",
            "ellos parecieren",
        ],
    ),
    (
        "parecer",
        "imperativo",
        "afirmativo",
        ["parece", "parezca", "parezcamos", "pareced", "parezcan"],
    ),
    (
        "parecer",
        "imperativo",
        "negativo",
        ["no parezcas", "no parezca", "no parezcamos", "no parezcáis", "no parezcan"],
    ),
    (
        "parecer",
        "condicional",
        "presente",
        [
            "yo parecería",
            "tú parecerías",
            "él parecería",
            "nosotros pareceríamos",
            "vosotros pareceríais",
            "ellos parecerían",
        ],
    ),
    (
        "parecer",
        "indicativo",
        "pretérito-perfecto-compuesto",
        [
            "yo he parecido",
            "tú has parecido",
            "él ha parecido",
            "nosotros hemos parecido",
            "vosotros habéis parecido",
            "ellos han parecido",
        ],
    ),
    (
        "abolir",
        "indicativo",
        "presente",
        [
            "yo abolo",
            "tú aboles",
            "él abole",
            "nosotros abolimos",
            "vosotros abolís",
            "ellos abolen",
        ],
    ),
    (
        "abolir",
        "subjuntivo",
        "futuro",
        [
            "yo aboliere",
            "tú abolieres",
            "él aboliere",
            "nosotros aboliéremos",
            "vosotros aboliereis",
            "ellos abolieren",
        ],
    ),
]


@pytest.mark.parametrize(
    "infinitive,mood,tense,expected_result", test_es_conjugate_mood_tense_data
)
def test_inflector_es_conjugate_mood_tense(infinitive, mood, tense, expected_result):
    assert cg.conjugate_mood_tense(infinitive, mood, tense) == expected_result


def test_abolir():
    """
    Reproduce error:

    >           co.template.moods[persons_mood_name].tenses[aux_tense_name].person_endings]
    E       KeyError: 'presente'

    ../../PyVEnvs/Py311/lib/python3.11/site-packages/verbecc/inflector.py:259: KeyError

    Error was occuring because the "<Subvuntivo>" was empty in the "abol:ir" template.
    """
    result = cg.conjugate("abolir")
    assert result is not None


def test_inflector_es_get_conj_obs():
    co = cg._inflector._get_conj_obs("abañar")
    assert co.verb.infinitive == "abañar"
    assert co.verb_stem == "abañ"


def test_inflector_es_get_verb_stem():
    verb_stem = cg._inflector._get_verb_stem("abañar", "cort:ar")
    assert verb_stem == "abañ"


def test_inflector_es_conjugate_simple_mood_tense():
    verb_stem = "abañ"
    tense_elem = etree.fromstring(
        """<presente>
            <p><i>o</i></p>
            <p><i>as</i></p>
            <p><i>a</i></p>
            <p><i>amos</i></p>
            <p><i>áis</i></p>
            <p><i>an</i></p>
        </presente>""",
        parser=None,
    )
    tense_name = "présent"
    tense_template = TenseTemplate(tense_elem)
    out = cg._inflector._conjugate_simple_mood_tense(
        verb_stem, "indicativo", tense_template
    )
    assert len(out) == 6
    assert out == [
        "yo abaño",
        "tú abañas",
        "él abaña",
        "nosotros abañamos",
        "vosotros abañáis",
        "ellos abañan",
    ]


test_inflector_es_get_default_pronoun_data = [
    ("1s", "m", False, "yo"),
    ("1s", "m", True, "yo me"),
    ("2s", "m", False, "tú"),
    ("2s", "m", True, "tú te"),
    ("3s", "m", False, "él"),
    ("3s", "m", True, "él se"),
    ("3s", "f", False, "ella"),
    ("3s", "f", True, "ella se"),
    ("1p", "m", False, "nosotros"),
    ("1p", "m", True, "nosotros nos"),
    ("2p", "m", False, "vosotros"),
    ("2p", "m", True, "vosotros os"),
    ("3p", "m", False, "ellos"),
    ("3p", "m", True, "ellos se"),
    ("3p", "f", False, "ellas"),
    ("3p", "f", True, "ellas se"),
]


@pytest.mark.parametrize(
    "person,gender,is_reflexive,expected_result",
    test_inflector_es_get_default_pronoun_data,
)
def test_inflector_es_get_default_pronoun(
    person, gender, is_reflexive, expected_result
):
    assert (
        cg._inflector._get_default_pronoun(person, gender, is_reflexive=is_reflexive)
        == expected_result
    )
