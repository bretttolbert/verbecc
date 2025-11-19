import pytest

from verbecc.src.conjugator.conjugator import Conjugator
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.src.defs.types.mood import Moods
from verbecc.src.defs.types.number import Number
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.tense import Tenses


@pytest.fixture(scope="module")
def cg():
    cg = Conjugator(lang=Lang.it)
    yield cg


def test_all_verbs_have_templates(cg):
    verbs = cg.get_verbs()
    template_names = cg.get_template_names()
    missing_templates = set()
    for verb in verbs:
        if verb.template not in template_names:
            missing_templates.add(verb.template)
    assert len(missing_templates) == 0


@pytest.mark.parametrize(
    "infinitive,mood,tense,expected_result",
    [
        (
            "avere",
            "indicativo",
            "presente",
            [
                "io ho",
                "tu hai",
                "lui ha",
                "lei ha",
                "noi abbiamo",
                "voi avete",
                "loro hanno",
            ],
        ),
        (
            "avere",
            "indicativo",
            "imperfetto",
            [
                "io avevo",
                "tu avevi",
                "lui aveva",
                "lei aveva",
                "noi avevamo",
                "voi avevate",
                "loro avevano",
            ],
        ),
        (
            "avere",
            "indicativo",
            "passato-remoto",
            [
                "io ebbi",
                "tu avesti",
                "lui ebbe",
                "lei ebbe",
                "noi avemmo",
                "voi aveste",
                "loro ebbero",
            ],
        ),
        (
            "avere",
            "indicativo",
            "futuro",
            [
                "io avrò",
                "tu avrai",
                "lui avrà",
                "lei avrà",
                "noi avremo",
                "voi avrete",
                "loro avranno",
            ],
        ),
    ],
)
def test_inflector_it_conjugate_mood_tense(
    cg, infinitive, mood, tense, expected_result
):
    tc = cg.conjugate_mood_tense(infinitive, mood, tense)
    assert [c[0] for c in tc] == expected_result


def test_inflector_it_conjugate(cg):
    assert cg.conjugate("avere") != None


def test_inflector_itadd_subjunctive_relative_pronoun(cg):
    assert (
        cg._inflector.add_subjunctive_relative_pronoun("io abbia", "") == "che io abbia"
    )


