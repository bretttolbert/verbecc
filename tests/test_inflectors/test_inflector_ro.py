import pytest

from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.src.conjugator.conjugator import Conjugator
from verbecc.src.defs.types.conjugation import (
    TenseConjugation,
    Conjugation,
)
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.number import Number
from verbecc.src.defs.types.mood import Moods
from verbecc.src.defs.types.tense import Tenses


@pytest.fixture(scope="module")
def cg():
    cg = Conjugator(lang=Lang.ro)
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
            "avea",
            Moods.ro.Participiu,
            Tenses.ro.Participiu,
            TenseConjugation([Conjugation(None, None, None, None, ["avut"])]),
        ),
        (
            "face",
            Moods.ro.Participiu,
            Tenses.ro.Participiu,
            TenseConjugation([Conjugation(None, None, None, None, ["făcut"])]),
        ),
        (
            "avea",
            Moods.ro.Indicativ,
            Tenses.ro.Prezent,
            TenseConjugation(
                [
                    Conjugation(
                        Person.First, Number.Singular, Gender.m, "eu", ["eu am"]
                    ),
                    Conjugation(
                        Person.First, Number.Singular, Gender.m, "tu", ["tu ai"]
                    ),
                    Conjugation(
                        Person.First, Number.Singular, Gender.m, "el", ["el a"]
                    ),
                    Conjugation(
                        Person.First, Number.Plural, Gender.m, "noi", ["noi am"]
                    ),
                    Conjugation(
                        Person.Second, Number.Plural, Gender.m, "voi", ["voi aţi"]
                    ),
                    Conjugation(Person.Third, Number.Plural, Gender.m, "ei", ["ei au"]),
                ]
            ),
        ),
        (
            "avea",
            Moods.ro.Indicativ,
            Tenses.ro.Prezent,
            TenseConjugation(
                [
                    Conjugation(
                        Person.First, Number.Singular, Gender.m, "eu", ["eu am"]
                    ),
                    Conjugation(
                        Person.Second, Number.Singular, Gender.m, "tu", ["tu ai"]
                    ),
                    Conjugation(
                        Person.Third, Number.Singular, Gender.m, "el", ["el are"]
                    ),
                    Conjugation(
                        Person.First, Number.Plural, Gender.m, "noi", ["noi avem"]
                    ),
                    Conjugation(
                        Person.Second, Number.Plural, Gender.m, "voi", ["voi aveţi"]
                    ),
                    Conjugation(Person.Third, Number.Plural, Gender.m, "ei", ["ei au"]),
                ]
            ),
        ),
        (
            "avea",
            Moods.ro.Indicativ,
            Tenses.ro.Imperfect,
            ["eu aveam", "tu aveai", "el avea", "noi aveam", "voi aveaţi", "ei aveau"],
        ),
        (
            "avea",
            Moods.ro.Indicativ,
            Tenses.ro.PerfectSimplu,
            ["eu avui", "tu avuși", "el avu", "noi avurăm", "voi avurăţi", "ei avură"],
        ),
        (
            "avea",
            Moods.ro.Indicativ,
            Tenses.ro.PerfectCompus,
            [
                "eu am avut",
                "tu ai avut",
                "el a avut",
                "noi am avut",
                "voi aţi avut",
                "ei au avut",
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
                "noi avuserăm",
                "voi avuserăţi",
                "ei avuseră",
            ],
        ),
        (
            "face",
            Moods.ro.Indicativ,
            Tenses.ro.Prezent,
            ["eu fac", "tu faci", "el face", "noi facem", "voi faceţi", "ei fac"],
        ),
        (
            "face",
            Moods.ro.Indicativ,
            Tenses.ro.Imperfect,
            [
                "eu făceam",
                "tu făceai",
                "el făcea",
                "noi făceam",
                "voi făceaţi",
                "ei făceau",
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
                "noi făcurăm",
                "voi făcurăţi",
                "ei făcură",
            ],
        ),
        (
            "face",
            Moods.ro.Indicativ,
            Tenses.ro.PerfectCompus,
            TenseConjugation(
                [
                    Conjugation(
                        Person.First, Number.Singular, Gender.m, "eu", ["eu am făcut"]
                    ),
                    Conjugation(
                        Person.Second, Number.Singular, Gender.m, "tu", ["tu ai făcut"]
                    ),
                    Conjugation(
                        Person.Third, Number.Singular, Gender.m, "el", ["el a făcut"]
                    ),
                    Conjugation(
                        Person.First, Number.Plural, Gender.m, "noi", ["noi am făcut"]
                    ),
                    Conjugation(
                        Person.Second, Number.Plural, Gender.m, "voi", ["voi aţi făcut"]
                    ),
                    Conjugation(
                        Person.Third, Number.Plural, Gender.m, "ei", ["ei au făcut"]
                    ),
                ]
            ),
        ),
        (
            "face",
            Moods.ro.Indicativ,
            Tenses.ro.MaiMultCaPerfect,
            TenseConjugation(
                [
                    Conjugation(
                        Person.First, Number.Singular, Gender.m, "eu", ["eu făcusem"]
                    ),
                    Conjugation(
                        Person.Second, Number.Singular, Gender.m, "tu", ["tu făcuseși"]
                    ),
                    Conjugation(
                        Person.Third, Number.Singular, Gender.m, "el", ["el făcuse"]
                    ),
                    Conjugation(
                        Person.First,
                        Number.Singular,
                        Gender.m,
                        "noi",
                        ["noi făcuserăm"],
                    ),
                    Conjugation(
                        Person.Second,
                        Number.Plural,
                        Gender.m,
                        "voi",
                        ["voi făcuserăţi"],
                    ),
                    Conjugation(
                        Person.Third, Number.Plural, Gender.m, "ei", ["ei făcuseră"]
                    ),
                ]
            ),
        ),
        (
            "voi",
            Moods.ro.Indicativ,
            Tenses.ro.Prezent,
            TenseConjugation(
                [
                    Conjugation(
                        Person.First,
                        Number.Singular,
                        Gender.m,
                        "eu",
                        ["eu voiesc", "eu voi"],
                    ),
                    Conjugation(
                        Person.Second,
                        Number.Singular,
                        Gender.m,
                        "tu",
                        ["tu voiești", "tu vei"],
                    ),
                    Conjugation(
                        Person.Third,
                        Number.Singular,
                        Gender.m,
                        "el",
                        ["el voiește", "el va"],
                    ),
                    Conjugation(
                        Person.First,
                        Number.Plural,
                        Gender.m,
                        "noi",
                        ["noi voim", "noi vom"],
                    ),
                    Conjugation(
                        Person.Second,
                        Number.Plural,
                        Gender.m,
                        "voi",
                        ["voi voiţi", "voi veţi"],
                    ),
                    Conjugation(
                        Person.Third,
                        Number.Plural,
                        Gender.m,
                        "ei",
                        ["ei voiesc", "ei vor"],
                    ),
                ]
            ),
        ),
        (
            "face",
            Moods.ro.Indicativ,
            Tenses.ro.Viitor1,
            [
                "eu voi face",
                "tu vei face",
                "el va face",
                "noi vom face",
                "voi veţi face",
                "ei vor face",
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
                "noi vom fi făcut",
                "voi veţi fi făcut",
                "ei vor fi făcut",
            ],
        ),
        (
            "face",
            "conjunctiv",
            Tenses.ro.Prezent,
            [
                "eu să fac",
                "tu să faci",
                "el să facă",
                "noi să facem",
                "voi să faceţi",
                "ei să facă",
            ],
        ),
        (
            "face",
            "conjunctiv",
            "perfect",
            [
                "eu să fi făcut",
                "tu să fi făcut",
                "el să fi făcut",
                "noi să fi făcut",
                "voi să fi făcut",
                "ei să fi făcut",
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
                "noi o să facem",
                "voi o să faceţi",
                "ei o să facă",
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
                "noi avem să fi făcut",
                "voi aveţi să fi făcut",
                "ei au să fi făcut",
            ],
        ),
        (
            "avea",
            "conjunctiv",
            Tenses.ro.Prezent,
            [
                "eu să am",
                "tu să ai",
                "el să aibă",
                "noi să avem",
                "voi să aveţi",
                "ei să aibă",
            ],
        ),
        (
            "avea",
            "condițional",
            Tenses.ro.Prezent,
            [
                "eu aş avea",
                "tu ai avea",
                "el ar avea",
                "noi am avea",
                "voi aţi avea",
                "ei ar avea",
            ],
        ),
        (
            "avea",
            "condițional",
            "perfect",
            [
                "eu aş fi avut",
                "tu ai fi avut",
                "el ar fi avut",
                "noi am fi avut",
                "voi aţi fi avut",
                "ei ar fi avut",
            ],
        ),
    ],
)
def test_inflector_ro_conjugate_mood_tense(
    cg, infinitive, mood, tense, alternates_behavior, expected_result
):
    assert (
        cg.conjugate_mood_tense(infinitive, mood, tense, alternates_behavior)
        == expected_result
    )


