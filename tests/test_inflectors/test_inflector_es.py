import pytest
from lxml import etree

from verbecc.src.conjugator.complete_conjugator import CompleteConjugator
from verbecc.src.conjugator.mood_conjugator import MoodConjugator
from verbecc.src.conjugator.tense_conjugator import TenseConjugator
from verbecc.src.defs.types.conjugation import Conjugation, TenseConjugation
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.src.defs.types.mood import Moods
from verbecc.src.defs.types.number import Number
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.tense import Tenses
from verbecc.src.parsers.tense_template_parser import TenseTemplateParser
from verbecc.src.defs.types.pronoun import Pronouns


@pytest.fixture(scope="module")
def ccg():
    ccg = CompleteConjugator(lang=Lang.es)
    yield ccg


@pytest.fixture(scope="module")
def mcg():
    mcg = MoodConjugator(lang=Lang.es)
    yield mcg


@pytest.fixture(scope="module")
def tcg():
    tcg = TenseConjugator(lang=Lang.es)
    yield tcg


def test_all_verbs_have_templates(ccg):
    verbs = ccg.get_verbs()
    template_names = ccg.get_template_names()
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
                "vos abañás",
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
                "vos sos",
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
                "vos tenés",
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
                "vos habés",
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
                "vos hacés",
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
                "vos vás",
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
                "vos comés",
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
                "vos habés comido",
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
                "comé",
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
                "vos parecés",
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
                "parecé",
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
                "vos habés parecido",
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
                "vos abolís",
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
def test_inflector_es_conjugate_mood_tense(
    ccg, infinitive, mood, tense, expected_result
):
    tc = ccg.conjugate_mood_tense(infinitive, mood, tense)
    assert [c[0] for c in tc] == expected_result


def test_abolir(ccg):
    """
    Reproduce error:

    >           co.template.mood_templates[persons_mood].tense_templates[aux_tense].person_endings]
    E       KeyError: 'presente'

    ../../PyVEnvs/Py311/lib/python3.11/site-packages/verbecc/inflector.py:259: KeyError

    Error was occuring because the "<Subvuntivo>" was empty in the "abol:ir" template.
    """
    cc = ccg.conjugate("abolir")
    assert cc is not None


def test_abolir_imperativo_afirmativo(ccg):
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
    tc = ccg.conjugate_mood_tense("abolir", Moods.es.Imperativo, Tenses.es.Afirmativo)
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


def test_soler_imperativo_afirmativo(ccg):
    tc = ccg.conjugate_mood_tense("soler", Moods.es.Imperativo, Tenses.es.Afirmativo)
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


def test_soler_imperativo_negativo(ccg):
    tc = ccg.conjugate_mood_tense("soler", Moods.es.Imperativo, Tenses.es.Negativo)
    assert [c[0] for c in tc] == [
        "no suelas",
        "no suelas",
        "no suela",
        "no suela",
        "no suela",
        "no solamos",
        "no soláis",
        "no suelan",
        "no suelan",
        "no suelan",
    ]


def test_inflector_es_get_conj_obs(ccg):
    co = ccg._get_conj_obs("abañar")
    assert co.verb.infinitive == "abañar"
    assert co.verb_stem == "abañ"


def test_inflector_es_get_verb_stem_from_template_name(ccg):
    verb_stem = ccg._inflector.get_verb_stem_from_template_name("abañar", "cort:ar")
    assert verb_stem == "abañ"