@pytest.mark.parametrize(
    "person,number,gender,is_reflexive,expected_result",
    [
        (Person.First, Number.Singular, Gender.m, False, "io"),
        (Person.First, Number.Singular, Gender.m, True, "io mi"),
        (Person.Second, Number.Singular, Gender.m, False, "tu"),
        (Person.Second, Number.Singular, Gender.m, True, "tu ti"),
        (Person.Third, Number.Singular, Gender.m, False, "lui"),
        (Person.Third, Number.Singular, Gender.m, True, "lui si"),
        (Person.Third, Number.Singular, Gender.f, False, "lei"),
        (Person.Third, Number.Singular, Gender.f, True, "lei si"),
        (Person.First, Number.Plural, Gender.m, False, "noi"),
        (Person.First, Number.Plural, Gender.m, True, "noi ci"),
        (Person.Second, Number.Plural, Gender.m, False, "voi"),
        (Person.Second, Number.Plural, Gender.m, True, "voi vi"),
        (Person.Third, Number.Plural, Gender.m, False, "loro"),
        (Person.Third, Number.Plural, Gender.m, True, "loro si"),
        (Person.Third, Number.Plural, Gender.f, False, "loro"),
        (Person.Third, Number.Plural, Gender.f, True, "loro si"),
    ],
)
def test_inflector_it_get_pronouns(
    cg,
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


@pytest.mark.parametrize(
    "infinitive,expected_result",
    [
        (
            "avere",
            [
                "io ho",
                "tu hai",
                "lui ha",
                "lei ha",
                "noi abbiamo",
                "voi avete",
                "loro hanno",
            ],
        ),
        (
            "essere",
            [
                "io sono",
                "tu sei",
                "lui è",
                "lei è",
                "noi siamo",
                "voi siete",
                "loro sono",
            ],
        ),
        (
            "alzare",
            [
                "io alzo",
                "tu alzi",
                "lui alza",
                "lei alza",
                "noi alziamo",
                "voi alzate",
                "loro alzano",
            ],
        ),
    ],
)
def test_indicative_present(cg, infinitive, expected_result):
    cc = cg.conjugate(infinitive)
    mc = cc["indicativo"]
    tc = mc["presente"]
    assert [c[0] for c in tc] == expected_result


@pytest.mark.parametrize(
    "infinitive,expected_result",
    [
        (
            "avere",
            [
                "io ho avuto",
                "tu hai avuto",
                "lui ha avuto",
                "lei ha avuto",
                "noi abbiamo avuto",
                "voi avete avuto",
                "loro hanno avuto",
            ],
        ),
        (
            "essere",
            [
                "io sono stata",
                "io sono stato",
                "tu sei stata",
                "tu sei stato",
                "lui è stato",
                "lei è stata",
                "noi siamo state",
                "noi siamo stati",
                "voi siete state",
                "voi siete stati",
                "loro sono state",
                "loro sono stati",
            ],
        ),
        (
            "alzare",
            [
                "io ho alzato",
                "tu hai alzato",
                "lui ha alzato",
                "lei ha alzato",
                "noi abbiamo alzato",
                "voi avete alzato",
                "loro hanno alzato",
            ],
        ),
    ],
)
def test_passato_prossimo(cg, infinitive, expected_result):
    cc = cg.conjugate(infinitive)
    mc = cc[Moods.it.Indicativo]
    tc = mc[Tenses.it.PassatoProssimo]
    assert [c[0] for c in tc] == expected_result


@pytest.mark.parametrize(
    "infinitive,expected_result",
    [
        (
            "alzarsi",
            [
                "io mi alzo",
                "tu ti alzi",
                "lui si alza",
                "lei si alza",
                "noi ci alziamo",
                "voi vi alzate",
                "loro si alzano",
            ],
        ),
    ],
)
def test_alzarsi_indicative_present(cg, infinitive, expected_result):
    cc = cg.conjugate(infinitive)
    mc = cc[Moods.it.Indicativo]
    tc = mc[Tenses.it.Presente]
    assert [c[0] for c in tc] == expected_result


@pytest.mark.parametrize(
    "infinitive,expected_result",
    [
        (
            "alzarsi",
            [
                "io mi sono alzata",
                "io mi sono alzato",
                "tu ti sei alzata",
                "tu ti sei alzato",
                "lui si è alzato",
                "lei si è alzata",
                "noi ci siamo alzate",
                "noi ci siamo alzati",
                "voi vi siete alzate",
                "voi vi siete alzati",
                "loro si sono alzate",
                "loro si sono alzati",
            ],
        ),
    ],
)
def test_inflector_it_alzarsi_indicativo_passato_prossimo(
    cg, infinitive, expected_result
):
    cc = cg.conjugate(infinitive)
    mc = cc[Moods.it.Indicativo]
    tc = mc[Tenses.it.PassatoProssimo]
    assert [c[0] for c in tc] == expected_result


def test_inflector_it_conjugate_compound_essere_indicativo_passato_prossimo(cg):
    infinitive = "essere"
    co = cg._get_conj_obs(infinitive)
    tc = cg._tense_conjugator._conjugate_compound_mood_tense(
        co,
        "indicativo",
        "passato-prossimo",
        "indicativo",
        "presente",
        False,
        True,
    )
    assert [list(c) for c in tc] == [
        ["io sono stata"],
        ["io sono stato"],
        ["tu sei stata"],
        ["tu sei stato"],
        ["lui è stato"],
        ["lei è stata"],
        ["noi siamo state"],
        ["noi siamo stati"],
        ["voi siete state"],
        ["voi siete stati"],
        ["loro sono state"],
        ["loro sono stati"],
    ]