def test_inflector_ro_conjugate_mood_tense_viitor_1(cg):
    assert cg.conjugate_mood_tense(
        "face",
        Moods.ro.Indicativ,
        Tenses.ro.Viitor1,
    ) == TenseConjugation(
        [
            Conjugation(Person.First, Number.Singular, Gender.m, "eu", ["eu voi face"]),
            Conjugation(
                Person.Second, Number.Singular, Gender.m, "tu", ["tu vei face"]
            ),
            Conjugation(Person.Third, Number.Singular, Gender.m, "el", ["el va face"]),
            Conjugation(Person.First, Number.Plural, Gender.m, "noi", ["noi vom face"]),
            Conjugation(
                Person.Second, Number.Plural, Gender.m, "voi", ["voi veţi face"]
            ),
            Conjugation(Person.Third, Number.Plural, Gender.m, "ei", ["ei vor face"]),
        ]
    )


def test_inflector_ro_conjugate_mood_tense_viitor_1_popular(cg):
    assert cg.conjugate_mood_tense(
        "face",
        Moods.ro.Indicativ,
        Tenses.ro.Viitor1Popular,
        TenseConjugation(
            [
                Conjugation(
                    Person.First, Number.Singular, Gender.m, "eu", ["eu o să fac"]
                ),
                Conjugation(
                    Person.Second, Number.Singular, Gender.m, "tu", ["tu o să faci"]
                ),
                Conjugation(
                    Person.Third, Number.Singular, Gender.m, "el", ["el o să facă"]
                ),
                Conjugation(
                    Person.First, Number.Plural, Gender.m, "noi", ["noi o să facem"]
                ),
                Conjugation(
                    Person.Second, Number.Plural, Gender.m, "voi", ["voi o să faceţi"]
                ),
                Conjugation(
                    Person.Third, Number.Plural, Gender.m, "ei", ["ei o să facă"]
                ),
            ]
        ),
    )


