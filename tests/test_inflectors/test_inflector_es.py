import pytest
from lxml import etree

from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.mood import Mood
from verbecc.src.defs.types.tense import Tense
from verbecc.src.defs.types.lang_specific_options import LangSpecificOptions
from verbecc.src.defs.types.lang.es.lang_specific_options_es import (
    LangSpecificOptionsEs,
)
from verbecc.src.defs.types.lang.es.voseo_options import VoseoOptions
from verbecc.src.conjugator.conjugator import Conjugator
from verbecc.src.parsers.tense_template import TenseTemplate

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
@pytest.mark.parametrize(
    "infinitive,mood,tense,expected_result",
    [
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
            [
                "yo soy",
                "tú eres",
                "él es",
                "nosotros somos",
                "vosotros sois",
                "ellos son",
            ],
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
            [
                "yo he",
                "tú has",
                "él hay",
                "nosotros hemos",
                "vosotros habéis",
                "ellos han",
            ],
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
            [
                "yo voy",
                "tú vas",
                "él va",
                "nosotros vamos",
                "vosotros vais",
                "ellos van",
            ],
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
            [
                "no parezcas",
                "no parezca",
                "no parezcamos",
                "no parezcáis",
                "no parezcan",
            ],
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
    ],
)
def test_inflector_es_conjugate_mood_tense(infinitive, mood, tense, expected_result):
    assert cg.conjugate_mood_tense(infinitive, mood, tense) == expected_result


def test_abolir():
    """
    Reproduce error:

    >           co.template.mood_templates[persons_mood].tense_templates[aux_tense].person_endings]
    E       KeyError: 'presente'

    ../../PyVEnvs/Py311/lib/python3.11/site-packages/verbecc/inflector.py:259: KeyError

    Error was occuring because the "<Subvuntivo>" was empty in the "abol:ir" template.
    """
    result = cg.conjugate("abolir")
    assert result is not None


def test_inflector_es_get_conj_obs():
    co = cg._get_conj_obs("abañar")
    assert co.verb.infinitive == "abañar"
    assert co.verb_stem == "abañ"


def test_inflector_es_get_verb_stem_from_template_name():
    verb_stem = cg._inflector._get_verb_stem_from_template_name("abañar", "cort:ar")
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
    tense = "présent"
    tense_template = TenseTemplate(tense_elem)
    out = cg._conjugate_simple_mood_tense(
        verb_stem, "indicativo", tense, tense_template
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


@pytest.mark.parametrize(
    "person,gender,is_reflexive,expected_result",
    [
        (Person.FirstPersonSingular, Gender.m, False, "yo"),
        (Person.FirstPersonSingular, Gender.m, True, "yo me"),
        (Person.SecondPersonSingular, Gender.m, False, "tú"),
        (Person.SecondPersonSingular, Gender.m, True, "tú te"),
        (Person.ThirdPersonSingular, Gender.m, False, "él"),
        (Person.ThirdPersonSingular, Gender.m, True, "él se"),
        (Person.ThirdPersonSingular, Gender.f, False, "ella"),
        (Person.ThirdPersonSingular, Gender.f, True, "ella se"),
        (Person.FirstPersonPlural, Gender.m, False, "nosotros"),
        (Person.FirstPersonPlural, Gender.m, True, "nosotros nos"),
        (Person.SecondPersonPlural, Gender.m, False, "vosotros"),
        (Person.SecondPersonPlural, Gender.m, True, "vosotros os"),
        (Person.ThirdPersonPlural, Gender.m, False, "ellos"),
        (Person.ThirdPersonPlural, Gender.m, True, "ellos se"),
        (Person.ThirdPersonPlural, Gender.f, False, "ellas"),
        (Person.ThirdPersonPlural, Gender.f, True, "ellas se"),
    ],
)
def test_inflector_es_get_default_pronoun(
    person: Person, gender: Gender, is_reflexive: bool, expected_result: str
):
    assert (
        cg._inflector.get_default_pronoun(person, gender, is_reflexive=is_reflexive)
        == expected_result
    )


def test_inflector_es_conjugate_mood_tense_ar_no_voseo():
    assert cg.conjugate_mood_tense("hablar", Mood.es.Indicativo, Tense.es.Presente) == [
        "yo hablo",
        "tú hablas",
        "él habla",
        "nosotros hablamos",
        "vosotros habláis",
        "ellos hablan",
    ]


def test_inflector_es_conjugate_mood_tense_ar_voseo_tipo_3():
    assert cg.conjugate_mood_tense(
        "hablar",
        Mood.es.Indicativo,
        Tense.es.Presente,
        lang_specific_options=LangSpecificOptionsEs(
            voseo_options=VoseoOptions.VoseoTipo3
        ),
    ) == [
        "yo hablo",
        "vos hablás",
        "él habla",
        "nosotros hablamos",
        "vosotros habláis",
        "ellos hablan",
    ]


def test_inflector_es_conjugate_mood_tense_er_no_voseo():
    assert cg.conjugate_mood_tense("beber", Mood.es.Indicativo, Tense.es.Presente) == [
        "yo bebo",
        "tú bebes",
        "él bebe",
        "nosotros bebemos",
        "vosotros bebéis",
        "ellos beben",
    ]


def test_inflector_es_conjugate_mood_tense_er_voseo_tipo_3():
    assert cg.conjugate_mood_tense(
        "beber",
        Mood.es.Indicativo,
        Tense.es.Presente,
        lang_specific_options=LangSpecificOptionsEs(
            voseo_options=VoseoOptions.VoseoTipo3
        ),
    ) == [
        "yo bebo",
        "vos bebés",
        "él bebe",
        "nosotros bebemos",
        "vosotros bebéis",
        "ellos beben",
    ]


def test_inflector_es_conjugate_mood_tense_ir_no_voseo():
    assert cg.conjugate_mood_tense("dormir", Mood.es.Indicativo, Tense.es.Presente) == [
        "yo duermo",
        "tú duermes",
        "él duerme",
        "nosotros dormimos",
        "vosotros dormís",
        "ellos duermen",
    ]


def test_inflector_es_conjugate_mood_tense_ir_voseo_tipo_3():
    assert cg.conjugate_mood_tense(
        "dormir",
        Mood.es.Indicativo,
        Tense.es.Presente,
        lang_specific_options=LangSpecificOptionsEs(
            voseo_options=VoseoOptions.VoseoTipo3
        ),
    ) == [
        "yo duermo",
        "vos dormís",
        "él duerme",
        "nosotros dormimos",
        "vosotros dormís",
        "ellos duermen",
    ]
