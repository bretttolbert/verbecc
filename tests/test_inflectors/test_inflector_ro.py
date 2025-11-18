import pytest

from verbecc.src.conjugator.conjugator import Conjugator
from verbecc.src.defs.types.conjugation import Conjugation
from verbecc.src.defs.types.conjugation import TenseConjugation
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.src.defs.types.mood import Moods
from verbecc.src.defs.types.number import Number
from verbecc.src.defs.types.person import Person
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
    cg, infinitive, mood, tense, expected_result
):
    tc = cg.conjugate_mood_tense(infinitive, mood, tense)
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
                        Person.First, Number.Singular, None, "eu", ["eu am făcut"]
                    ),
                    Conjugation(
                        Person.Second, Number.Singular, None, "tu", ["tu ai făcut"]
                    ),
                    Conjugation(
                        Person.Third, Number.Singular, Gender.m, "el", ["el a făcut"]
                    ),
                    Conjugation(
                        Person.Third, Number.Singular, Gender.f, "ea", ["ea a făcut"]
                    ),
                    Conjugation(
                        Person.First, Number.Plural, None, "noi", ["noi am făcut"]
                    ),
                    Conjugation(
                        Person.Second, Number.Plural, None, "voi", ["voi aţi făcut"]
                    ),
                    Conjugation(
                        Person.Third, Number.Plural, Gender.m, "ei", ["ei au făcut"]
                    ),
                    Conjugation(
                        Person.Third, Number.Plural, Gender.f, "ele", ["ele au făcut"]
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
                        Person.First, Number.Singular, None, "eu", ["eu făcusem"]
                    ),
                    Conjugation(
                        Person.Second, Number.Singular, None, "tu", ["tu făcuseși"]
                    ),
                    Conjugation(
                        Person.Third, Number.Singular, Gender.m, "el", ["el făcuse"]
                    ),
                    Conjugation(
                        Person.Third, Number.Singular, Gender.f, "ea", ["ea făcuse"]
                    ),
                    Conjugation(
                        Person.First,
                        Number.Plural,
                        None,
                        "noi",
                        ["noi făcuserăm"],
                    ),
                    Conjugation(
                        Person.Second,
                        Number.Plural,
                        None,
                        "voi",
                        ["voi făcuserăţi"],
                    ),
                    Conjugation(
                        Person.Third, Number.Plural, Gender.m, "ei", ["ei făcuseră"]
                    ),
                    Conjugation(
                        Person.Third, Number.Plural, Gender.f, "ele", ["ele făcuseră"]
                    ),
                ],
            ),
        ),
        (
            "voi",
            Moods.ro.Indicativ,
            Tenses.ro.Prezent,
            TenseConjugation(
                Tenses.ro.Prezent,
                [
                    Conjugation(
                        Person.First,
                        Number.Singular,
                        None,
                        "eu",
                        ["eu voiesc", "eu voi"],
                    ),
                    Conjugation(
                        Person.Second,
                        Number.Singular,
                        None,
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
                        Person.Third,
                        Number.Singular,
                        Gender.f,
                        "ea",
                        ["ea voiește", "ea va"],
                    ),
                    Conjugation(
                        Person.First,
                        Number.Plural,
                        None,
                        "noi",
                        ["noi voim", "noi vom"],
                    ),
                    Conjugation(
                        Person.Second,
                        Number.Plural,
                        None,
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
                    Conjugation(
                        Person.Third,
                        Number.Plural,
                        Gender.f,
                        "ele",
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
                    Conjugation(Person.First, Number.Singular, None, "eu", ["eu am"]),
                    Conjugation(Person.Second, Number.Singular, None, "tu", ["tu ai"]),
                    Conjugation(
                        Person.Third,
                        Number.Singular,
                        Gender.m,
                        "el",
                        ["el a", "el are"],
                    ),
                    Conjugation(
                        Person.Third,
                        Number.Singular,
                        Gender.f,
                        "ea",
                        ["ea a", "ea are"],
                    ),
                    Conjugation(
                        Person.First,
                        Number.Plural,
                        None,
                        "noi",
                        ["noi am", "noi avem"],
                    ),
                    Conjugation(
                        Person.Second,
                        Number.Plural,
                        None,
                        "voi",
                        ["voi aţi", "voi aveţi"],
                    ),
                    Conjugation(Person.Third, Number.Plural, Gender.m, "ei", ["ei au"]),
                    Conjugation(
                        Person.Third, Number.Plural, Gender.f, "ele", ["ele au"]
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
                        Person.First, Number.Singular, None, "eu", ["eu aveam"]
                    ),
                    Conjugation(
                        Person.Second, Number.Singular, None, "tu", ["tu aveai"]
                    ),
                    Conjugation(
                        Person.Third, Number.Singular, Gender.m, "el", ["el avea"]
                    ),
                    Conjugation(
                        Person.Third, Number.Singular, Gender.f, "ea", ["ea avea"]
                    ),
                    Conjugation(
                        Person.First, Number.Plural, None, "noi", ["noi aveam"]
                    ),
                    Conjugation(
                        Person.Second, Number.Plural, None, "voi", ["voi aveaţi"]
                    ),
                    Conjugation(
                        Person.Third, Number.Plural, Gender.m, "ei", ["ei aveau"]
                    ),
                    Conjugation(
                        Person.Third, Number.Plural, Gender.f, "ele", ["ele aveau"]
                    ),
                ],
            ),
        ),
    ],
)
def test_inflector_ro_conjugate_mood_tense_tc(
    cg, infinitive, mood, tense, expected_result
):
    tc = cg.conjugate_mood_tense(infinitive, mood, tense)
    assert tc == expected_result


