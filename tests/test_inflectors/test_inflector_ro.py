import pytest

from typing import Generator

from verbecc.core.conjugator.complete_conjugator import CompleteConjugator
from verbecc.core.conjugator.mood_conjugator import MoodConjugator
from verbecc.core.conjugator.tense_conjugator import TenseConjugator
from verbecc.core.defs.types.conjugation import Conjugation
from verbecc.core.defs.types.conjugation import TenseConjugation
from verbecc.core.defs.types.gender import Gender
from verbecc.core.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.core.defs.types.mood import Moods
from verbecc.core.defs.types.mood import Mood
from verbecc.core.defs.types.number import Number
from verbecc.core.defs.types.person import Person
from verbecc.core.defs.types.tense import Tenses
from verbecc.core.defs.types.tense import Tense
from verbecc.core.defs.types.pronoun import Pronouns


@pytest.fixture(scope="module")
def ccg() -> Generator[CompleteConjugator, None, None]:
    # Setup
    ccg = CompleteConjugator(lang=Lang.ro)
    yield ccg
    # Teardown


@pytest.fixture(scope="module")
def mcg():
    mcg = MoodConjugator(lang=Lang.ro)
    yield mcg


@pytest.fixture(scope="module")
def tcg():
    tcg = TenseConjugator(lang=Lang.ro)
    yield tcg


def test_all_verbs_have_templates(ccg: CompleteConjugator):
    verbs = ccg.get_verbs()
    template_names = ccg.get_template_names()
    missing_templates: set[str] = set()
    for verb in verbs:
        if verb.template not in template_names:
            missing_templates.add(verb.template)
    assert len(missing_templates) == 0


