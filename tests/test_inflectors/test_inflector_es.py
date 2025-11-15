import pytest
from lxml import etree

from verbecc.src.conjugator.conjugator import Conjugator
from verbecc.src.defs.types.conjugation import Conjugation, TenseConjugation
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.src.defs.types.mood import Moods
from verbecc.src.defs.types.number import Number
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.tense import Tenses
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
                "vos abañas",
                "él abaña",
                "ella abaña",
                "usted abaña",
                "nosotros abañamos",
                "vosotros abañáis",
                "ellos abañan",
                "ellas abañan",
                "ustedes abañan",
            ],
        ),
        (
            "estar",
            Moods.es.Indicativo,
            Tenses.es.Presente,
            [
                "yo estoy",
                "tú estás",
                "vos estás",
                "él está",
                "ella está",
                "usted está",
                "nosotros estamos",
                "vosotros estáis",
                "ellos están",
                "ellas están",
                "ustedes están",
            ],
        ),
        (
            "ser",
            Moods.es.Indicativo,
            Tenses.es.Presente,
            [
                "yo soy",
                "tú eres",
                "vos eres",
                "él es",
                "ella es",
                "usted es",
                "nosotros somos",
                "vosotros sois",
                "ellos son",
                "ellas son",
                "ustedes son",
            ],
        ),
        (
            "tener",
            Moods.es.Indicativo,
            Tenses.es.Presente,
            [
                "yo tengo",
                "tú tienes",
                "vos tienes",
                "él tiene",
                "ella tiene",
                "usted tiene",
                "nosotros tenemos",
                "vosotros tenéis",
                "ellos tienen",
                "ellas tienen",
                "ustedes tienen",
            ],
        ),
        (
            "haber",
            Moods.es.Indicativo,
            Tenses.es.Presente,
            [
                "yo he",
                "tú has",
                "vos has",
                "él hay",
                "ella hay",
                "usted hay",
                "nosotros hemos",
                "vosotros habéis",
                "ellos han",
                "ellas han",
                "ustedes han",
            ],
        ),
        (
            "haber",
            Moods.es.Indicativo,
            Tenses.es.PretéritoImperfecto,
            [
                "yo había",
                "tú habías",
                "vos habías",
                "él había",
                "ella había",
                "usted había",
                "nosotros habíamos",
                "vosotros habíais",
                "ellos habían",
                "ellas habían",
                "ustedes habían",
            ],
        ),
        (
            "haber",
            Moods.es.Indicativo,
            Tenses.es.PretéritoPerfectoSimple,
            [
                "yo hube",
                "tú hubiste",
                "vos hubiste",
                "él hubo",
                "ella hubo",
                "usted hubo",
                "nosotros hubimos",
                "vosotros hubisteis",
                "ellos hubieron",
                "ellas hubieron",
                "ustedes hubieron",
            ],
        ),
        (
            "haber",
            Moods.es.Indicativo,
            Tenses.es.Futuro,
            [
                "yo habré",
                "tú habrás",
                "vos habrás",
                "él habrá",
                "ella habrá",
                "usted habrá",
                "nosotros habremos",
                "vosotros habréis",
                "ellos habrán",
                "ellas habrán",
                "ustedes habrán",
            ],
        ),
        (
            "haber",
            Moods.es.Condicional,
            Tenses.es.Presente,
            [
                "yo habría",
                "tú habrías",
                "vos habrías",
                "él habría",
                "ella habría",
                "usted habría",
                "nosotros habríamos",
                "vosotros habríais",
                "ellos habrían",
                "ellas habrían",
                "ustedes habrían",
            ],
        ),
        (
            "haber",
            Moods.es.Subjuntivo,
            Tenses.es.Presente,
            [
                "yo haya",
                "tú hayas",
                "vos hayas",
                "él haya",
                "ella haya",
                "usted haya",
                "nosotros hayamos",
                "vosotros hayáis",
                "ellos hayan",
                "ellas hayan",
                "ustedes hayan",
            ],
        ),
        (
            "haber",
            Moods.es.Subjuntivo,
            Tenses.es.PretéritoImperfecto1,
            [
                "yo hubiera",
                "tú hubieras",
                "vos hubieras",
                "él hubiera",
                "ella hubiera",
                "usted hubiera",
                "nosotros hubiéramos",
                "vosotros hubierais",
                "ellos hubieran",
                "ellas hubieran",
                "ustedes hubieran",
            ],
        ),
        (
            "haber",
            Moods.es.Subjuntivo,
            Tenses.es.PretéritoImperfecto2,
            [
                "yo hubiese",
                "tú hubieses",
                "vos hubieses",
                "él hubiese",
                "ella hubiese",
                "usted hubiese",
                "nosotros hubiésemos",
                "vosotros hubieseis",
                "ellos hubiesen",
                "ellas hubiesen",
                "ustedes hubiesen",
            ],
        ),
        (
            "haber",
            Moods.es.Subjuntivo,
            Tenses.es.Futuro,
            [
                "yo hubiere",
                "tú hubieres",
                "vos hubieres",
                "él hubiere",
                "ella hubiere",
                "usted hubiere",
                "nosotros hubiéremos",
                "vosotros hubiereis",
                "ellos hubieren",
                "ellas hubieren",
                "ustedes hubieren",
            ],
        ),
        (
            "hacer",
            Moods.es.Indicativo,
            Tenses.es.Presente,
            [
                "yo hago",
                "tú haces",
                "vos haces",
                "él hace",
                "ella hace",
                "usted hace",
                "nosotros hacemos",
                "vosotros hacéis",
                "ellos hacen",
                "ellas hacen",
                "ustedes hacen",
            ],
        ),
        (
            "ir",
            Moods.es.Indicativo,
            Tenses.es.Presente,
            [
                "yo voy",
                "tú vas",
                "vos vas",
                "él va",
                "ella va",
                "usted va",
                "nosotros vamos",
                "vosotros vais",
                "ellos van",
                "ellas van",
                "ustedes van",
            ],
        ),
        (
            "comer",
            Moods.es.Indicativo,
            Tenses.es.Presente,
            [
                "yo como",
                "tú comes",
                "vos comes",
                "él come",
                "ella come",
                "usted come",
                "nosotros comemos",
                "vosotros coméis",
                "ellos comen",
                "ellas comen",
                "ustedes comen",
            ],
        ),
        (
            "comer",
            Moods.es.Indicativo,
            Tenses.es.PretéritoPerfectoSimple,
            [
                "yo comí",
                "tú comiste",
                "vos comiste",
                "él comió",
                "ella comió",
                "usted comió",
                "nosotros comimos",
                "vosotros comisteis",
                "ellos comieron",
                "ellas comieron",
                "ustedes comieron",
            ],
        ),
        (
            "comer",
            Moods.es.Indicativo,
            Tenses.es.PretéritoImperfecto,
            [
                "yo comía",
                "tú comías",
                "vos comías",
                "él comía",
                "ella comía",
                "usted comía",
                "nosotros comíamos",
                "vosotros comíais",
                "ellos comían",
                "ellas comían",
                "ustedes comían",
            ],
        ),
        (
            "comer",
            Moods.es.Condicional,
            Tenses.es.Presente,
            [
                "yo comería",
                "tú comerías",
                "vos comerías",
                "él comería",
                "ella comería",
                "usted comería",
                "nosotros comeríamos",
                "vosotros comeríais",
                "ellos comerían",
                "ellas comerían",
                "ustedes comerían",
            ],
        ),
        (
            "comer",
            Moods.es.Indicativo,
            Tenses.es.PretéritoPerfectoCompuesto,
            [
                "yo he comido",
                "tú has comido",
                "vos has comido",
                "él ha comido",
                "ella ha comido",
                "usted ha comido",
                "nosotros hemos comido",
                "vosotros habéis comido",
                "ellos han comido",
                "ellas han comido",
                "ustedes han comido",
            ],
        ),
        (
            "comer",
            Moods.es.Indicativo,
            Tenses.es.PretéritoPluscuamperfecto,
            [
                "yo había comido",
                "tú habías comido",
                "vos habías comido",
                "él había comido",
                "ella había comido",
                "usted había comido",
                "nosotros habíamos comido",
                "vosotros habíais comido",
                "ellos habían comido",
                "ellas habían comido",
                "ustedes habían comido",
            ],
        ),
        (
            "comer",
            Moods.es.Indicativo,
            Tenses.es.PretéritoAnterior,
            [
                "yo hube comido",
                "tú hubiste comido",
                "vos hubiste comido",
                "él hubo comido",
                "ella hubo comido",
                "usted hubo comido",
                "nosotros hubimos comido",
                "vosotros hubisteis comido",
                "ellos hubieron comido",
                "ellas hubieron comido",
                "ustedes hubieron comido",
            ],
        ),
        (
            "comer",
            Moods.es.Indicativo,
            Tenses.es.FuturoPerfecto,
            [
                "yo habré comido",
                "tú habrás comido",
                "vos habrás comido",
                "él habrá comido",
                "ella habrá comido",
                "usted habrá comido",
                "nosotros habremos comido",
                "vosotros habréis comido",
                "ellos habrán comido",
                "ellas habrán comido",
                "ustedes habrán comido",
            ],
        ),
        (
            "comer",
            Moods.es.Condicional,
            Tenses.es.Perfecto,
            [
                "yo habría comido",
                "tú habrías comido",
                "vos habrías comido",
                "él habría comido",
                "ella habría comido",
                "usted habría comido",
                "nosotros habríamos comido",
                "vosotros habríais comido",
                "ellos habrían comido",
                "ellas habrían comido",
                "ustedes habrían comido",
            ],
        ),
        (
            "comer",
            Moods.es.Subjuntivo,
            Tenses.es.PretéritoPerfecto,
            [
                "yo haya comido",
                "tú hayas comido",
                "vos hayas comido",
                "él haya comido",
                "ella haya comido",
                "usted haya comido",
                "nosotros hayamos comido",
                "vosotros hayáis comido",
                "ellos hayan comido",
                "ellas hayan comido",
                "ustedes hayan comido",
            ],
        ),
        (
            "comer",
            Moods.es.Subjuntivo,
            Tenses.es.PretéritoPluscuamperfecto1,
            [
                "yo hubiera comido",
                "tú hubieras comido",
                "vos hubieras comido",
                "él hubiera comido",
                "ella hubiera comido",
                "usted hubiera comido",
                "nosotros hubiéramos comido",
                "vosotros hubierais comido",
                "ellos hubieran comido",
                "ellas hubieran comido",
                "ustedes hubieran comido",
            ],
        ),
        (
            "comer",
            Moods.es.Subjuntivo,
            Tenses.es.PretéritoPluscuamperfecto2,
            [
                "yo hubiese comido",
                "tú hubieses comido",
                "vos hubieses comido",
                "él hubiese comido",
                "ella hubiese comido",
                "usted hubiese comido",
                "nosotros hubiésemos comido",
                "vosotros hubieseis comido",
                "ellos hubiesen comido",
                "ellas hubiesen comido",
                "ustedes hubiesen comido",
            ],
        ),
        (
            "comer",
            Moods.es.Subjuntivo,
            Tenses.es.FuturoPerfecto,
            [
                "yo hubiere comido",
                "tú hubieres comido",
                "vos hubieres comido",
                "él hubiere comido",
                "ella hubiere comido",
                "usted hubiere comido",
                "nosotros hubiéremos comido",
                "vosotros hubiereis comido",
                "ellos hubieren comido",
                "ellas hubieren comido",
                "ustedes hubieren comido",
            ],
        ),
        (
            "comer",
            Moods.es.Imperativo,
            Tenses.es.Afirmativo,
            [
                "come",
                "come",
                "coma",
                "coma",
                "coma",
                "comamos",
                "comed",
                "coman",
                "coman",
                "coman",
            ],
        ),
        (
            "comer",
            Moods.es.Imperativo,
            Tenses.es.Negativo,
            [
                "no comas",
                "no comas",
                "no coma",
                "no coma",
                "no coma",
                "no comamos",
                "no comáis",
                "no coman",
                "no coman",
                "no coman",
            ],
        ),
        (
            "parecer",
            Moods.es.Indicativo,
            Tenses.es.Presente,
            [
                "yo parezco",
                "tú pareces",
                "vos pareces",
                "él parece",
                "ella parece",
                "usted parece",
                "nosotros parecemos",
                "vosotros parecéis",
                "ellos parecen",
                "ellas parecen",
                "ustedes parecen",
            ],
        ),
        (
            "parecer",
            Moods.es.Indicativo,
            Tenses.es.PretéritoImperfecto,
            [
                "yo parecía",
                "tú parecías",
                "vos parecías",
                "él parecía",
                "ella parecía",
                "usted parecía",
                "nosotros parecíamos",
                "vosotros parecíais",
                "ellos parecían",
                "ellas parecían",
                "ustedes parecían",
            ],
        ),
        (
            "parecer",
            Moods.es.Indicativo,
            Tenses.es.PretéritoPerfectoSimple,
            [
                "yo parecí",
                "tú pareciste",
                "vos pareciste",
                "él pareció",
                "ella pareció",
                "usted pareció",
                "nosotros parecimos",
                "vosotros parecisteis",
                "ellos parecieron",
                "ellas parecieron",
                "ustedes parecieron",
            ],
        ),
        (
            "parecer",
            Moods.es.Indicativo,
            Tenses.es.Futuro,
            [
                "yo pareceré",
                "tú parecerás",
                "vos parecerás",
                "él parecerá",
                "ella parecerá",
                "usted parecerá",
                "nosotros pareceremos",
                "vosotros pareceréis",
                "ellos parecerán",
                "ellas parecerán",
                "ustedes parecerán",
            ],
        ),
        (
            "parecer",
            Moods.es.Subjuntivo,
            Tenses.es.Presente,
            [
                "yo parezca",
                "tú parezcas",
                "vos parezcas",
                "él parezca",
                "ella parezca",
                "usted parezca",
                "nosotros parezcamos",
                "vosotros parezcáis",
                "ellos parezcan",
                "ellas parezcan",
                "ustedes parezcan",
            ],
        ),
        (
            "parecer",
            Moods.es.Subjuntivo,
            Tenses.es.PretéritoImperfecto1,
            [
                "yo pareciera",
                "tú parecieras",
                "vos parecieras",
                "él pareciera",
                "ella pareciera",
                "usted pareciera",
                "nosotros pareciéramos",
                "vosotros parecierais",
                "ellos parecieran",
                "ellas parecieran",
                "ustedes parecieran",
            ],
        ),
        (
            "parecer",
            Moods.es.Subjuntivo,
            Tenses.es.PretéritoImperfecto2,
            [
                "yo pareciese",
                "tú parecieses",
                "vos parecieses",
                "él pareciese",
                "ella pareciese",
                "usted pareciese",
                "nosotros pareciésemos",
                "vosotros parecieseis",
                "ellos pareciesen",
                "ellas pareciesen",
                "ustedes pareciesen",
            ],
        ),
        (
            "parecer",
            Moods.es.Subjuntivo,
            Tenses.es.Futuro,
            [
                "yo pareciere",
                "tú parecieres",
                "vos parecieres",
                "él pareciere",
                "ella pareciere",
                "usted pareciere",
                "nosotros pareciéremos",
                "vosotros pareciereis",
                "ellos parecieren",
                "ellas parecieren",
                "ustedes parecieren",
            ],
        ),
        (
            "parecer",
            Moods.es.Imperativo,
            Tenses.es.Afirmativo,
            [
                "parece",
                "parece",
                "parezca",
                "parezca",
                "parezca",
                "parezcamos",
                "pareced",
                "parezcan",
                "parezcan",
                "parezcan",
            ],
        ),
        (
            "parecer",
            Moods.es.Imperativo,
            Tenses.es.Negativo,
            [
                "no parezcas",
                "no parezcas",
                "no parezca",
                "no parezca",
                "no parezca",
                "no parezcamos",
                "no parezcáis",
                "no parezcan",
                "no parezcan",
                "no parezcan",
            ],
        ),
        (
            "parecer",
            Moods.es.Condicional,
            Tenses.es.Presente,
            [
                "yo parecería",
                "tú parecerías",
                "vos parecerías",
                "él parecería",
                "ella parecería",
                "usted parecería",
                "nosotros pareceríamos",
                "vosotros pareceríais",
                "ellos parecerían",
                "ellas parecerían",
                "ustedes parecerían",
            ],
        ),
        (
            "parecer",
            Moods.es.Indicativo,
            Tenses.es.PretéritoPerfectoCompuesto,
            [
                "yo he parecido",
                "tú has parecido",
                "vos has parecido",
                "él ha parecido",
                "ella ha parecido",
                "usted ha parecido",
                "nosotros hemos parecido",
                "vosotros habéis parecido",
                "ellos han parecido",
                "ellas han parecido",
                "ustedes han parecido",
            ],
        ),
        (
            "abolir",
            Moods.es.Indicativo,
            Tenses.es.Presente,
            [
                "yo abolo",
                "tú aboles",
                "vos aboles",
                "él abole",
                "ella abole",
                "usted abole",
                "nosotros abolimos",
                "vosotros abolís",
                "ellos abolen",
                "ellas abolen",
                "ustedes abolen",
            ],
        ),
        (
            "abolir",
            Moods.es.Subjuntivo,
            Tenses.es.Futuro,
            [
                "yo aboliere",
                "tú abolieres",
                "vos abolieres",
                "él aboliere",
                "ella aboliere",
                "usted aboliere",
                "nosotros aboliéremos",
                "vosotros aboliereis",
                "ellos abolieren",
                "ellas abolieren",
                "ustedes abolieren",
            ],
        ),
    ],
)
def test_inflector_es_conjugate_mood_tense(infinitive, mood, tense, expected_result):
    tc = cg.conjugate_mood_tense(infinitive, mood, tense)
    assert [c[0] for c in tc] == expected_result


