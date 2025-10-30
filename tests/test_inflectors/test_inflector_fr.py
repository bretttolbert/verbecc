import pytest
from lxml import etree
from typing import cast

from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.person import Person
from verbecc.src.conjugator.conjugator import Conjugator, AlternatesBehavior
from verbecc.src.parsers.tense_template_parser import TenseTemplateParser
from verbecc.src.defs.types.exceptions import ConjugatorError
from verbecc.src.defs.types.conjugation import MoodsConjugation


@pytest.fixture(scope="module")
def cg():
    cg = Conjugator(lang="fr")
    yield cg


def test_all_verbs_have_templates(cg):
    verbs = cg.get_verbs()
    template_names = cg.get_template_names()
    missing_templates = set()
    for verb in verbs:
        if verb.template not in template_names:
            missing_templates.add(verb.template)
    assert len(missing_templates) == 0


def test_add_subjunctive_relative_prounoun(cg):
    assert (
        cg._inflector.add_subjunctive_relative_pronoun("tu manges", "")
        == "que tu manges"
    )
    assert (
        cg._inflector.add_subjunctive_relative_pronoun("il mange", "") == "qu'il mange"
    )
    assert (
        cg._inflector.add_subjunctive_relative_pronoun("elles mangent", "")
        == "qu'elles mangent"
    )


def testadd_reflexive_pronoun(cg):
    assert cg._inflector.add_reflexive_pronoun("lever") == "se lever"
    assert cg._inflector.add_reflexive_pronoun("écrouler") == "s'écrouler"


def testsplit_reflexive(cg):
    assert cg._inflector.split_reflexive("se lever") == (True, "lever")
    assert cg._inflector.split_reflexive("s'écrouler") == (True, "écrouler")
    assert cg._inflector.split_reflexive("secouer") == (False, "secouer")


@pytest.mark.parametrize(
    "infinitive,expected_result",
    [
        ("être", False),
        ("lever", True),
        ("pleuvoir", False),
        ("manger", True),
    ],
)
def test_inflector_frverb_can_be_reflexive(cg, infinitive, expected_result):
    assert cg._inflector.verb_can_be_reflexive(infinitive) == expected_result


def test_inflector_fr_impersonal_verbs(cg):
    impersonal_verbs = [
        v.infinitive
        for v in cg._inflector._verbs
        if cg._inflector._is_impersonal_verb(v.infinitive)
    ]
    assert set(impersonal_verbs) == set(
        [
            "advenir",
            "apparoir",
            "bruiner",
            "bruire",
            "chaloir",
            "clore",
            "déclore",
            "échoir",
            "éclore",
            "enclore",
            "falloir",
            "forclore",
            "frire",
            "grêler",
            "messeoir",
            "neiger",
            "pleuvoir",
            "seoir",
            "sourdre",
        ]
    )


def test_inflector_fr_conjugate_simple_mood_tense(cg):
    mood = "indicatif"
    tense = "présent"
    verb_stem = "man"
    tense_elem = etree.fromstring(
        """<présent>
        <p><i>ge</i></p>
        <p><i>ges</i></p>
        <p><i>ge</i></p>
        <p><i>geons</i></p>
        <p><i>gez</i></p>
        <p><i>gent</i></p>
        </présent>""",
        parser=None,
    )
    tense_template = TenseTemplateParser(Lang.fr, mood).parse(tense_elem)
    out = cg._conjugate_simple_mood_tense(verb_stem, mood, tense, tense_template)
    assert len(out) == 6
    assert out == [
        "je mange",
        "tu manges",
        "il mange",
        "nous mangeons",
        "vous mangez",
        "ils mangent",
    ]


def test_inflector_fr_get_verb_stem_from_template_name(cg):
    verb_stem = cg._inflector.get_verb_stem_from_template_name("manger", "man:ger")
    assert verb_stem == "man"
    verb_stem = cg._inflector.get_verb_stem_from_template_name("téléphoner", "aim:er")
    assert verb_stem == "téléphon"
    verb_stem = cg._inflector.get_verb_stem_from_template_name("vendre", "ten:dre")
    assert verb_stem == "ven"
    # In the case of irregular verbs, the verb stem is empty string
    verb_stem = cg._inflector.get_verb_stem_from_template_name("aller", ":aller")
    assert verb_stem == ""
    # The infinitive ending must match the template ending
    with pytest.raises(ConjugatorError):
        verb_stem = cg._inflector.get_verb_stem_from_template_name("vendre", "man:ger")


