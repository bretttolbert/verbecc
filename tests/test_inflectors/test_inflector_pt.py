import pytest

from verbecc.core.conjugator.complete_conjugator import CompleteConjugator
from verbecc.core.conjugator.mood_conjugator import MoodConjugator
from verbecc.core.conjugator.tense_conjugator import TenseConjugator
from verbecc.core.defs.types.conjugation.tense_conjugation import TenseConjugation
from verbecc.core.defs.types.gender import Gender
from verbecc.core.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.core.defs.types.mood import Mood
from verbecc.core.defs.types.mood import Moods
from verbecc.core.defs.types.number import Number
from verbecc.core.defs.types.person import Person
from verbecc.core.defs.types.tense import Tense
from verbecc.core.defs.types.tense import Tenses


@pytest.fixture(scope="module")
def ccg():
    ccg = CompleteConjugator(lang=Lang.pt)
    yield ccg


@pytest.fixture(scope="module")
def mcg():
    mcg = MoodConjugator(lang=Lang.pt)
    yield mcg


@pytest.fixture(scope="module")
def tcg():
    tcg = TenseConjugator(lang=Lang.pt)
    yield tcg


def test_all_verbs_have_templates(ccg: CompleteConjugator):
    verbs = ccg.get_verbs()
    template_names: list[str] = ccg.get_template_names()
    missing_templates: set[str] = set()
    for verb in verbs:
        if verb.template not in template_names:
            missing_templates.add(verb.template)
    assert len(missing_templates) == 0


def test_conjugate_ter_subjuntivo_preterito_perfeito(ccg: CompleteConjugator):
    tc = ccg.conjugate_mood_tense(
        "ter", Moods.pt.Subjuntivo, Tenses.pt.PretéritoPerfeito
    )
    assert [c[0] for c in tc] == [
        "eu tenha tido",
        "tu tenhas tido",
        "ele tenha tido",
        "ela tenha tido",
        "você tenha tido",
        "nós tenhamos tido",
        "vós tenhais tido",
        "eles tenham tido",
        "elas tenham tido",
        "vocês tenham tido",
    ]


def test_conjugate_ter_infinitivo_pessoal_presente(ccg: CompleteConjugator):
    """
    Ref: https://www.conjugacao.com.br/verbo-ter/

    Difference: In Spanish, infinitivo moods is conjugated without pronouns
    """
    tc = ccg.conjugate_mood_tense(
        "ter", Moods.pt.Infinitivo, Tenses.pt.InfinitivoPessoalPresente
    )
    assert [c[0] for c in tc] == [
        "por ter eu",
        "por teres tu",
        "por ter ele",
        "por ter ela",
        "por ter você",
        "por termos nós",
        "por terdes vós",
        "por terem eles",
        "por terem elas",
        "por terem vocês",
    ]


def test_conjugate_ter_imperativo_afirmativo(ccg: CompleteConjugator):
    """
    Ref: https://www.conjugacao.com.br/verbo-ter/
    """
    tc: TenseConjugation = ccg.conjugate_mood_tense("ter", Moods.pt.Imperativo, Tenses.pt.Afirmativo)
    assert [c[0] for c in tc] == [
        "-",
        "tem tu",
        "tenha você",
        "tenhamos nós",
        "tende vós",
        "tenham vocês",
    ]


def test_conjugate_ter_imperativo_negativo(ccg: CompleteConjugator):
    """
    Ref: https://www.conjugacao.com.br/verbo-ter/
    """
    tc: TenseConjugation = ccg.conjugate_mood_tense("ter", Moods.pt.Imperativo, Tenses.pt.Negativo)
    assert [c[0] for c in tc] == [
        "-",
        "não tenhas tu",
        "não tenha você",
        "não tenhamos nós",
        "não tenhais vós",
        "não tenham vocês",
    ]