def test_abolir():
    """
    Reproduce error:

    >           co.template.mood_templates[persons_mood].tense_templates[aux_tense].person_endings]
    E       KeyError: 'presente'

    ../../PyVEnvs/Py311/lib/python3.11/site-packages/verbecc/inflector.py:259: KeyError

    Error was occuring because the "<Subvuntivo>" was empty in the "abol:ir" template.
    """
    cc = cg.conjugate("abolir")
    assert cc is not None


def test_abolir_imperativo_afirmativo():
    """
    Reproduce another error with this verb
        # step one for imperativo: remove the trailing 'd'
    >   if ending[-1] == "d":
           ^^^^^^^^^^
    E   IndexError: string index out of range

    Error was occuring because of another issue with "abol:ir" template

    Need to fix such issues in conjugations-es.xml
    by searching for "<i/><"

    """
    tc = cg.conjugate_mood_tense("abolir", Moods.es.Imperativo, Tenses.es.Afirmativo)
    assert [c[0] for c in tc] == [
        "abole",
        "abolí",
        "abola",
        "abola",
        "abola",
        "abolamos",
        "abolid",
        "abolan",
        "abolan",
        "abolan",
    ]


def test_soler_imperativo_afirmativo():
    tc = cg.conjugate_mood_tense("soler", Moods.es.Imperativo, Tenses.es.Afirmativo)
    assert [c[0] for c in tc] == [
        "suele",
        "solé",
        "suela",
        "suela",
        "suela",
        "solamos",
        "soled",
        "suelan",
        "suelan",
        "suelan",
    ]