@pytest.mark.parametrize(
    "infinitive,mood,tense,expected_result",
    [
        (
            "avea",
            Moods.ro.Indicativ,
            Tenses.ro.PerfectSimplu,
            [
                "eu avui",
                "tu avuși",
                "el avu",
                "ea avu",
                "noi avurăm",
                "voi avurăţi",
                "ei avură",
                "ele avură",
            ],
        ),
        (
            "avea",
            Moods.ro.Indicativ,
            Tenses.ro.PerfectCompus,
            [
                "eu am avut",
                "tu ai avut",
                "el a avut",
                "ea a avut",
                "noi am avut",
                "voi aţi avut",
                "ei au avut",
                "ele au avut",
            ],
        ),
        (
            "avea",
            Moods.ro.Indicativ,
            Tenses.ro.MaiMultCaPerfect,
            [
                "eu avusem",
                "tu avuseși",
                "el avuse",
                "ea avuse",
                "noi avuserăm",
                "voi avuserăţi",
                "ei avuseră",
                "ele avuseră",
            ],
        ),
        (
            "face",
            Moods.ro.Indicativ,
            Tenses.ro.Prezent,
            [
                "eu fac",
                "tu faci",
                "el face",
                "ea face",
                "noi facem",
                "voi faceţi",
                "ei fac",
                "ele fac",
            ],
        ),
        (
            "face",
            Moods.ro.Indicativ,
            Tenses.ro.Imperfect,
            [
                "eu făceam",
                "tu făceai",
                "el făcea",
                "ea făcea",
                "noi făceam",
                "voi făceaţi",
                "ei făceau",
                "ele făceau",
            ],
        ),
        (
            "face",
            Moods.ro.Indicativ,
            Tenses.ro.PerfectSimplu,
            [
                "eu făcui",
                "tu făcuși",
                "el făcu",
                "ea făcu",
                "noi făcurăm",
                "voi făcurăţi",
                "ei făcură",
                "ele făcură",
            ],
        ),
        (
            "face",
            Moods.ro.Indicativ,
            Tenses.ro.Viitor1,
            [
                "eu voi face",
                "tu vei face",
                "el va face",
                "ea va face",
                "noi vom face",
                "voi veţi face",
                "ei vor face",
                "ele vor face",
            ],
        ),
        (
            "face",
            Moods.ro.Indicativ,
            "viitor-2",
            [
                "eu voi fi făcut",
                "tu vei fi făcut",
                "el va fi făcut",
                "ea va fi făcut",
                "noi vom fi făcut",
                "voi veţi fi făcut",
                "ei vor fi făcut",
                "ele vor fi făcut",
            ],
        ),
        (
            "face",
            Moods.ro.Conjunctiv,
            Tenses.ro.Prezent,
            [
                "eu să fac",
                "tu să faci",
                "el să facă",
                "ea să facă",
                "noi să facem",
                "voi să faceţi",
                "ei să facă",
                "ele să facă",
            ],
        ),
        (
            "face",
            Moods.ro.Conjunctiv,
            Tenses.ro.Perfect,
            [
                "eu să fi făcut",
                "tu să fi făcut",
                "el să fi făcut",
                "ea să fi făcut",
                "noi să fi făcut",
                "voi să fi făcut",
                "ei să fi făcut",
                "ele să fi făcut",
            ],
        ),
        (
            "face",
            Moods.ro.Condițional,
            Tenses.ro.Perfect,
            [
                "eu aş fi făcut",
                "tu ai fi făcut",
                "el ar fi făcut",
                "ea ar fi făcut",
                "noi am fi făcut",
                "voi aţi fi făcut",
                "ei ar fi făcut",
                "ele ar fi făcut",
            ],
        ),
        (
            "face",
            Moods.ro.Indicativ,
            Tenses.ro.Viitor1Popular,
            [
                "eu o să fac",
                "tu o să faci",
                "el o să facă",
                "ea o să facă",
                "noi o să facem",
                "voi o să faceţi",
                "ei o să facă",
                "ele o să facă",
            ],
        ),
        (
            "face",
            Moods.ro.Indicativ,
            Tenses.ro.Viitor2Popular,
            [
                "eu am să fi făcut",
                "tu ai să fi făcut",
                "el are să fi făcut",
                "ea are să fi făcut",
                "noi avem să fi făcut",
                "voi aveţi să fi făcut",
                "ei au să fi făcut",
                "ele au să fi făcut",
            ],
        ),
        (
            "avea",
            Moods.ro.Conjunctiv,
            Tenses.ro.Prezent,
            [
                "eu să am",
                "tu să ai",
                "el să aibă",
                "ea să aibă",
                "noi să avem",
                "voi să aveţi",
                "ei să aibă",
                "ele să aibă",
            ],
        ),
        (
            "avea",
            Moods.ro.Condițional,
            Tenses.ro.Prezent,
            [
                "eu aş avea",
                "tu ai avea",
                "el ar avea",
                "ea ar avea",
                "noi am avea",
                "voi aţi avea",
                "ei ar avea",
                "ele ar avea",
            ],
        ),
        (
            "avea",
            Moods.ro.Condițional,
            Tenses.ro.Perfect,
            [
                "eu aş fi avut",
                "tu ai fi avut",
                "el ar fi avut",
                "ea ar fi avut",
                "noi am fi avut",
                "voi aţi fi avut",
                "ei ar fi avut",
                "ele ar fi avut",
            ],
        ),
    ],
)
def test_inflector_ro_conjugate_mood_tense_str_only(
    ccg: CompleteConjugator, infinitive: str, mood: Mood, tense: Tense, expected_result: list[str]
):
    tc = ccg.conjugate_mood_tense(infinitive, mood, tense)
    assert [c[0] for c in tc] == expected_result