def test_inflector_es_conjugate_simple_mood_tense(tcg):
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
    tc = tcg._tense_conjugator_simple._conjugate_simple_mood_tense(
        verb_stem, mood, tense, tense_template
    )
    assert [c[0] for c in tc] == [
        "yo abaño",
        "tú abañas",
        "vos abañás",
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
        (Person.First, Number.Singular, None, False, Pronouns.es.yo),
        (Person.First, Number.Singular, None, True, "yo me"),
        (Person.Second, Number.Singular, None, False, Pronouns.es.tú),
        (Person.Second, Number.Singular, None, True, "tú te"),
        (Person.Third, Number.Singular, Gender.m, False, Pronouns.es.él),
        (Person.Third, Number.Singular, Gender.m, True, "él se"),
        (Person.Third, Number.Singular, Gender.f, False, Pronouns.es.ella),
        (Person.Third, Number.Singular, Gender.f, True, "ella se"),
        (Person.First, Number.Plural, None, False, Pronouns.es.nosotros),
        (Person.First, Number.Plural, None, True, "nosotros nos"),
        (Person.Second, Number.Plural, None, False, Pronouns.es.vosotros),
        (Person.Second, Number.Plural, None, True, "vosotros os"),
        (Person.Third, Number.Plural, Gender.m, False, Pronouns.es.ellos),
        (Person.Third, Number.Plural, Gender.m, True, "ellos se"),
        (Person.Third, Number.Plural, Gender.f, False, Pronouns.es.ellas),
        (Person.Third, Number.Plural, Gender.f, True, "ellas se"),
    ],
)
def test_inflector_es_get_pronouns(
    ccg,
    person: Person,
    number: Number,
    gender: Gender,
    is_reflexive: bool,
    expected_result: str,
):
    pronoun = ccg._inflector.get_pronouns(person, number, gender)[0]
    if is_reflexive:
        pronoun = ccg._inflector.make_pronoun_reflexive(pronoun)
    assert pronoun == expected_result


