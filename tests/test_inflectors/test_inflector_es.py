import pytest
from lxml import etree
from typing import cast

from verbecc.src.conjugator.conjugator import Conjugator
from verbecc.src.defs.types.conjugation import Conjugation, TenseConjugation
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.src.defs.types.lang_specific_options import LangSpecificOptions
from verbecc.src.defs.types.lang.es.lang_specific_options_es import (
    LangSpecificOptionsEs,
)
from verbecc.src.defs.types.lang.es.voseo_options import VoseoOptions
from verbecc.src.defs.types.mood import Moods
from verbecc.src.defs.types.number import Number
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.tense import Tenses
from verbecc.src.inflectors.inflector import Inflector
from verbecc.src.inflectors.lang.inflector_es import InflectorEs
from verbecc.src.parsers.tense_template_parser import TenseTemplateParser

cg = Conjugator(lang=Lang.es)


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
            Moods.es.Indicativo,
            Tenses.es.Presente,
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
            Moods.es.Indicativo,
            Tenses.es.Presente,
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
            Moods.es.Indicativo,
            Tenses.es.Presente,
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
            Moods.es.Indicativo,
            Tenses.es.Presente,
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
            Moods.es.Indicativo,
            Tenses.es.Presente,
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
            Moods.es.Indicativo,
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
            Moods.es.Indicativo,
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
            Moods.es.Indicativo,
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
            Tenses.es.Presente,
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
            Tenses.es.Presente,
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
            Moods.es.Indicativo,
            Tenses.es.Presente,
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
            Moods.es.Indicativo,
            Tenses.es.Presente,
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
            Moods.es.Indicativo,
            Tenses.es.Presente,
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
            Moods.es.Indicativo,
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
            Moods.es.Indicativo,
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
            Tenses.es.Presente,
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
            Moods.es.Indicativo,
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
            Moods.es.Indicativo,
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
            Moods.es.Indicativo,
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
            Moods.es.Indicativo,
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
            Moods.es.Indicativo,
            Tenses.es.Presente,
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
            Moods.es.Indicativo,
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
            Moods.es.Indicativo,
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
            Moods.es.Indicativo,
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
            Tenses.es.Presente,
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
            Tenses.es.Presente,
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
            Moods.es.Indicativo,
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
            Moods.es.Indicativo,
            Tenses.es.Presente,
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
    verb_stem = cg._inflector.get_verb_stem_from_template_name("abañar", "cort:ar")
    assert verb_stem == "abañ"


def test_inflector_es_conjugate_simple_mood_tense():
    mood = Moods.es.Indicativo
    tense = Tenses.es.Presente
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
    tense_template = TenseTemplateParser(Lang.es, mood).parse(tense_elem)
    out = cg._conjugate_simple_mood_tense(verb_stem, mood, tense, tense_template)
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
    "person,number,gender,is_reflexive,expected_result",
    [
        (Person.First, Number.Singular, Gender.m, False, "yo"),
        (Person.First, Number.Singular, Gender.m, True, "yo me"),
        (Person.Second, Number.Singular, Gender.m, False, "tú"),
        (Person.Second, Number.Singular, Gender.m, True, "tú te"),
        (Person.Third, Number.Singular, Gender.m, False, "él"),
        (Person.Third, Number.Singular, Gender.m, True, "él se"),
        (Person.Third, Number.Singular, Gender.f, False, "ella"),
        (Person.Third, Number.Singular, Gender.f, True, "ella se"),
        (Person.First, Number.Plural, Gender.m, False, "nosotros"),
        (Person.First, Number.Plural, Gender.m, True, "nosotros nos"),
        (Person.Second, Number.Plural, Gender.m, False, "vosotros"),
        (Person.Second, Number.Plural, Gender.m, True, "vosotros os"),
        (Person.Third, Number.Plural, Gender.m, False, "ellos"),
        (Person.Third, Number.Plural, Gender.m, True, "ellos se"),
        (Person.Third, Number.Plural, Gender.f, False, "ellas"),
        (Person.Third, Number.Plural, Gender.f, True, "ellas se"),
    ],
)
def test_inflector_es_get_default_pronoun(
    person: Person,
    number: Number,
    gender: Gender,
    is_reflexive: bool,
    expected_result: str,
):
    inf = cast(InflectorEs, cg._inflector)
    assert (
        cg._inflector.get_default_pronoun(
            person, number, gender, is_reflexive=is_reflexive
        )
        == expected_result
    )


