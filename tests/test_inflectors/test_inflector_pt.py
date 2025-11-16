import pytest
from typing import List

from verbecc.src.conjugator.conjugator import Conjugator
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.src.defs.types.mood import Mood
from verbecc.src.defs.types.number import Number
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.tense import Tense


@pytest.fixture(scope="module")
def cg():
    cg = Conjugator(lang=Lang.pt)
    yield cg


def test_all_verbs_have_templates(cg: Conjugator):
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
            "ter",
            "indicativo",
            "presente",
            [
                "eu tenho",
                "tu tens",
                "ele tem",
                "ela tem",
                "nós temos",
                "vós tendes",
                "eles têm",
                "elas têm",
            ],
        ),
        (
            "ter",
            "indicativo",
            "pretérito-perfeito",
            [
                "eu tive",
                "tu tiveste",
                "ele teve",
                "ela teve",
                "nós tivemos",
                "vós tivestes",
                "eles tiveram",
                "elas tiveram",
            ],
        ),
        (
            "ter",
            "indicativo",
            "pretérito-imperfeito",
            [
                "eu tinha",
                "tu tinhas",
                "ele tinha",
                "ela tinha",
                "nós tínhamos",
                "vós tínheis",
                "eles tinham",
                "elas tinham",
            ],
        ),
        (
            "ter",
            "indicativo",
            "pretérito-mais-que-perfeito",
            [
                "eu tivera",
                "tu tiveras",
                "ele tivera",
                "ela tivera",
                "nós tivéramos",
                "vós tivéreis",
                "eles tiveram",
                "elas tiveram",
            ],
        ),
        (
            "ter",
            "indicativo",
            "pretérito-perfeito-composto",
            [
                "eu tenho tido",
                "tu tens tido",
                "ele tem tido",
                "ela tem tido",
                "nós temos tido",
                "vós tendes tido",
                "eles têm tido",
                "elas têm tido",
            ],
        ),
        (
            "ter",
            "indicativo",
            "pretérito-mais-que-perfeito-composto",
            [
                "eu tinha tido",
                "tu tinhas tido",
                "ele tinha tido",
                "ela tinha tido",
                "nós tínhamos tido",
                "vós tínheis tido",
                "eles tinham tido",
                "elas tinham tido",
            ],
        ),
        (
            "ter",
            "indicativo",
            "pretérito-mais-que-perfeito-anterior",
            [
                "eu tivera tido",
                "tu tiveras tido",
                "ele tivera tido",
                "ela tivera tido",
                "nós tivéramos tido",
                "vós tivéreis tido",
                "eles tiveram tido",
                "elas tiveram tido",
            ],
        ),
        (
            "ter",
            "indicativo",
            "futuro-do-presente",
            [
                "eu terei",
                "tu terás",
                "ele terá",
                "ela terá",
                "nós teremos",
                "vós tereis",
                "eles terão",
                "elas terão",
            ],
        ),
        (
            "ter",
            "indicativo",
            "futuro-do-presente-composto",
            [
                "eu terei tido",
                "tu terás tido",
                "ele terá tido",
                "ela terá tido",
                "nós teremos tido",
                "vós tereis tido",
                "eles terão tido",
                "elas terão tido",
            ],
        ),
        (
            "ter",
            "subjuntivo",
            "presente",
            [
                "que eu tenha",
                "que tu tenhas",
                "que ele tenha",
                "que ela tenha",
                "que nós tenhamos",
                "que vós tenhais",
                "que eles tenham",
                "que elas tenham",
            ],
        ),
        (
            "ter",
            "subjuntivo",
            "pretérito-perfeito",
            [
                "eu tenha tido",
                "tu tenhas tido",
                "ele tenha tido",
                "ela tenha tido",
                "nós tenhamos tido",
                "vós tenhais tido",
                "eles tenham tido",
                "elas tenham tido",
            ],
        ),
        (
            "ter",
            "subjuntivo",
            "pretérito-imperfeito",
            [
                "se eu tivesse",
                "se tu tivesses",
                "se ele tivesse",
                "se ela tivesse",
                "se nós tivéssemos",
                "se vós tivésseis",
                "se eles tivessem",
                "se elas tivessem",
            ],
        ),
        (
            "ter",
            "subjuntivo",
            "pretérito-mais-que-perfeito",
            [
                "eu tivesse tido",
                "tu tivesses tido",
                "ele tivesse tido",
                "ela tivesse tido",
                "nós tivéssemos tido",
                "vós tivésseis tido",
                "eles tivessem tido",
                "elas tivessem tido",
            ],
        ),
        (
            "ter",
            "subjuntivo",
            "futuro",
            [
                "quando eu tiver",
                "quando tu tiveres",
                "quando ele tiver",
                "quando ela tiver",
                "quando nós tivermos",
                "quando vós tiverdes",
                "quando eles tiverem",
                "quando elas tiverem",
            ],
        ),
        (
            "ter",
            "subjuntivo",
            "futuro-composto",
            [
                "eu tiver tido",
                "tu tiveres tido",
                "ele tiver tido",
                "ela tiver tido",
                "nós tivermos tido",
                "vós tiverdes tido",
                "eles tiverem tido",
                "elas tiverem tido",
            ],
        ),
        (
            "ter",
            "condicional",
            "futuro-do-pretérito",
            [
                "eu teria",
                "tu terias",
                "ele teria",
                "ela teria",
                "nós teríamos",
                "vós teríeis",
                "eles teriam",
                "elas teriam",
            ],
        ),
        (
            "ter",
            "condicional",
            "futuro-do-pretérito-composto",
            [
                "eu teria tido",
                "tu terias tido",
                "ele teria tido",
                "ela teria tido",
                "nós teríamos tido",
                "vós teríeis tido",
                "eles teriam tido",
                "elas teriam tido",
            ],
        ),
        (
            "ter",
            "infinitivo",
            "infinitivo-pessoal-presente",
            [
                "por ter eu",
                "por teres tu",
                "por ter ele",
                "por ter ela",
                "por termos nós",
                "por terdes vós",
                "por terem eles",
                "por terem elas",
            ],
        ),
        (
            "ter",
            "infinitivo",
            "infinitivo-pessoal-composto",
            [
                "ter tido",
                "teres tido",
                "ter tido",
                "ter tido",
                "termos tido",
                "terdes tido",
                "terem tido",
                "terem tido",
            ],
        ),
        (
            "ter",
            "imperativo",
            "afirmativo",
            ["-", "tem tu", "tenha você", "tenhamos nós", "tende vós", "tenham vocês"],
        ),
        (
            "ter",
            "imperativo",
            "negativo",
            [
                "-",
                "não tenhas tu",
                "não tenha você",
                "não tenhamos nós",
                "não tenhais vós",
                "não tenham vocês",
            ],
        ),
        (
            "andar",
            "indicativo",
            "pretérito-perfeito",
            [
                "eu andei",
                "tu andaste",
                "ele andou",
                "nós andámos",
                "vós andastes",
                "eles andaram",
            ],
        ),
        (
            "ficar",
            "indicativo",
            "pretérito-perfeito",
            [
                "eu fiquei",
                "tu ficaste",
                "ele ficou",
                "nós ficámos",
                "vós ficastes",
                "eles ficaram",
            ],
        ),
        (
            "amar",
            "indicativo",
            "pretérito-perfeito",
            [
                "eu amei",
                "tu amaste",
                "ele amou",
                "nós amámos",
                "vós amastes",
                "eles amaram",
            ],
        ),
        (
            "odiar",
            "indicativo",
            "pretérito-perfeito",
            [
                "eu odiei",
                "tu odiaste",
                "ele odiou",
                "nós odiámos",
                "vós odiastes",
                "eles odiaram",
            ],
        ),
        (
            "arguir",
            "indicativo",
            "presente",
            [
                "eu arguo",
                "tu argúis",
                "ele argúi",
                "nós arguimos",
                "vós arguistes",
                "eles argúem",
            ],
        ),
        (
            "arguir",
            "indicativo",
            "pretérito-perfeito",
            [
                "eu argui",
                "tu arguiste",
                "ele arguiu",
                "nós arguimos",
                "vós arguistes",
                "eles arguiram",
            ],
        ),
        (
            "arguir",
            "indicativo",
            "pretérito-imperfeito",
            [
                "eu arguia",
                "tu arguas",
                "ele arguia",
                "nós arguíamos",
                "vós arguíeis",
                "eles arguiam",
            ],
        ),
        (
            "arguir",
            "indicativo",
            "pretérito-mais-que-perfeito",
            [
                "eu arguira",
                "tu arguiras",
                "ele arguira",
                "nós arguíramos",
                "vós arguíreis",
                "eles arguiram",
            ],
        ),
        (
            "arguir",
            "indicativo",
            "futuro-do-presente",
            [
                "eu arguirei",
                "tu arguirás",
                "ele arguirá",
                "ela arguirá",
                "nós arguiremos",
                "vós arguireis",
                "eles arguirão",
                "elas arguirão",
            ],
        ),
        (
            "arguir",
            "condicional",
            "futuro-do-pretérito",
            [
                "eu arguiria",
                "tu arguirias",
                "ele arguiria",
                "ela arguiria",
                "nós arguiríamos",
                "vós arguiríeis",
                "eles arguiriam",
                "elas arguiriam",
            ],
        ),
        (
            "arguir",
            "subjuntivo",
            "pretérito-imperfeito",
            [
                "se eu arguisse",
                "se tu arguisses",
                "se ele arguisse",
                "se ela arguisse",
                "se nós arguíssemos",
                "se vós arguísseis",
                "se eles arguissem",
                "se elas arguissem",
            ],
        ),
        (
            "arguir",
            "subjuntivo",
            "futuro",
            [
                "quando eu arguir",
                "quando tu arguires",
                "quando ele arguir",
                "quando nós arguirmos",
                "quando vós arguirdes",
                "quando eles arguirem",
            ],
        ),
        (
            "arguir",
            "infinitivo",
            "infinitivo-pessoal-presente",
            [
                "por arguir eu",
                "por arguíres tu",
                "por arguir ele",
                "por arguirmos nós",
                "por arguirdes vós",
                "por arguírem eles",
            ],
        ),
        (
            "arguir",
            "imperativo",
            "afirmativo",
            [
                "-",
                "argúi tu",
                "argua você",
                "arguamos nós",
                "arguí vós",
                "arguam vocês",
            ],
        ),
    ],
)
def test_inflector_pt_conjugate_mood_tense(
    cg: Conjugator,
    infinitive: str,
    mood: Mood,
    tense: Tense,
    expected_result: List[str],
):
    tc = cg.conjugate_mood_tense(infinitive, mood, tense)
    assert [c[0] for c in tc] == expected_result