@pytest.mark.parametrize(
    "infinitive,mood,tense,expected_result",
    [
        (
            "avea",
            Moods.ro.Participiu,
            Tenses.ro.Participiu,
            TenseConjugation(
                Tenses.ro.Participiu, [Conjugation(None, None, None, None, ["avut"])]
            ),
        ),
        (
            "face",
            Moods.ro.Participiu,
            Tenses.ro.Participiu,
            TenseConjugation(
                Tenses.ro.Participiu, [Conjugation(None, None, None, None, ["făcut"])]
            ),
        ),
        (
            "face",
            Moods.ro.Indicativ,
            Tenses.ro.PerfectCompus,
            TenseConjugation(
                Tenses.ro.PerfectCompus,
                [
                    Conjugation(
                        Person.First, Number.Singular, None, Pronouns.ro.eu, ["eu am făcut"]
                    ),
                    Conjugation(
                        Person.Second, Number.Singular, None, Pronouns.ro.tu, ["tu ai făcut"]
                    ),
                    Conjugation(
                        Person.Third, Number.Singular, Gender.m, Pronouns.ro.el, ["el a făcut"]
                    ),
                    Conjugation(
                        Person.Third, Number.Singular, Gender.f, Pronouns.ro.ea, ["ea a făcut"]
                    ),
                    Conjugation(
                        Person.First, Number.Plural, None, Pronouns.ro.noi, ["noi am făcut"]
                    ),
                    Conjugation(
                        Person.Second, Number.Plural, None, Pronouns.ro.voi, ["voi aţi făcut"]
                    ),
                    Conjugation(
                        Person.Third, Number.Plural, Gender.m, Pronouns.ro.ei, ["ei au făcut"]
                    ),
                    Conjugation(
                        Person.Third, Number.Plural, Gender.f, Pronouns.ro.ele, ["ele au făcut"]
                    ),
                ],
            ),
        ),
        (
            "face",
            Moods.ro.Indicativ,
            Tenses.ro.MaiMultCaPerfect,
            TenseConjugation(
                Tenses.ro.MaiMultCaPerfect,
                [
                    Conjugation(
                        Person.First, Number.Singular, None, Pronouns.ro.eu, ["eu făcusem"]
                    ),
                    Conjugation(
                        Person.Second, Number.Singular, None, Pronouns.ro.tu, ["tu făcuseși"]
                    ),
                    Conjugation(
                        Person.Third, Number.Singular, Gender.m, Pronouns.ro.el, ["el făcuse"]
                    ),
                    Conjugation(
                        Person.Third, Number.Singular, Gender.f, Pronouns.ro.ea, ["ea făcuse"]
                    ),
                    Conjugation(
                        Person.First,
                        Number.Plural,
                        None,
                        Pronouns.ro.noi,
                        ["noi făcuserăm"],
                    ),
                    Conjugation(
                        Person.Second,
                        Number.Plural,
                        None,
                        Pronouns.ro.voi,
                        ["voi făcuserăţi"],
                    ),
                    Conjugation(
                        Person.Third, Number.Plural, Gender.m, Pronouns.ro.ei, ["ei făcuseră"]
                    ),
                    Conjugation(
                        Person.Third, Number.Plural, Gender.f, Pronouns.ro.ele, ["ele făcuseră"]
                    ),
                ],
            ),
        ),
        (
            Pronouns.ro.voi,
            Moods.ro.Indicativ,
            Tenses.ro.Prezent,
            TenseConjugation(
                Tenses.ro.Prezent,
                [
                    Conjugation(
                        Person.First,
                        Number.Singular,
                        None,
                        Pronouns.ro.eu,
                        ["eu voiesc", "eu voi"],
                    ),
                    Conjugation(
                        Person.Second,
                        Number.Singular,
                        None,
                        Pronouns.ro.tu,
                        ["tu voiești", "tu vei"],
                    ),
                    Conjugation(
                        Person.Third,
                        Number.Singular,
                        Gender.m,
                        Pronouns.ro.el,
                        ["el voiește", "el va"],
                    ),
                    Conjugation(
                        Person.Third,
                        Number.Singular,
                        Gender.f,
                        Pronouns.ro.ea,
                        ["ea voiește", "ea va"],
                    ),
                    Conjugation(
                        Person.First,
                        Number.Plural,
                        None,
                        Pronouns.ro.noi,
                        ["noi voim", "noi vom"],
                    ),
                    Conjugation(
                        Person.Second,
                        Number.Plural,
                        None,
                        Pronouns.ro.voi,
                        ["voi voiţi", "voi veţi"],
                    ),
                    Conjugation(
                        Person.Third,
                        Number.Plural,
                        Gender.m,
                        Pronouns.ro.ei,
                        ["ei voiesc", "ei vor"],
                    ),
                    Conjugation(
                        Person.Third,
                        Number.Plural,
                        Gender.f,
                        Pronouns.ro.ele,
                        ["ele voiesc", "ele vor"],
                    ),
                ],
            ),
        ),
        (
            "avea",
            Moods.ro.Indicativ,
            Tenses.ro.Prezent,
            TenseConjugation(
                Tenses.ro.Prezent,
                [
                    Conjugation(Person.First, Number.Singular, None, Pronouns.ro.eu, ["eu am"]),
                    Conjugation(Person.Second, Number.Singular, None, Pronouns.ro.tu, ["tu ai"]),
                    Conjugation(
                        Person.Third,
                        Number.Singular,
                        Gender.m,
                        Pronouns.ro.el,
                        ["el a", "el are"],
                    ),
                    Conjugation(
                        Person.Third,
                        Number.Singular,
                        Gender.f,
                        Pronouns.ro.ea,
                        ["ea a", "ea are"],
                    ),
                    Conjugation(
                        Person.First,
                        Number.Plural,
                        None,
                        Pronouns.ro.noi,
                        ["noi am", "noi avem"],
                    ),
                    Conjugation(
                        Person.Second,
                        Number.Plural,
                        None,
                        Pronouns.ro.voi,
                        ["voi aţi", "voi aveţi"],
                    ),
                    Conjugation(Person.Third, Number.Plural, Gender.m, Pronouns.ro.ei, ["ei au"]),
                    Conjugation(
                        Person.Third, Number.Plural, Gender.f, Pronouns.ro.ele, ["ele au"]
                    ),
                ],
            ),
        ),
        (
            "avea",
            Moods.ro.Indicativ,
            Tenses.ro.Imperfect,
            TenseConjugation(
                Tenses.ro.Imperfect,
                [
                    Conjugation(
                        Person.First, Number.Singular, None, Pronouns.ro.eu, ["eu aveam"]
                    ),
                    Conjugation(
                        Person.Second, Number.Singular, None, Pronouns.ro.tu, ["tu aveai"]
                    ),
                    Conjugation(
                        Person.Third, Number.Singular, Gender.m, Pronouns.ro.el, ["el avea"]
                    ),
                    Conjugation(
                        Person.Third, Number.Singular, Gender.f, Pronouns.ro.ea, ["ea avea"]
                    ),
                    Conjugation(
                        Person.First, Number.Plural, None, Pronouns.ro.noi, ["noi aveam"]
                    ),
                    Conjugation(
                        Person.Second, Number.Plural, None, Pronouns.ro.voi, ["voi aveaţi"]
                    ),
                    Conjugation(
                        Person.Third, Number.Plural, Gender.m, Pronouns.ro.ei, ["ei aveau"]
                    ),
                    Conjugation(
                        Person.Third, Number.Plural, Gender.f, Pronouns.ro.ele, ["ele aveau"]
                    ),
                ],
            ),
        ),
    ],
)
def test_inflector_ro_conjugate_mood_tense_tc(
    ccg: CompleteConjugator, infinitive: str, mood: Mood, tense: Tense, expected_result: TenseConjugation
):
    tc = ccg.conjugate_mood_tense(infinitive, mood, tense)
    assert tc == expected_result


