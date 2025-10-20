import pytest

from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.person import Person
from verbecc.src.conjugator.conjugator import Conjugator
from verbecc.src.defs.types.alternates_behavior import AlternatesBehavior


@pytest.fixture(scope="module")
def cg():
    cg = Conjugator(lang="ro")
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
    "infinitive,mood,tense,alternates_behavior,expected_result",
    [
        ("avea", "participiu", "participiu", AlternatesBehavior.FirstOnly, ["avut"]),
        ("face", "participiu", "participiu", AlternatesBehavior.FirstOnly, ["făcut"]),
        (
            "avea",
            "indicativ",
            "prezent",
            AlternatesBehavior.FirstOnly,
            ["eu am", "tu ai", "el a", "noi am", "voi aţi", "ei au"],
        ),
        (
            "avea",
            "indicativ",
            "prezent",
            AlternatesBehavior.SecondOnly,
            ["eu am", "tu ai", "el are", "noi avem", "voi aveţi", "ei au"],
        ),
        (
            "avea",
            "indicativ",
            "imperfect",
            AlternatesBehavior.FirstOnly,
            ["eu aveam", "tu aveai", "el avea", "noi aveam", "voi aveaţi", "ei aveau"],
        ),
        (
            "avea",
            "indicativ",
            "perfect-simplu",
            AlternatesBehavior.FirstOnly,
            ["eu avui", "tu avuși", "el avu", "noi avurăm", "voi avurăţi", "ei avură"],
        ),
        (
            "avea",
            "indicativ",
            "perfect-compus",
            AlternatesBehavior.FirstOnly,
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
            "indicativ",
            "mai-mult-ca-perfect",
            AlternatesBehavior.FirstOnly,
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
            "indicativ",
            "prezent",
            AlternatesBehavior.FirstOnly,
            ["eu fac", "tu faci", "el face", "noi facem", "voi faceţi", "ei fac"],
        ),
        (
            "face",
            "indicativ",
            "imperfect",
            AlternatesBehavior.FirstOnly,
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
            "indicativ",
            "perfect-simplu",
            AlternatesBehavior.FirstOnly,
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
            "indicativ",
            "perfect-compus",
            AlternatesBehavior.FirstOnly,
            [
                "eu am făcut",
                "tu ai făcut",
                "el a făcut",
                "noi am făcut",
                "voi aţi făcut",
                "ei au făcut",
            ],
        ),
        (
            "face",
            "indicativ",
            "mai-mult-ca-perfect",
            AlternatesBehavior.FirstOnly,
            [
                "eu făcusem",
                "tu făcuseși",
                "el făcuse",
                "noi făcuserăm",
                "voi făcuserăţi",
                "ei făcuseră",
            ],
        ),
        (
            "voi",
            "indicativ",
            "prezent",
            AlternatesBehavior.FirstOnly,
            [
                "eu voiesc",
                "tu voiești",
                "el voiește",
                "noi voim",
                "voi voiţi",
                "ei voiesc",
            ],
        ),
        (
            "voi",
            "indicativ",
            "prezent",
            AlternatesBehavior.SecondOnly,
            ["eu voi", "tu vei", "el va", "noi vom", "voi veţi", "ei vor"],
        ),
        (
            "face",
            "indicativ",
            "viitor-1",
            AlternatesBehavior.FirstOnly,
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
            "indicativ",
            "viitor-2",
            AlternatesBehavior.FirstOnly,
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
            "prezent",
            AlternatesBehavior.FirstOnly,
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
            AlternatesBehavior.FirstOnly,
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
            "indicativ",
            "viitor-1-popular",
            AlternatesBehavior.FirstOnly,
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
            "indicativ",
            "viitor-2-popular",
            AlternatesBehavior.FirstOnly,
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
            "prezent",
            AlternatesBehavior.FirstOnly,
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
            "prezent",
            AlternatesBehavior.FirstOnly,
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
            AlternatesBehavior.FirstOnly,
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
        "face", "indicativ", "viitor-1", AlternatesBehavior.FirstOnly
    ) == [
        "eu voi face",
        "tu vei face",
        "el va face",
        "noi vom face",
        "voi veţi face",
        "ei vor face",
    ]


def test_inflector_ro_conjugate_mood_tense_viitor_1_popular(cg):
    assert cg.conjugate_mood_tense(
        "face",
        "indicativ",
        "viitor-1-popular",
        AlternatesBehavior.FirstOnly,
        [
            "eu o să fac",
            "tu o să faci",
            "el o să facă",
            "noi o să facem",
            "voi o să faceţi",
            "ei o să facă",
        ],
    )


def test_inflector_ro_conjugate_mood_tense_condițional_perfect(cg):
    assert cg.conjugate_mood_tense(
        "avea", "condițional", "perfect", AlternatesBehavior.FirstOnly
    ) == [
        "eu aş fi avut",
        "tu ai fi avut",
        "el ar fi avut",
        "noi am fi avut",
        "voi aţi fi avut",
        "ei ar fi avut",
    ]


def test_inflector_ro_conjugate_mood_tense_conjunctiv_perfect(cg):
    assert cg.conjugate_mood_tense(
        "face", "conjunctiv", "perfect", AlternatesBehavior.FirstOnly
    ) == [
        "eu să fi făcut",
        "tu să fi făcut",
        "el să fi făcut",
        "noi să fi făcut",
        "voi să fi făcut",
        "ei să fi făcut",
    ]


@pytest.mark.parametrize(
    "person,gender,is_reflexive,expected_result",
    [
        (Person.FirstPersonSingular, Gender.M, False, "eu"),
        (Person.FirstPersonSingular, Gender.M, True, "eu mă"),
        (Person.SecondPersonSingular, Gender.M, False, "tu"),
        (Person.SecondPersonSingular, Gender.M, True, "tu te"),
        (Person.ThirdPersonSingular, Gender.M, False, "el"),
        (Person.ThirdPersonSingular, Gender.M, True, "el se"),
        (Person.ThirdPersonSingular, Gender.F, False, "ea"),
        (Person.ThirdPersonSingular, Gender.F, True, "ea se"),
        (Person.FirstPersonPlural, Gender.M, False, "noi"),
        (Person.FirstPersonPlural, Gender.M, True, "noi ne"),
        (Person.SecondPersonPlural, Gender.M, False, "voi"),
        (Person.SecondPersonPlural, Gender.M, True, "voi vă"),
        (Person.ThirdPersonPlural, Gender.M, False, "ei"),
        (Person.ThirdPersonPlural, Gender.M, True, "ei se"),
        (Person.ThirdPersonPlural, Gender.F, False, "ele"),
        (Person.ThirdPersonPlural, Gender.F, True, "ele se"),
    ],
)
def test_inflector_ro_get_default_pronoun(
    cg, person: Person, gender: Gender, is_reflexive: bool, expected_result: str
):
    assert (
        cg._inflector._get_default_pronoun(person, gender, is_reflexive=is_reflexive)
        == expected_result
    )