def test_soler_imperativo_negativo():
    tc = cg.conjugate_mood_tense("soler", Moods.es.Imperativo, Tenses.es.Negativo)
    assert [c[0] for c in tc] == [
        "no suelas",
        "no suelas",
        "no suela",
        "no suela",
        "no suela",
        "no solamos",
        "no solaís",
        "no suelan",
        "no suelan",
        "no suelan",
    ]


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
    tc = cg._conjugate_simple_mood_tense(verb_stem, mood, tense, tense_template)
    assert [c[0] for c in tc] == [
        "yo abaño",
        "tú abañas",
        "vos abañas",
        "él abaña",
        "ella abaña",
        "usted abaña",
        "nosotros abañamos",
        "vosotros abañáis",
        "ellos abañan",
        "ellas abañan",
        "ustedes abañan",
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
def test_inflector_es_get_pronouns(
    person: Person,
    number: Number,
    gender: Gender,
    is_reflexive: bool,
    expected_result: str,
):
    pronoun = cg._inflector.get_pronouns(person, number, gender)[0]
    if is_reflexive:
        pronoun = cg._inflector.make_pronoun_reflexive(pronoun)
    assert pronoun == expected_result


def test_inflector_es_conjugate_mood_indicativo_tense_presente_ar_voseo_tipo_3():
    assert cg.conjugate_mood_tense(
        "hablar",
        Moods.es.Indicativo,
        Tenses.es.Presente,
    ) == TenseConjugation(
        [
            Conjugation(Person.First, Number.Singular, None, "yo", ["yo hablo"]),
            Conjugation(Person.Second, Number.Singular, None, "tú", ["tú hablas"]),
            Conjugation(Person.Second, Number.Singular, None, "vos", ["vos hablás"]),
            Conjugation(Person.Third, Number.Singular, Gender.m, "él", ["él habla"]),
            Conjugation(
                Person.Third, Number.Singular, Gender.f, "ella", ["ella habla"]
            ),
            Conjugation(Person.Third, Number.Singular, None, "usted", ["usted habla"]),
            Conjugation(
                Person.First,
                Number.Plural,
                None,
                "nosotros",
                ["nosotros hablamos"],
            ),
            Conjugation(
                Person.Second,
                Number.Plural,
                None,
                "vosotros",
                ["vosotros habláis"],
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.m, "ellos", ["ellos hablan"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.f, "ellas", ["ellas hablan"]
            ),
            Conjugation(
                Person.Third, Number.Plural, None, "ustedes", ["ustedes hablan"]
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