@pytest.mark.parametrize(
    "person,number,gender,is_reflexive,expected_result",
    [
        (Person.First, Number.Singular, Gender.m, False, "eu"),
        (Person.First, Number.Singular, Gender.m, True, "eu me"),
        (Person.Second, Number.Singular, Gender.m, False, "tu"),
        (Person.Second, Number.Singular, Gender.m, True, "tu te"),
        (Person.Third, Number.Singular, Gender.m, False, "ele"),
        (Person.Third, Number.Singular, Gender.m, True, "ele se"),
        (Person.Third, Number.Singular, Gender.f, False, "ela"),
        (Person.Third, Number.Singular, Gender.f, True, "ela se"),
        (Person.First, Number.Plural, Gender.m, False, "nós"),
        (Person.First, Number.Plural, Gender.m, True, "nós nos"),
        (Person.Second, Number.Plural, Gender.m, False, "vós"),
        (Person.Second, Number.Plural, Gender.m, True, "vós se"),
        (Person.Third, Number.Plural, Gender.m, False, "eles"),
        (Person.Third, Number.Plural, Gender.m, True, "eles se"),
        (Person.Third, Number.Plural, Gender.f, False, "elas"),
        (Person.Third, Number.Plural, Gender.f, True, "elas se"),
    ],
)
def test_inflector_pt_get_pronouns(
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