def test_inflector_es_conjugate_mood_indicativo_tense_presente_ar_voseo_tipo_3():
    assert cg.conjugate_mood_tense(
        "hablar",
        Moods.es.Indicativo,
        Tenses.es.Presente,
    ) == TenseConjugation(
        [
            Conjugation(Person.First, Number.Singular, Gender.m, "yo", ["yo hablo"]),
            Conjugation(Person.Second, Number.Singular, Gender.m, "tú", ["tú hablas"]),
            Conjugation(
                Person.Second, Number.Singular, Gender.m, "vos", ["vos hablás"]
            ),
            Conjugation(Person.Third, Number.Singular, Gender.m, "él", ["él habla"]),
            Conjugation(
                Person.First,
                Number.Singular,
                Gender.m,
                "nosotros",
                ["nosotros hablamos"],
            ),
            Conjugation(
                Person.Second,
                Number.Singular,
                Gender.m,
                "vosotros",
                ["vosotros habláis"],
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.m, "ellos", ["ellos hablan"]
            ),
        ]
    )


def test_inflector_es_conjugate_mood_indicativo_tense_presente_er_voseo_tipo_3():
    assert cg.conjugate_mood_tense(
        "beber",
        Moods.es.Indicativo,
        Tenses.es.Presente,
    ) == TenseConjugation(
        [
            Conjugation(Person.First, Number.Singular, Gender.m, "yo", ["yo bebo"]),
            Conjugation(Person.First, Number.Singular, Gender.m, "tú", ["tú bebes"]),
            Conjugation(Person.First, Number.Singular, Gender.m, "vos", ["vos bebés"]),
            Conjugation(Person.First, Number.Singular, Gender.m, "él", ["él bebe"]),
            Conjugation(
                Person.First,
                Number.Plural,
                Gender.m,
                "nosotros",
                ["nosotros bebemos"],
            ),
            Conjugation(
                Person.Second, Number.Plural, Gender.m, "vosotros", ["vosotros bebéis"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.m, "ellos", ["ellos beben"]
            ),
        ]
    )


def test_inflector_es_conjugate_mood_indicativo_tense_presente_ir_voseo_tipo_3():
    assert cg.conjugate_mood_tense(
        "dormir",
        Moods.es.Indicativo,
        Tenses.es.Presente,
    ) == TenseConjugation(
        [
            Conjugation(Person.First, Number.Singular, Gender.m, "yo", ["yo duermo"]),
            Conjugation(Person.Second, Number.Singular, Gender.m, "tú", ["tú duermes"]),
            Conjugation(
                Person.Second, Number.Singular, Gender.m, "vos", ["vos dormís"]
            ),
            Conjugation(Person.Third, Number.Singular, Gender.m, "él", ["él duerme"]),
            Conjugation(
                Person.First,
                Number.Plural,
                Gender.m,
                "nosotros",
                ["nosotros dormimos"],
            ),
            Conjugation(
                Person.Second, Number.Plural, Gender.m, "vosotros", ["vosotros dormís"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.m, "ellos", ["ellos duermen"]
            ),
        ]
    )


def test_inflector_es_conjugate_mood_indicativo_tense_presente_ser_voseo_tipo_3():
    assert cg.conjugate_mood_tense(
        "ser",
        Moods.es.Indicativo,
        Tenses.es.Presente,
    ) == TenseConjugation(
        [
            Conjugation(Person.First, Number.Singular, Gender.m, "yo", ["yo soy"]),
            Conjugation(Person.Second, Number.Singular, Gender.m, "tú", ["tú eres"]),
            Conjugation(Person.Second, Number.Singular, Gender.m, "vos", ["vos sos"]),
            Conjugation(Person.Third, Number.Singular, Gender.m, "él", ["él es"]),
            Conjugation(
                Person.First, Number.Plural, Gender.m, "nosotros", ["nosotros somos"]
            ),
            Conjugation(
                Person.Second, Number.Plural, Gender.m, "vosotros", ["vosotros sois"]
            ),
            Conjugation(Person.Third, Number.Plural, Gender.m, "ellos", ["ellos son"]),
        ]
    )


def test_inflector_es_conjugate_mood_subjuntivo_tense_presente_ser_voseo_tipo_3():
    assert cg.conjugate_mood_tense(
        "ser",
        Moods.es.Subjuntivo,
        Tenses.es.Presente,
    ) == TenseConjugation(
        [
            Conjugation(Person.First, Number.Singular, Gender.m, "yo", ["yo sea"]),
            Conjugation(Person.Second, Number.Singular, Gender.m, "tú", ["tú seas"]),
            Conjugation(Person.Second, Number.Singular, Gender.m, "vos", ["vos seas"]),
            Conjugation(Person.Third, Number.Singular, Gender.m, "él", ["él sea"]),
            Conjugation(
                Person.First, Number.Plural, Gender.m, "nosotros", ["nosotros seamos"]
            ),
            Conjugation(
                Person.Second, Number.Plural, Gender.m, "vosotros", ["vosotros seáis"]
            ),
            Conjugation(Person.Third, Number.Plural, Gender.m, "ellos", ["ellos sean"]),
        ]
    )


def test_inflector_es_conjugate_mood_imperativo_tense_afirmativo_ar_voseo_tipo_3():
    assert cg.conjugate_mood_tense(
        "hablar",
        Moods.es.Imperativo,
        Tenses.es.Afirmativo,
    ) == TenseConjugation(
        [
            Conjugation(Person.Second, Number.Singular, Gender.m, "tú", ["habla"]),
            Conjugation(Person.Second, Number.Singular, Gender.m, "vos", ["hablá"]),
            Conjugation(Person.Third, Number.Singular, Gender.m, "él", ["hable"]),
            Conjugation(
                Person.First, Number.Plural, Gender.m, "nosotros", ["hablemos"]
            ),
            Conjugation(Person.Second, Number.Plural, Gender.m, "vosotros", ["hablad"]),
            Conjugation(Person.Third, Number.Plural, Gender.m, "ellos", ["hablen"]),
        ]
    )


def test_inflector_es_conjugate_mood_imperativo_tense_negativo_ar_voseo_tipo_3():
    assert cg.conjugate_mood_tense(
        "hablar",
        Moods.es.Imperativo,
        Tenses.es.Negativo,
    ) == TenseConjugation(
        [
            Conjugation(Person.Second, Number.Singular, Gender.m, "tú", ["no hables"]),
            Conjugation(Person.Second, Number.Singular, Gender.m, "vos", ["no hables"]),
            Conjugation(Person.Third, Number.Singular, Gender.m, "él", ["no hable"]),
            Conjugation(
                Person.First, Number.Plural, Gender.m, "nosotros", ["no hablemos"]
            ),
            Conjugation(
                Person.Second, Number.Plural, Gender.m, "vosotros", ["no habléis"]
            ),
            Conjugation(Person.Third, Number.Plural, Gender.m, "ellos", ["no hablen"]),
        ]
    )


def test_inflector_es_conjugate_mood_imperativo_tense_afirmativo_ir_voseo_tipo_3():
    assert cg.conjugate_mood_tense(
        "vivir",
        Moods.es.Imperativo,
        Tenses.es.Afirmativo,
    ) == TenseConjugation(
        [
            Conjugation(Person.Second, Number.Singular, Gender.m, "tú", ["vive"]),
            Conjugation(Person.Second, Number.Singular, Gender.m, "vos", ["viví"]),
            Conjugation(Person.Third, Number.Singular, Gender.m, "él", ["viva"]),
            Conjugation(Person.First, Number.Plural, Gender.m, "nosotros", ["vivamos"]),
            Conjugation(Person.Second, Number.Plural, Gender.m, "vosotros", ["vivid"]),
            Conjugation(Person.Third, Number.Plural, Gender.m, "ellos", ["vivan"]),
        ]
    )


def test_inflector_es_conjugate_mood_imperativo_tense_negativo_ir_voseo_tipo_3():
    assert cg.conjugate_mood_tense(
        "vivir",
        Moods.es.Imperativo,
        Tenses.es.Negativo,
    ) == TenseConjugation(
        [
            Conjugation(Person.Second, Number.Singular, Gender.m, "tú", ["no vivas"]),
            Conjugation(Person.Second, Number.Singular, Gender.m, "vos", ["no vivas"]),
            Conjugation(Person.Third, Number.Singular, Gender.m, "él", ["no viva"]),
            Conjugation(
                Person.First, Number.Plural, Gender.m, "nosotros", ["no vivamos"]
            ),
            Conjugation(
                Person.Second, Number.Plural, Gender.m, "vosotros", ["no viváis"]
            ),
            Conjugation(Person.Third, Number.Plural, Gender.m, "ellos", ["no vivan"]),
        ]
    )


def test_inflector_es_conjugate_mood_imperativo_tense_afirmativo_er_voseo_tipo_3():
    assert cg.conjugate_mood_tense(
        "beber",
        Moods.es.Imperativo,
        Tenses.es.Afirmativo,
    ) == TenseConjugation(
        [
            Conjugation(Person.Second, Number.Singular, Gender.m, "tú", ["bebe"]),
            Conjugation(Person.Second, Number.Singular, Gender.m, "vos", ["bebé"]),
            Conjugation(Person.Third, Number.Singular, Gender.m, "él", ["beba"]),
            Conjugation(Person.First, Number.Plural, Gender.m, "nosotros", ["bebamos"]),
            Conjugation(Person.Second, Number.Plural, Gender.m, "vosotros", ["bebed"]),
            Conjugation(Person.Third, Number.Plural, Gender.m, "ellos", ["beban"]),
        ]
    )


def test_inflector_es_conjugate_mood_imperativo_tense_negativo_er_voseo_tipo_3():
    assert cg.conjugate_mood_tense(
        "beber",
        Moods.es.Imperativo,
        Tenses.es.Negativo,
    ) == TenseConjugation(
        [
            Conjugation(Person.Second, Number.Singular, Gender.m, "tú", ["no bebas"]),
            Conjugation(Person.Second, Number.Singular, Gender.m, "vos", ["no bebas"]),
            Conjugation(Person.Third, Number.Singular, Gender.m, "él", ["no beba"]),
            Conjugation(
                Person.First, Number.Plural, Gender.m, "nosotros", ["no bebamos"]
            ),
            Conjugation(
                Person.Second, Number.Plural, Gender.m, "vosotros", ["no bebáis"]
            ),
            Conjugation(Person.Third, Number.Plural, Gender.m, "ellos", ["no beban"]),
        ]
    )


def test_inflector_es_conjugate_mood_imperativo_tense_afirmativo_ser_voseo_tipo_3():
    assert cg.conjugate_mood_tense(
        "ser",
        Moods.es.Imperativo,
        Tenses.es.Afirmativo,
    ) == TenseConjugation(
        [
            Conjugation(Person.Second, Number.Singular, Gender.m, "tú", ["sé"]),
            Conjugation(Person.Second, Number.Singular, Gender.m, "vos", ["sé"]),
            Conjugation(Person.Third, Number.Singular, Gender.m, "él", ["sea"]),
            Conjugation(Person.First, Number.Plural, Gender.m, "nosotros", ["seamos"]),
            Conjugation(Person.Second, Number.Plural, Gender.m, "vosotros", ["sed"]),
            Conjugation(Person.Third, Number.Plural, Gender.m, "ellos", ["sean"]),
        ]
    )


def test_inflector_es_conjugate_mood_imperativo_tense_negativo_ser_voseo_tipo_3():
    assert cg.conjugate_mood_tense(
        "ser",
        Moods.es.Imperativo,
        Tenses.es.Negativo,
    ) == TenseConjugation(
        [
            Conjugation(Person.Second, Number.Singular, Gender.m, "tú", ["no seas"]),
            Conjugation(Person.Second, Number.Singular, Gender.m, "vos", ["no seas"]),
            Conjugation(Person.Third, Number.Singular, Gender.m, "él", ["no sea"]),
            Conjugation(
                Person.First, Number.Plural, Gender.m, "nosotros", ["no seamos"]
            ),
            Conjugation(
                Person.Second, Number.Plural, Gender.m, "vosotros", ["no seáis"]
            ),
            Conjugation(Person.Third, Number.Plural, Gender.m, "ellos", ["no sean"]),
        ]
    )