def test_inflector_es_conjugate_mood_indicativo_tense_presente_ar_voseo_tipo_3(ccg):
    assert ccg.conjugate_mood_tense(
        "hablar",
        Moods.es.Indicativo,
        Tenses.es.Presente,
    ) == TenseConjugation(
        Tenses.es.Presente,
        [
            Conjugation(
                Person.First, Number.Singular, None, Pronouns.es.yo, ["yo hablo"]
            ),
            Conjugation(
                Person.Second, Number.Singular, None, Pronouns.es.tú, ["tú hablas"]
            ),
            Conjugation(
                Person.Second, Number.Singular, None, Pronouns.es.vos, ["vos hablás"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.m, Pronouns.es.él, ["él habla"]
            ),
            Conjugation(
                Person.Third,
                Number.Singular,
                Gender.f,
                Pronouns.es.ella,
                ["ella habla"],
            ),
            Conjugation(
                Person.Third, Number.Singular, None, Pronouns.es.usted, ["usted habla"]
            ),
            Conjugation(
                Person.First,
                Number.Plural,
                None,
                Pronouns.es.nosotros,
                ["nosotros hablamos"],
            ),
            Conjugation(
                Person.Second,
                Number.Plural,
                None,
                Pronouns.es.vosotros,
                ["vosotros habláis"],
            ),
            Conjugation(
                Person.Third,
                Number.Plural,
                Gender.m,
                Pronouns.es.ellos,
                ["ellos hablan"],
            ),
            Conjugation(
                Person.Third,
                Number.Plural,
                Gender.f,
                Pronouns.es.ellas,
                ["ellas hablan"],
            ),
            Conjugation(
                Person.Third,
                Number.Plural,
                None,
                Pronouns.es.ustedes,
                ["ustedes hablan"],
            ),
        ],
    )


def test_inflector_es_conjugate_mood_indicativo_tense_presente_er_voseo_tipo_3(ccg):
    assert ccg.conjugate_mood_tense(
        "beber",
        Moods.es.Indicativo,
        Tenses.es.Presente,
    ) == TenseConjugation(
        Tenses.es.Presente,
        [
            Conjugation(
                Person.First, Number.Singular, None, Pronouns.es.yo, ["yo bebo"]
            ),
            Conjugation(
                Person.Second, Number.Singular, None, Pronouns.es.tú, ["tú bebes"]
            ),
            Conjugation(
                Person.Second, Number.Singular, None, Pronouns.es.vos, ["vos bebés"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.m, Pronouns.es.él, ["él bebe"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.f, Pronouns.es.ella, ["ella bebe"]
            ),
            Conjugation(
                Person.Third, Number.Singular, None, Pronouns.es.usted, ["usted bebe"]
            ),
            Conjugation(
                Person.First,
                Number.Plural,
                None,
                Pronouns.es.nosotros,
                ["nosotros bebemos"],
            ),
            Conjugation(
                Person.Second,
                Number.Plural,
                None,
                Pronouns.es.vosotros,
                ["vosotros bebéis"],
            ),
            Conjugation(
                Person.Third,
                Number.Plural,
                Gender.m,
                Pronouns.es.ellos,
                ["ellos beben"],
            ),
            Conjugation(
                Person.Third,
                Number.Plural,
                Gender.f,
                Pronouns.es.ellas,
                ["ellas beben"],
            ),
            Conjugation(
                Person.Third,
                Number.Plural,
                None,
                Pronouns.es.ustedes,
                ["ustedes beben"],
            ),
        ],
    )


def test_inflector_es_conjugate_mood_indicativo_tense_presente_ir_voseo_tipo_3(ccg):
    assert ccg.conjugate_mood_tense(
        "dormir",
        Moods.es.Indicativo,
        Tenses.es.Presente,
    ) == TenseConjugation(
        Tenses.es.Presente,
        [
            Conjugation(
                Person.First, Number.Singular, None, Pronouns.es.yo, ["yo duermo"]
            ),
            Conjugation(
                Person.Second, Number.Singular, None, Pronouns.es.tú, ["tú duermes"]
            ),
            Conjugation(
                Person.Second, Number.Singular, None, Pronouns.es.vos, ["vos dormís"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.m, Pronouns.es.él, ["él duerme"]
            ),
            Conjugation(
                Person.Third,
                Number.Singular,
                Gender.f,
                Pronouns.es.ella,
                ["ella duerme"],
            ),
            Conjugation(
                Person.Third, Number.Singular, None, Pronouns.es.usted, ["usted duerme"]
            ),
            Conjugation(
                Person.First,
                Number.Plural,
                None,
                Pronouns.es.nosotros,
                ["nosotros dormimos"],
            ),
            Conjugation(
                Person.Second,
                Number.Plural,
                None,
                Pronouns.es.vosotros,
                ["vosotros dormís"],
            ),
            Conjugation(
                Person.Third,
                Number.Plural,
                Gender.m,
                Pronouns.es.ellos,
                ["ellos duermen"],
            ),
            Conjugation(
                Person.Third,
                Number.Plural,
                Gender.f,
                Pronouns.es.ellas,
                ["ellas duermen"],
            ),
            Conjugation(
                Person.Third,
                Number.Plural,
                None,
                Pronouns.es.ustedes,
                ["ustedes duermen"],
            ),
        ],
    )


def test_inflector_es_conjugate_mood_indicativo_tense_presente_ser_voseo_tipo_3(ccg):
    assert ccg.conjugate_mood_tense(
        "ser",
        Moods.es.Indicativo,
        Tenses.es.Presente,
    ) == TenseConjugation(
        Tenses.es.Presente,
        [
            Conjugation(
                Person.First, Number.Singular, None, Pronouns.es.yo, ["yo soy"]
            ),
            Conjugation(
                Person.Second, Number.Singular, None, Pronouns.es.tú, ["tú eres"]
            ),
            Conjugation(
                Person.Second, Number.Singular, None, Pronouns.es.vos, ["vos sos"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.m, Pronouns.es.él, ["él es"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.f, Pronouns.es.ella, ["ella es"]
            ),
            Conjugation(
                Person.Third, Number.Singular, None, Pronouns.es.usted, ["usted es"]
            ),
            Conjugation(
                Person.First,
                Number.Plural,
                None,
                Pronouns.es.nosotros,
                ["nosotros somos"],
            ),
            Conjugation(
                Person.Second,
                Number.Plural,
                None,
                Pronouns.es.vosotros,
                ["vosotros sois"],
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.m, Pronouns.es.ellos, ["ellos son"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.f, Pronouns.es.ellas, ["ellas son"]
            ),
            Conjugation(
                Person.Third, Number.Plural, None, Pronouns.es.ustedes, ["ustedes son"]
            ),
        ],
    )


def test_inflector_es_conjugate_mood_subjuntivo_tense_presente_ser_voseo_tipo_3(ccg):
    assert ccg.conjugate_mood_tense(
        "ser",
        Moods.es.Subjuntivo,
        Tenses.es.Presente,
    ) == TenseConjugation(
        Tenses.es.Presente,
        [
            Conjugation(
                Person.First, Number.Singular, None, Pronouns.es.yo, ["yo sea"]
            ),
            Conjugation(
                Person.Second, Number.Singular, None, Pronouns.es.tú, ["tú seas"]
            ),
            Conjugation(
                Person.Second, Number.Singular, None, Pronouns.es.vos, ["vos seas"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.m, Pronouns.es.él, ["él sea"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.f, Pronouns.es.ella, ["ella sea"]
            ),
            Conjugation(
                Person.Third, Number.Singular, None, Pronouns.es.usted, ["usted sea"]
            ),
            Conjugation(
                Person.First,
                Number.Plural,
                None,
                Pronouns.es.nosotros,
                ["nosotros seamos"],
            ),
            Conjugation(
                Person.Second,
                Number.Plural,
                None,
                Pronouns.es.vosotros,
                ["vosotros seáis"],
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.m, Pronouns.es.ellos, ["ellos sean"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.f, Pronouns.es.ellas, ["ellas sean"]
            ),
            Conjugation(
                Person.Third, Number.Plural, None, Pronouns.es.ustedes, ["ustedes sean"]
            ),
        ],
    )


def test_inflector_es_conjugate_mood_imperativo_tense_afirmativo_ar_voseo_tipo_3(ccg):
    assert ccg.conjugate_mood_tense(
        "hablar",
        Moods.es.Imperativo,
        Tenses.es.Afirmativo,
    ) == TenseConjugation(
        Tenses.es.Afirmativo,
        [
            Conjugation(
                Person.Second, Number.Singular, None, Pronouns.es.tú, ["habla"]
            ),
            Conjugation(
                Person.Second, Number.Singular, None, Pronouns.es.vos, ["hablá"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.m, Pronouns.es.él, ["hable"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.f, Pronouns.es.ella, ["hable"]
            ),
            Conjugation(
                Person.Third, Number.Singular, None, Pronouns.es.usted, ["hable"]
            ),
            Conjugation(
                Person.First, Number.Plural, None, Pronouns.es.nosotros, ["hablemos"]
            ),
            Conjugation(
                Person.Second, Number.Plural, None, Pronouns.es.vosotros, ["hablad"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.m, Pronouns.es.ellos, ["hablen"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.f, Pronouns.es.ellas, ["hablen"]
            ),
            Conjugation(
                Person.Third, Number.Plural, None, Pronouns.es.ustedes, ["hablen"]
            ),
        ],
    )


def test_inflector_es_conjugate_mood_imperativo_tense_negativo_ar_voseo_tipo_3(ccg):
    assert ccg.conjugate_mood_tense(
        "hablar",
        Moods.es.Imperativo,
        Tenses.es.Negativo,
    ) == TenseConjugation(
        Tenses.es.Negativo,
        [
            Conjugation(
                Person.Second, Number.Singular, None, Pronouns.es.tú, ["no hables"]
            ),
            Conjugation(
                Person.Second, Number.Singular, None, Pronouns.es.vos, ["no hables"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.m, Pronouns.es.él, ["no hable"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.f, Pronouns.es.ella, ["no hable"]
            ),
            Conjugation(
                Person.Third, Number.Singular, None, Pronouns.es.usted, ["no hable"]
            ),
            Conjugation(
                Person.First, Number.Plural, None, Pronouns.es.nosotros, ["no hablemos"]
            ),
            Conjugation(
                Person.Second, Number.Plural, None, Pronouns.es.vosotros, ["no habléis"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.m, Pronouns.es.ellos, ["no hablen"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.f, Pronouns.es.ellas, ["no hablen"]
            ),
            Conjugation(
                Person.Third, Number.Plural, None, Pronouns.es.ustedes, ["no hablen"]
            ),
        ],
    )


def test_inflector_es_conjugate_mood_imperativo_tense_afirmativo_ir_voseo_tipo_3(ccg):
    assert ccg.conjugate_mood_tense(
        "vivir",
        Moods.es.Imperativo,
        Tenses.es.Afirmativo,
    ) == TenseConjugation(
        Tenses.es.Afirmativo,
        [
            Conjugation(Person.Second, Number.Singular, None, Pronouns.es.tú, ["vive"]),
            Conjugation(
                Person.Second, Number.Singular, None, Pronouns.es.vos, ["viví"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.m, Pronouns.es.él, ["viva"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.f, Pronouns.es.ella, ["viva"]
            ),
            Conjugation(
                Person.Third, Number.Singular, None, Pronouns.es.usted, ["viva"]
            ),
            Conjugation(
                Person.First, Number.Plural, None, Pronouns.es.nosotros, ["vivamos"]
            ),
            Conjugation(
                Person.Second, Number.Plural, None, Pronouns.es.vosotros, ["vivid"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.m, Pronouns.es.ellos, ["vivan"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.f, Pronouns.es.ellas, ["vivan"]
            ),
            Conjugation(
                Person.Third, Number.Plural, None, Pronouns.es.ustedes, ["vivan"]
            ),
        ],
    )


def test_inflector_es_conjugate_mood_imperativo_tense_negativo_ir_voseo_tipo_3(ccg):
    assert ccg.conjugate_mood_tense(
        "vivir",
        Moods.es.Imperativo,
        Tenses.es.Negativo,
    ) == TenseConjugation(
        Tenses.es.Negativo,
        [
            Conjugation(
                Person.Second, Number.Singular, None, Pronouns.es.tú, ["no vivas"]
            ),
            Conjugation(
                Person.Second, Number.Singular, None, Pronouns.es.vos, ["no vivas"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.m, Pronouns.es.él, ["no viva"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.f, Pronouns.es.ella, ["no viva"]
            ),
            Conjugation(
                Person.Third, Number.Singular, None, Pronouns.es.usted, ["no viva"]
            ),
            Conjugation(
                Person.First, Number.Plural, None, Pronouns.es.nosotros, ["no vivamos"]
            ),
            Conjugation(
                Person.Second, Number.Plural, None, Pronouns.es.vosotros, ["no viváis"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.m, Pronouns.es.ellos, ["no vivan"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.f, Pronouns.es.ellas, ["no vivan"]
            ),
            Conjugation(
                Person.Third, Number.Plural, None, Pronouns.es.ustedes, ["no vivan"]
            ),
        ],
    )


def test_inflector_es_conjugate_mood_imperativo_tense_afirmativo_er_voseo_tipo_3(ccg):
    assert ccg.conjugate_mood_tense(
        "beber",
        Moods.es.Imperativo,
        Tenses.es.Afirmativo,
    ) == TenseConjugation(
        Tenses.es.Afirmativo,
        [
            Conjugation(Person.Second, Number.Singular, None, Pronouns.es.tú, ["bebe"]),
            Conjugation(
                Person.Second, Number.Singular, None, Pronouns.es.vos, ["bebé"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.m, Pronouns.es.él, ["beba"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.f, Pronouns.es.ella, ["beba"]
            ),
            Conjugation(
                Person.Third, Number.Singular, None, Pronouns.es.usted, ["beba"]
            ),
            Conjugation(
                Person.First, Number.Plural, None, Pronouns.es.nosotros, ["bebamos"]
            ),
            Conjugation(
                Person.Second, Number.Plural, None, Pronouns.es.vosotros, ["bebed"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.m, Pronouns.es.ellos, ["beban"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.f, Pronouns.es.ellas, ["beban"]
            ),
            Conjugation(
                Person.Third, Number.Plural, None, Pronouns.es.ustedes, ["beban"]
            ),
        ],
    )


def test_inflector_es_conjugate_mood_imperativo_tense_negativo_er_voseo_tipo_3(ccg):
    assert ccg.conjugate_mood_tense(
        "beber",
        Moods.es.Imperativo,
        Tenses.es.Negativo,
    ) == TenseConjugation(
        Tenses.es.Negativo,
        [
            Conjugation(
                Person.Second, Number.Singular, None, Pronouns.es.tú, ["no bebas"]
            ),
            Conjugation(
                Person.Second, Number.Singular, None, Pronouns.es.vos, ["no bebas"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.m, Pronouns.es.él, ["no beba"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.f, Pronouns.es.ella, ["no beba"]
            ),
            Conjugation(
                Person.Third, Number.Singular, None, Pronouns.es.usted, ["no beba"]
            ),
            Conjugation(
                Person.First, Number.Plural, None, Pronouns.es.nosotros, ["no bebamos"]
            ),
            Conjugation(
                Person.Second, Number.Plural, None, Pronouns.es.vosotros, ["no bebáis"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.m, Pronouns.es.ellos, ["no beban"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.f, Pronouns.es.ellas, ["no beban"]
            ),
            Conjugation(
                Person.Third, Number.Plural, None, Pronouns.es.ustedes, ["no beban"]
            ),
        ],
    )


def test_inflector_es_conjugate_mood_imperativo_tense_afirmativo_ser_voseo_tipo_3(ccg):
    assert ccg.conjugate_mood_tense(
        "ser",
        Moods.es.Imperativo,
        Tenses.es.Afirmativo,
    ) == TenseConjugation(
        Tenses.es.Afirmativo,
        [
            Conjugation(Person.Second, Number.Singular, None, Pronouns.es.tú, ["sé"]),
            Conjugation(Person.Second, Number.Singular, None, Pronouns.es.vos, ["sé"]),
            Conjugation(
                Person.Third, Number.Singular, Gender.m, Pronouns.es.él, ["sea"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.f, Pronouns.es.ella, ["sea"]
            ),
            Conjugation(
                Person.Third, Number.Singular, None, Pronouns.es.usted, ["sea"]
            ),
            Conjugation(
                Person.First, Number.Plural, None, Pronouns.es.nosotros, ["seamos"]
            ),
            Conjugation(
                Person.Second, Number.Plural, None, Pronouns.es.vosotros, ["sed"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.m, Pronouns.es.ellos, ["sean"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.f, Pronouns.es.ellas, ["sean"]
            ),
            Conjugation(
                Person.Third, Number.Plural, None, Pronouns.es.ustedes, ["sean"]
            ),
        ],
    )


def test_inflector_es_conjugate_mood_imperativo_tense_negativo_ser_voseo_tipo_3(ccg):
    assert ccg.conjugate_mood_tense(
        "ser",
        Moods.es.Imperativo,
        Tenses.es.Negativo,
    ) == TenseConjugation(
        Tenses.es.Negativo,
        [
            Conjugation(
                Person.Second, Number.Singular, None, Pronouns.es.tú, ["no seas"]
            ),
            Conjugation(
                Person.Second, Number.Singular, None, Pronouns.es.vos, ["no seas"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.m, Pronouns.es.él, ["no sea"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.f, Pronouns.es.ella, ["no sea"]
            ),
            Conjugation(
                Person.Third, Number.Singular, None, Pronouns.es.usted, ["no sea"]
            ),
            Conjugation(
                Person.First, Number.Plural, None, Pronouns.es.nosotros, ["no seamos"]
            ),
            Conjugation(
                Person.Second, Number.Plural, None, Pronouns.es.vosotros, ["no seáis"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.m, Pronouns.es.ellos, ["no sean"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.f, Pronouns.es.ellas, ["no sean"]
            ),
            Conjugation(
                Person.Third, Number.Plural, None, Pronouns.es.ustedes, ["no sean"]
            ),
        ],
    )