def test_inflector_ro_conjugate_mood_tense_viitor_1(cg):
    assert cg.conjugate_mood_tense(
        "face",
        Moods.ro.Indicativ,
        Tenses.ro.Viitor1,
    ) == TenseConjugation(
        Tenses.ro.Viitor1,
        [
            Conjugation(Person.First, Number.Singular, None, "eu", ["eu voi face"]),
            Conjugation(Person.Second, Number.Singular, None, "tu", ["tu vei face"]),
            Conjugation(Person.Third, Number.Singular, Gender.m, "el", ["el va face"]),
            Conjugation(Person.Third, Number.Singular, Gender.f, "ea", ["ea va face"]),
            Conjugation(Person.First, Number.Plural, None, "noi", ["noi vom face"]),
            Conjugation(Person.Second, Number.Plural, None, "voi", ["voi veţi face"]),
            Conjugation(Person.Third, Number.Plural, Gender.m, "ei", ["ei vor face"]),
            Conjugation(Person.Third, Number.Plural, Gender.f, "ele", ["ele vor face"]),
        ],
    )


def test_inflector_ro_conjugate_mood_tense_viitor_1_popular(cg):
    tc = cg.conjugate_mood_tense(
        "face",
        Moods.ro.Indicativ,
        Tenses.ro.Viitor1Popular,
    )
    assert tc == TenseConjugation(
        Tenses.ro.Viitor1Popular,
        [
            Conjugation(Person.First, Number.Singular, None, "eu", ["eu o să fac"]),
            Conjugation(Person.Second, Number.Singular, None, "tu", ["tu o să faci"]),
            Conjugation(
                Person.Third, Number.Singular, Gender.m, "el", ["el o să facă"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.f, "ea", ["ea o să facă"]
            ),
            Conjugation(Person.First, Number.Plural, None, "noi", ["noi o să facem"]),
            Conjugation(Person.Second, Number.Plural, None, "voi", ["voi o să faceţi"]),
            Conjugation(Person.Third, Number.Plural, Gender.m, "ei", ["ei o să facă"]),
            Conjugation(
                Person.Third, Number.Plural, Gender.f, "ele", ["ele o să facă"]
            ),
        ],
    )


def test_inflector_ro_conjugate_mood_tense_condițional_perfect(cg):
    tc = cg.conjugate_mood_tense("avea", Moods.ro.Condițional, Tenses.ro.Perfect)
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


def test_inflector_ro_conjugate_mood_tense_conjunctiv_perfect(cg):
    tc = cg.conjugate_mood_tense(
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