@pytest.mark.parametrize(
    "person,gender,is_reflexive,expected_result",
    [
        (Person.FirstPersonSingular, Gender.m, False, "je"),
        (Person.FirstPersonSingular, Gender.m, True, "je me"),
        (Person.SecondPersonSingular, Gender.m, False, "tu"),
        (Person.SecondPersonSingular, Gender.m, True, "tu te"),
        (Person.ThirdPersonSingular, Gender.m, False, "il"),
        (Person.ThirdPersonSingular, Gender.m, True, "il se"),
        (Person.ThirdPersonSingular, Gender.f, False, "elle"),
        (Person.ThirdPersonSingular, Gender.f, True, "elle se"),
        (Person.FirstPersonPlural, Gender.m, False, "nous"),
        (Person.FirstPersonPlural, Gender.m, True, "nous nous"),
        (Person.SecondPersonPlural, Gender.m, False, "vous"),
        (Person.SecondPersonPlural, Gender.m, True, "vous vous"),
        (Person.ThirdPersonPlural, Gender.m, False, "ils"),
        (Person.ThirdPersonPlural, Gender.m, True, "ils se"),
        (Person.ThirdPersonPlural, Gender.f, False, "elles"),
        (Person.ThirdPersonPlural, Gender.f, True, "elles se"),
    ],
)
def test_inflector_fr_get_default_pronoun(
    cg, person: Person, gender: Gender, is_reflexive: bool, expected_result: str
):
    assert (
        cg._inflector.get_default_pronoun(person, gender, is_reflexive=is_reflexive)
        == expected_result
    )


@pytest.mark.parametrize(
    "infinitive,expected_result",
    [
        (
            "avoir",
            ["j'ai", "tu as", "il a", "nous avons", "vous avez", "ils ont"],
        ),
        (
            "habiter",
            [
                "j'habite",
                "tu habites",
                "il habite",
                "nous habitons",
                "vous habitez",
                "ils habitent",
            ],
        ),
        (
            "s'habiller",
            [
                "je m'habille",
                "tu t'habilles",
                "il s'habille",
                "nous nous habillons",
                "vous vous habillez",
                "ils s'habillent",
            ],
        ),
    ],
)
def test_pronoun_combined_vowel_h_non_aspiré(cg, infinitive, expected_result):
    conj = cg.conjugate(infinitive)
    moods_conj = cast(MoodsConjugation, conj["moods"])
    assert moods_conj["indicatif"]["présent"] == expected_result


@pytest.mark.parametrize(
    "infinitive,expected_result",
    [
        (
            "habiter",
            [
                "que j'habite",
                "que tu habites",
                "qu'il habite",
                "que nous habitions",
                "que vous habitiez",
                "qu'ils habitent",
            ],
        )
    ],
)
def test_subjonctif_vowel_h_non_aspiré(cg, infinitive, expected_result):
    conj = cg.conjugate(infinitive)
    moods_conj = cast(MoodsConjugation, conj["moods"])
    assert moods_conj["subjonctif"]["présent"] == expected_result


def test_can_conjugate_all_verbs(cg):
    verbs = cg.get_verbs()
    all_conjugations = {}
    for verb in verbs:
        conjugation = cg.conjugate(verb.infinitive)
        all_conjugations[verb] = conjugation
    assert len(all_conjugations) == len(verbs)


def test_inflector_fr_conjugate_compound_raser(cg):
    infinitive = "raser"
    co = cg._get_conj_obs(infinitive)
    ret = cg._conjugate_compound(
        co,
        "subjonctif",
        "passé",
        "subjonctif",
        "présent",
        False,
        AlternatesBehavior.All,
        Gender.m,
        True,
    )
    assert ret == [
        ["que j'aie rasé"],
        ["que tu aies rasé"],
        ["qu'il ait rasé"],
        ["que nous ayons rasé"],
        ["que vous ayez rasé"],
        ["qu'ils aient rasé"],
    ]


def test_inflector_fr_conjugate_compound_se_raser(cg):
    """
    test targeting:
        - reflexive verb conjugation
        - compound verb conjugation with a verb conjugated with être (inflected participle)
        - Note: In French, all reflexive verbs are conjugated with être
    """
    infinitive = "se raser"
    co = cg._get_conj_obs(infinitive)
    ret = cg._conjugate_compound(
        co,
        "subjonctif",
        "passé",
        "subjonctif",
        "présent",
        False,
        AlternatesBehavior.All,
        Gender.m,
        True,
    )
    assert ret == [
        ["que je me sois rasé"],
        ["que tu te sois rasé"],
        ["qu'il se soit rasé"],
        ["que nous nous soyons rasés"],
        ["que vous vous soyez rasés"],
        ["qu'ils se soient rasés"],
    ]


def test_inflector_fr_conjugate_compound_parler_indicative_passé_composé(cg):
    """
    test targeting:
        - compound verb conjugation with a verb not conjugated with être (non-inflected participle)
    """
    infinitive = "parler"
    co = cg._get_conj_obs(infinitive)
    ret = cg._conjugate_compound(
        co,
        "indicatif",
        "passé-composé",
        "indicatif",
        "présent",
        False,
        AlternatesBehavior.All,
        Gender.m,
        True,
    )
    assert ret == [
        ["j'ai parlé"],
        ["tu as parlé"],
        ["il a parlé"],
        ["nous avons parlé"],
        ["vous avez parlé"],
        ["ils ont parlé"],
    ]
