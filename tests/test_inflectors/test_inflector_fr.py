import pytest
from lxml import etree
from typing import cast

from verbecc.src.conjugator.conjugator import Conjugator, AlternatesBehavior
from verbecc.src.parsers.tense_template import TenseTemplate
from verbecc.src.defs.types.exceptions import ConjugatorError
from verbecc.src.defs.types.data_types import MoodsConjugation


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
        cg._inflector._add_subjunctive_relative_pronoun("tu manges", "")
        == "que tu manges"
    )
    assert (
        cg._inflector._add_subjunctive_relative_pronoun("il mange", "") == "qu'il mange"
    )
    assert (
        cg._inflector._add_subjunctive_relative_pronoun("elles mangent", "")
        == "qu'elles mangent"
    )


def test_add_reflexive_pronoun(cg):
    assert cg._inflector._add_reflexive_pronoun("lever") == "se lever"
    assert cg._inflector._add_reflexive_pronoun("écrouler") == "s'écrouler"


def test_split_reflexive(cg):
    assert cg._inflector._split_reflexive("se lever") == (True, "lever")
    assert cg._inflector._split_reflexive("s'écrouler") == (True, "écrouler")
    assert cg._inflector._split_reflexive("secouer") == (False, "secouer")


@pytest.mark.parametrize(
    "infinitive,expected_result",
    [
        ("être", False),
        ("lever", True),
        ("pleuvoir", False),
        ("manger", True),
    ],
)
def test_inflector_fr_verb_can_be_reflexive(cg, infinitive, expected_result):
    assert cg._inflector._verb_can_be_reflexive(infinitive) == expected_result


def test_inflector_fr_impersonal_verbs(cg):
    impersonal_verbs = [
        v.infinitive
        for v in cg._inflector._verb_parser.verbs
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
    tense_name = "présent"
    tense_template = TenseTemplate(tense_elem)
    out = cg._conjugate_simple_mood_tense(verb_stem, "indicatif", tense_template)
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
    verb_stem = cg._inflector._get_verb_stem_from_template_name("manger", "man:ger")
    assert verb_stem == "man"
    verb_stem = cg._inflector._get_verb_stem_from_template_name("téléphoner", "aim:er")
    assert verb_stem == "téléphon"
    verb_stem = cg._inflector._get_verb_stem_from_template_name("vendre", "ten:dre")
    assert verb_stem == "ven"
    # In the case of irregular verbs, the verb stem is empty string
    verb_stem = cg._inflector._get_verb_stem_from_template_name("aller", ":aller")
    assert verb_stem == ""
    # The infinitive ending must match the template ending
    with pytest.raises(ConjugatorError):
        verb_stem = cg._inflector._get_verb_stem_from_template_name("vendre", "man:ger")


@pytest.mark.parametrize(
    "person,gender,is_reflexive,expected_result",
    [
        ("1s", "m", False, "je"),
        ("1s", "m", True, "je me"),
        ("2s", "m", False, "tu"),
        ("2s", "m", True, "tu te"),
        ("3s", "m", False, "il"),
        ("3s", "m", True, "il se"),
        ("3s", "f", False, "elle"),
        ("3s", "f", True, "elle se"),
        ("1p", "m", False, "nous"),
        ("1p", "m", True, "nous nous"),
        ("2p", "m", False, "vous"),
        ("2p", "m", True, "vous vous"),
        ("3p", "m", False, "ils"),
        ("3p", "m", True, "ils se"),
        ("3p", "f", False, "elles"),
        ("3p", "f", True, "elles se"),
    ],
)
def test_inflector_fr_get_default_pronoun(
    cg, person, gender, is_reflexive, expected_result
):
    assert (
        cg._inflector._get_default_pronoun(person, gender, is_reflexive=is_reflexive)
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


def test_inflector_fr_raser(cg):
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
        "m",
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


def test_inflector_fr_se_raser(cg):
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
        "m",
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