def test_inflector_ro_conjugate_mood_tense_condițional_perfect(cg):
    assert cg.conjugate_mood_tense("avea", Moods.ro.Condițional, Tenses.ro.Perfect) == [
        "eu aş fi avut",
        "tu ai fi avut",
        "el ar fi avut",
        "noi am fi avut",
        "voi aţi fi avut",
        "ei ar fi avut",
    ]


def test_inflector_ro_conjugate_mood_tense_conjunctiv_perfect(cg):
    assert cg.conjugate_mood_tense(
        "face",
        "conjunctiv",
        "perfect",
    ) == [
        "eu să fi făcut",
        "tu să fi făcut",
        "el să fi făcut",
        "noi să fi făcut",
        "voi să fi făcut",
        "ei să fi făcut",
    ]


@pytest.mark.parametrize(
    "person,number,gender,is_reflexive,expected_result",
    [
        (Person.First, Number.Singular, Gender.m, False, "eu"),
        (Person.First, Number.Singular, Gender.m, True, "eu mă"),
        (Person.Second, Number.Singular, Gender.m, False, "tu"),
        (Person.Second, Number.Singular, Gender.m, True, "tu te"),
        (Person.Third, Number.Singular, Gender.m, False, "el"),
        (Person.Third, Number.Singular, Gender.m, True, "el se"),
        (Person.Third, Number.Singular, Gender.f, False, "ea"),
        (Person.Third, Number.Singular, Gender.f, True, "ea se"),
        (Person.First, Number.Plural, Gender.m, False, "noi"),
        (Person.First, Number.Plural, Gender.m, True, "noi ne"),
        (Person.Second, Number.Plural, Gender.m, False, "voi"),
        (Person.Second, Number.Plural, Gender.m, True, "voi vă"),
        (Person.Third, Number.Plural, Gender.m, False, "ei"),
        (Person.Third, Number.Plural, Gender.m, True, "ei se"),
        (Person.Third, Number.Plural, Gender.f, False, "ele"),
        (Person.Third, Number.Plural, Gender.f, True, "ele se"),
    ],
)
def test_inflector_ro_get_pronouns(
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