def test_conjugate_ter_infinitivo_pessoal_composto(ccg: CompleteConjugator):
    tc = ccg.conjugate_mood_tense(
        "ter", Moods.pt.Infinitivo, Tenses.pt.InfinitivoPessoalComposto
    )
    assert [c[0] for c in tc] == [
        "ter tido",
        "teres tido",
        "ter tido",
        "ter tido",
        "ter tido",
        "termos tido",
        "terdes tido",
        "terem tido",
        "terem tido",
        "terem tido",
    ]


@pytest.mark.parametrize(
    "infinitive,mood,tense,expected_result",
    [
        (
            "ter",
            Moods.pt.Indicativo,
            Tenses.pt.Presente,
            [
                "eu tenho",
                "tu tens",
                "ele tem",
                "ela tem",
                "você tem",
                "nós temos",
                "vós tendes",
                "eles têm",
                "elas têm",
                "vocês têm",
            ],
        ),
        (
            "ter",
            Moods.pt.Indicativo,
            Tenses.pt.PretéritoPerfeito,
            [
                "eu tive",
                "tu tiveste",
                "ele teve",
                "ela teve",
                "você teve",
                "nós tivemos",
                "vós tivestes",
                "eles tiveram",
                "elas tiveram",
                "vocês tiveram",
            ],
        ),
        (
            "ter",
            Moods.pt.Indicativo,
            Tenses.pt.PretéritoImperfeito,
            [
                "eu tinha",
                "tu tinhas",
                "ele tinha",
                "ela tinha",
                "você tinha",
                "nós tínhamos",
                "vós tínheis",
                "eles tinham",
                "elas tinham",
                "vocês tinham",
            ],
        ),
        (
            "ter",
            Moods.pt.Indicativo,
            Tenses.pt.PretéritoMaisQuePerfeito,
            [
                "eu tivera",
                "tu tiveras",
                "ele tivera",
                "ela tivera",
                "você tivera",
                "nós tivéramos",
                "vós tivéreis",
                "eles tiveram",
                "elas tiveram",
                "vocês tiveram",
            ],
        ),
        (
            "ter",
            Moods.pt.Indicativo,
            "pretérito-perfeito-composto",
            [
                "eu tenho tido",
                "tu tens tido",
                "ele tem tido",
                "ela tem tido",
                "você tem tido",
                "nós temos tido",
                "vós tendes tido",
                "eles têm tido",
                "elas têm tido",
                "vocês têm tido",
            ],
        ),
        (
            "ter",
            Moods.pt.Indicativo,
            Tenses.pt.PretéritoMaisQuePerfeitoComposto,
            [
                "eu tinha tido",
                "tu tinhas tido",
                "ele tinha tido",
                "ela tinha tido",
                "você tinha tido",
                "nós tínhamos tido",
                "vós tínheis tido",
                "eles tinham tido",
                "elas tinham tido",
                "vocês tinham tido",
            ],
        ),
        (
            "ter",
            Moods.pt.Indicativo,
            Tenses.pt.PretéritoMaisQuePerfeitoAnterior,
            [
                "eu tivera tido",
                "tu tiveras tido",
                "ele tivera tido",
                "ela tivera tido",
                "você tivera tido",
                "nós tivéramos tido",
                "vós tivéreis tido",
                "eles tiveram tido",
                "elas tiveram tido",
                "vocês tiveram tido",
            ],
        ),
        (
            "ter",
            Moods.pt.Indicativo,
            Tenses.pt.FuturoDoPresente,
            [
                "eu terei",
                "tu terás",
                "ele terá",
                "ela terá",
                "você terá",
                "nós teremos",
                "vós tereis",
                "eles terão",
                "elas terão",
                "vocês terão",
            ],
        ),
        (
            "ter",
            Moods.pt.Indicativo,
            Tenses.pt.FuturoDoPresenteComposto,
            [
                "eu terei tido",
                "tu terás tido",
                "ele terá tido",
                "ela terá tido",
                "você terá tido",
                "nós teremos tido",
                "vós tereis tido",
                "eles terão tido",
                "elas terão tido",
                "vocês terão tido",
            ],
        ),
        (
            "ter",
            Moods.pt.Subjuntivo,
            Tenses.pt.Presente,
            [
                "que eu tenha",
                "que tu tenhas",
                "que ele tenha",
                "que ela tenha",
                "que você tenha",
                "que nós tenhamos",
                "que vós tenhais",
                "que eles tenham",
                "que elas tenham",
                "que vocês tenham",
            ],
        ),
        (
            "ter",
            Moods.pt.Subjuntivo,
            Tenses.pt.PretéritoPerfeito,
            [
                "eu tenha tido",
                "tu tenhas tido",
                "ele tenha tido",
                "ela tenha tido",
                "você tenha tido",
                "nós tenhamos tido",
                "vós tenhais tido",
                "eles tenham tido",
                "elas tenham tido",
                "vocês tenham tido",
            ],
        ),
        (
            "ter",
            Moods.pt.Subjuntivo,
            Tenses.pt.PretéritoImperfeito,
            [
                "se eu tivesse",
                "se tu tivesses",
                "se ele tivesse",
                "se ela tivesse",
                "se você tivesse",
                "se nós tivéssemos",
                "se vós tivésseis",
                "se eles tivessem",
                "se elas tivessem",
                "se vocês tivessem",
            ],
        ),
        (
            "ter",
            Moods.pt.Subjuntivo,
            Tenses.pt.PretéritoMaisQuePerfeito,
            [
                "eu tivesse tido",
                "tu tivesses tido",
                "ele tivesse tido",
                "ela tivesse tido",
                "você tivesse tido",
                "nós tivéssemos tido",
                "vós tivésseis tido",
                "eles tivessem tido",
                "elas tivessem tido",
                "vocês tivessem tido",
            ],
        ),
        (
            "ter",
            Moods.pt.Subjuntivo,
            Tenses.pt.Futuro,
            [
                "quando eu tiver",
                "quando tu tiveres",
                "quando ele tiver",
                "quando ela tiver",
                "quando você tiver",
                "quando nós tivermos",
                "quando vós tiverdes",
                "quando eles tiverem",
                "quando elas tiverem",
                "quando vocês tiverem",
            ],
        ),
        (
            "ter",
            Moods.pt.Subjuntivo,
            Tenses.pt.FuturoComposto,
            [
                "eu tiver tido",
                "tu tiveres tido",
                "ele tiver tido",
                "ela tiver tido",
                "você tiver tido",
                "nós tivermos tido",
                "vós tiverdes tido",
                "eles tiverem tido",
                "elas tiverem tido",
                "vocês tiverem tido",
            ],
        ),
        (
            "ter",
            Moods.pt.Condicional,
            Tenses.pt.FuturoDoPretérito,
            [
                "eu teria",
                "tu terias",
                "ele teria",
                "ela teria",
                "você teria",
                "nós teríamos",
                "vós teríeis",
                "eles teriam",
                "elas teriam",
                "vocês teriam",
            ],
        ),
        (
            "ter",
            Moods.pt.Condicional,
            Tenses.pt.FuturoDoPretéritoComposto,
            [
                "eu teria tido",
                "tu terias tido",
                "ele teria tido",
                "ela teria tido",
                "você teria tido",
                "nós teríamos tido",
                "vós teríeis tido",
                "eles teriam tido",
                "elas teriam tido",
                "vocês teriam tido",
            ],
        ),
        (
            "ter",
            Moods.pt.Infinitivo,
            Tenses.pt.InfinitivoPessoalPresente,
            [
                "por ter eu",
                "por teres tu",
                "por ter ele",
                "por ter ela",
                "por ter você",
                "por termos nós",
                "por terdes vós",
                "por terem eles",
                "por terem elas",
                "por terem vocês",
            ],
        ),
        (
            "ter",
            Moods.pt.Infinitivo,
            Tenses.pt.InfinitivoPessoalComposto,
            [
                "ter tido",
                "teres tido",
                "ter tido",
                "ter tido",
                "ter tido",
                "termos tido",
                "terdes tido",
                "terem tido",
                "terem tido",
                "terem tido",
            ],
        ),
        (
            "ter",
            Moods.pt.Imperativo,
            Tenses.pt.Afirmativo,
            [
                "-",
                "tem tu",
                "tenha você",
                "tenhamos nós",
                "tende vós",
                "tenham vocês",
            ],
        ),
        (
            "ter",
            Moods.pt.Imperativo,
            Tenses.pt.Negativo,
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
            Moods.pt.Indicativo,
            Tenses.pt.PretéritoPerfeito,
            [
                "eu andei",
                "tu andaste",
                "ele andou",
                "ela andou",
                "você andou",
                "nós andámos",
                "vós andastes",
                "eles andaram",
                "elas andaram",
                "vocês andaram",
            ],
        ),
        (
            "ficar",
            Moods.pt.Indicativo,
            Tenses.pt.PretéritoPerfeito,
            [
                "eu fiquei",
                "tu ficaste",
                "ele ficou",
                "ela ficou",
                "você ficou",
                "nós ficámos",
                "vós ficastes",
                "eles ficaram",
                "elas ficaram",
                "vocês ficaram",
            ],
        ),
        (
            "amar",
            Moods.pt.Indicativo,
            Tenses.pt.PretéritoPerfeito,
            [
                "eu amei",
                "tu amaste",
                "ele amou",
                "ela amou",
                "você amou",
                "nós amámos",
                "vós amastes",
                "eles amaram",
                "elas amaram",
                "vocês amaram",
            ],
        ),
        (
            "odiar",
            Moods.pt.Indicativo,
            Tenses.pt.PretéritoPerfeito,
            [
                "eu odiei",
                "tu odiaste",
                "ele odiou",
                "ela odiou",
                "você odiou",
                "nós odiámos",
                "vós odiastes",
                "eles odiaram",
                "elas odiaram",
                "vocês odiaram",
            ],
        ),
        (
            "arguir",
            Moods.pt.Indicativo,
            Tenses.pt.Presente,
            [
                "eu arguo",
                "tu argúis",
                "ele argúi",
                "ela argúi",
                "você argúi",
                "nós arguimos",
                "vós arguistes",
                "eles argúem",
                "elas argúem",
                "vocês argúem",
            ],
        ),
        (
            "arguir",
            Moods.pt.Indicativo,
            Tenses.pt.PretéritoPerfeito,
            [
                "eu argui",
                "tu arguiste",
                "ele arguiu",
                "ela arguiu",
                "você arguiu",
                "nós arguimos",
                "vós arguistes",
                "eles arguiram",
                "elas arguiram",
                "vocês arguiram",
            ],
        ),
        (
            "arguir",
            Moods.pt.Indicativo,
            Tenses.pt.PretéritoImperfeito,
            [
                "eu arguia",
                "tu arguas",
                "ele arguia",
                "ela arguia",
                "você arguia",
                "nós arguíamos",
                "vós arguíeis",
                "eles arguiam",
                "elas arguiam",
                "vocês arguiam",
            ],
        ),
        (
            "arguir",
            Moods.pt.Indicativo,
            Tenses.pt.PretéritoMaisQuePerfeito,
            [
                "eu arguira",
                "tu arguiras",
                "ele arguira",
                "ela arguira",
                "você arguira",
                "nós arguíramos",
                "vós arguíreis",
                "eles arguiram",
                "elas arguiram",
                "vocês arguiram",
            ],
        ),
        (
            "arguir",
            Moods.pt.Indicativo,
            Tenses.pt.FuturoDoPresente,
            [
                "eu arguirei",
                "tu arguirás",
                "ele arguirá",
                "ela arguirá",
                "você arguirá",
                "nós arguiremos",
                "vós arguireis",
                "eles arguirão",
                "elas arguirão",
                "vocês arguirão",
            ],
        ),
        (
            "arguir",
            Moods.pt.Condicional,
            Tenses.pt.FuturoDoPretérito,
            [
                "eu arguiria",
                "tu arguirias",
                "ele arguiria",
                "ela arguiria",
                "você arguiria",
                "nós arguiríamos",
                "vós arguiríeis",
                "eles arguiriam",
                "elas arguiriam",
                "vocês arguiriam",
            ],
        ),
        (
            "arguir",
            Moods.pt.Subjuntivo,
            Tenses.pt.PretéritoImperfeito,
            [
                "se eu arguisse",
                "se tu arguisses",
                "se ele arguisse",
                "se ela arguisse",
                "se você arguisse",
                "se nós arguíssemos",
                "se vós arguísseis",
                "se eles arguissem",
                "se elas arguissem",
                "se vocês arguissem",
            ],
        ),
        (
            "arguir",
            Moods.pt.Subjuntivo,
            Tenses.pt.Futuro,
            [
                "quando eu arguir",
                "quando tu arguires",
                "quando ele arguir",
                "quando ela arguir",
                "quando você arguir",
                "quando nós arguirmos",
                "quando vós arguirdes",
                "quando eles arguirem",
                "quando elas arguirem",
                "quando vocês arguirem",
            ],
        ),
        (
            "arguir",
            Moods.pt.Infinitivo,
            Tenses.pt.InfinitivoPessoalPresente,
            [
                "por arguir eu",
                "por arguíres tu",
                "por arguir ele",
                "por arguir ela",
                "por arguir você",
                "por arguirmos nós",
                "por arguirdes vós",
                "por arguírem eles",
                "por arguírem elas",
                "por arguírem vocês",
            ],
        ),
        (
            "arguir",
            Moods.pt.Imperativo,
            Tenses.pt.Afirmativo,
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
    ccg: CompleteConjugator,
    infinitive: str,
    mood: Mood,
    tense: Tense,
    expected_result: list[str],
):
    tc = ccg.conjugate_mood_tense(infinitive, mood, tense)
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
        (Person.Second, Number.Plural, Gender.m, True, "vós vos"),
        (Person.Third, Number.Plural, Gender.m, False, "eles"),
        (Person.Third, Number.Plural, Gender.m, True, "eles se"),
        (Person.Third, Number.Plural, Gender.f, False, "elas"),
        (Person.Third, Number.Plural, Gender.f, True, "elas se"),
    ],
)
def test_inflector_pt_get_pronouns(
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


def test_reflexive_indicativo_presente(ccg: CompleteConjugator):
    tc = ccg.conjugate_mood_tense("vestir-se", Moods.pt.Indicativo, Tenses.pt.Presente)
    assert [c[0] for c in tc] == [
        "eu visto-me",
        "tu vestes-te",
        "ele veste-se",
        "ela veste-se",
        "você veste-se",
        "nós vestimos-nos",
        "vós vestis-vos",
        "eles vestem-se",
        "elas vestem-se",
        "vocês vestem-se",
    ]


def test_reflexive_indicativo_pretérito_perfeito_composto(ccg: CompleteConjugator):
    tc = ccg.conjugate_mood_tense(
        "vestir-se", Moods.pt.Indicativo, Tenses.pt.PretéritoPerfeitoComposto
    )
    assert [c[0] for c in tc] == [
        "eu tenho-me vestido",
        "tu tens-te vestido",
        "ele tem-se vestido",
        "ela tem-se vestido",
        "você tem-se vestido",
        "nós temos-nos vestido",
        "vós tendes-vos vestido",
        "eles têm-se vestido",
        "elas têm-se vestido",
        "vocês têm-se vestido",
    ]