def test_inflector_ro_conjugate_mood_tense_viitor_1(ccg: CompleteConjugator):
    assert ccg.conjugate_mood_tense(
        "face",
        Moods.ro.Indicativ,
        Tenses.ro.Viitor1,
    ) == TenseConjugation(
        Tenses.ro.Viitor1,
        [
            Conjugation(Person.First, Number.Singular, None, Pronouns.ro.eu, ["eu voi face"]),
            Conjugation(Person.Second, Number.Singular, None, Pronouns.ro.tu, ["tu vei face"]),
            Conjugation(Person.Third, Number.Singular, Gender.m, Pronouns.ro.el, ["el va face"]),
            Conjugation(Person.Third, Number.Singular, Gender.f, Pronouns.ro.ea, ["ea va face"]),
            Conjugation(Person.First, Number.Plural, None, Pronouns.ro.noi, ["noi vom face"]),
            Conjugation(Person.Second, Number.Plural, None, Pronouns.ro.voi, ["voi veţi face"]),
            Conjugation(Person.Third, Number.Plural, Gender.m, Pronouns.ro.ei, ["ei vor face"]),
            Conjugation(Person.Third, Number.Plural, Gender.f, Pronouns.ro.ele, ["ele vor face"]),
        ],
    )


def test_inflector_ro_conjugate_mood_tense_viitor_1_popular(ccg: CompleteConjugator):
    tc = ccg.conjugate_mood_tense(
        "face",
        Moods.ro.Indicativ,
        Tenses.ro.Viitor1Popular,
    )
    assert tc == TenseConjugation(
        Tenses.ro.Viitor1Popular,
        [
            Conjugation(Person.First, Number.Singular, None, Pronouns.ro.eu, ["eu o să fac"]),
            Conjugation(Person.Second, Number.Singular, None, Pronouns.ro.tu, ["tu o să faci"]),
            Conjugation(
                Person.Third, Number.Singular, Gender.m, Pronouns.ro.el, ["el o să facă"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.f, Pronouns.ro.ea, ["ea o să facă"]
            ),
            Conjugation(Person.First, Number.Plural, None, Pronouns.ro.noi, ["noi o să facem"]),
            Conjugation(Person.Second, Number.Plural, None, Pronouns.ro.voi, ["voi o să faceţi"]),
            Conjugation(Person.Third, Number.Plural, Gender.m, Pronouns.ro.ei, ["ei o să facă"]),
            Conjugation(
                Person.Third, Number.Plural, Gender.f, Pronouns.ro.ele, ["ele o să facă"]
            ),
        ],
    )


def test_inflector_ro_conjugate_mood_tense_condițional_perfect(ccg: CompleteConjugator):
    tc = ccg.conjugate_mood_tense("avea", Moods.ro.Condițional, Tenses.ro.Perfect)
    assert [c[0] for c in tc] == [
        "eu aş fi avut",
        "tu ai fi avut",
        "el ar fi avut",
        "ea ar fi avut",
        "noi am fi avut",
        "voi aţi fi avut",
        "ei ar fi avut",
        "ele ar fi avut",
    ]


def test_inflector_ro_conjugate_mood_tense_conjunctiv_perfect(ccg: CompleteConjugator):
    tc = ccg.conjugate_mood_tense(
        "face",
        Moods.ro.Conjunctiv,
        Tenses.ro.Perfect,
    )
    assert [c[0] for c in tc] == [
        "eu să fi făcut",
        "tu să fi făcut",
        "el să fi făcut",
        "ea să fi făcut",
        "noi să fi făcut",
        "voi să fi făcut",
        "ei să fi făcut",
        "ele să fi făcut",
    ]


@pytest.mark.parametrize(
    "person,number,gender,is_reflexive,expected_result",
    [
        (Person.First, Number.Singular, Gender.m, False, Pronouns.ro.eu),
        (Person.First, Number.Singular, Gender.m, True, "eu mă"),
        (Person.Second, Number.Singular, Gender.m, False, Pronouns.ro.tu),
        (Person.Second, Number.Singular, Gender.m, True, "tu te"),
        (Person.Third, Number.Singular, Gender.m, False, Pronouns.ro.el),
        (Person.Third, Number.Singular, Gender.m, True, "el se"),
        (Person.Third, Number.Singular, Gender.f, False, "ea"),
        (Person.Third, Number.Singular, Gender.f, True, "ea se"),
        (Person.First, Number.Plural, Gender.m, False, "noi"),
        (Person.First, Number.Plural, Gender.m, True, "noi ne"),
        (Person.Second, Number.Plural, Gender.m, False, "voi"),
        (Person.Second, Number.Plural, Gender.m, True, "voi vă"),
        (Person.Third, Number.Plural, Gender.m, False, Pronouns.ro.ei),
        (Person.Third, Number.Plural, Gender.m, True, "ei se"),
        (Person.Third, Number.Plural, Gender.f, False, Pronouns.ro.ele),
        (Person.Third, Number.Plural, Gender.f, True, "ele se"),
    ],
)
def test_inflector_ro_get_pronouns(
    ccg: CompleteConjugator,
    person: Person,
    number: Number,
    gender: Gender,
    is_reflexive: bool,
    expected_result: str,
):
    pronoun = ccg.private_get_inflector().get_pronouns(person, number, gender)[0]
    if is_reflexive:
        pronoun = ccg.private_get_inflector().make_pronoun_reflexive(pronoun)
    assert pronoun == expected_result
