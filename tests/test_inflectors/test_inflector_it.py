import pytest
from typing import cast

from verbecc.src.conjugator.conjugator import Conjugator, MoodsConjugation


@pytest.fixture(scope="module")
def cg():
    cg = Conjugator(lang="it")
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
            ["io ho", "tu hai", "lui ha", "noi abbiamo", "voi avete", "loro hanno"],
        ),
        (
            "avere",
            "indicativo",
            "imperfetto",
            [
                "io avevo",
                "tu avevi",
                "lui aveva",
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
    assert cg.conjugate_mood_tense(infinitive, mood, tense) == expected_result


def test_inflector_it_conjugate(cg):
    assert cg.conjugate("avere") != None


def test_inflector_it_add_subjunctive_relative_pronoun(cg):
    assert (
        cg._inflector._add_subjunctive_relative_pronoun("io abbia", "")
        == "che io abbia"
    )


@pytest.mark.parametrize(
    "person,gender,is_reflexive,expected_result",
    [
        ("1s", "m", False, "io"),
        ("1s", "m", True, "mi"),
        ("2s", "m", False, "tu"),
        ("2s", "m", True, "ti"),
        ("3s", "m", False, "lui"),
        ("3s", "m", True, "si"),
        ("3s", "f", False, "lei"),
        ("3s", "f", True, "si"),
        ("1p", "m", False, "noi"),
        ("1p", "m", True, "ci"),
        ("2p", "m", False, "voi"),
        ("2p", "m", True, "vi"),
        ("3p", "m", False, "loro"),
        ("3p", "m", True, "si"),
        ("3p", "f", False, "loro"),
        ("3p", "f", True, "si"),
    ],
)
def test_inflector_it_get_default_pronoun(
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
            "avere",
            ["io ho", "tu hai", "lui ha", "noi abbiamo", "voi avete", "loro hanno"],
        ),
        (
            "essere",
            ["io sono", "tu sei", "lui è", "noi siamo", "voi siete", "loro sono"],
        ),
        (
            "alzare",
            [
                "io alzo",
                "tu alzi",
                "lui alza",
                "noi alziamo",
                "voi alzate",
                "loro alzano",
            ],
        ),
    ],
)
def test_indicative_present(cg, infinitive, expected_result):
    conj = cg.conjugate(infinitive)
    moods_conj = cast(MoodsConjugation, conj["moods"])
    assert moods_conj["indicativo"]["presente"] == expected_result


@pytest.mark.parametrize(
    "infinitive,expected_result",
    [
        (
            "avere",
            [
                "io ho avuto",
                "tu hai avuto",
                "lui ha avuto",
                "noi abbiamo avuto",
                "voi avete avuto",
                "loro hanno avuto",
            ],
        ),
        (
            "essere",
            [
                "io sono stato",
                "tu sei stato",
                "lui è stato",
                "noi siamo stato",
                "voi siete stato",
                "loro sono stato",
            ],
        ),
        (
            "alzare",
            [
                "io ho alzato",
                "tu hai alzato",
                "lui ha alzato",
                "noi abbiamo alzato",
                "voi avete alzato",
                "loro hanno alzato",
            ],
        ),
    ],
)
def test_passato_prossimo(cg, infinitive, expected_result):
    conj = cg.conjugate(infinitive)
    moods_conj = cast(MoodsConjugation, conj["moods"])
    assert moods_conj["indicativo"]["passato-prossimo"] == expected_result


@pytest.mark.skip("TODO: fix")
@pytest.mark.parametrize(
    "infinitive,expected_result",
    [
        (
            "alzarsi",
            [
                "io mi alzo",
                "tu ti alzi",
                "lei si alza",
                "noi ci alziamo",
                "voi vi alzate",
                "loro si alzano",
            ],
        ),
    ],
)
def test_alzarsi_indicative_present(cg, infinitive, expected_result):
    conj = cg.conjugate(infinitive)
    moods_conj = cast(MoodsConjugation, conj["moods"])
    assert moods_conj["indicativo"]["presente"] == expected_result


@pytest.mark.skip("TODO: fix")
@pytest.mark.parametrize(
    "infinitive,expected_result",
    [
        (
            "alzarsi",
            [
                "io mi sono alzato",
                "tu ti sei alzato",
                "lei si è alzato",
                "noi ci siamo alzati",
                "voi vi siete alzati",
                "loro si sono alzate",
            ],
        ),
    ],
)
def test_alzarsi_passato_prossimo(cg, infinitive, expected_result):
    conj = cg.conjugate(infinitive)
    moods_conj = cast(MoodsConjugation, conj["moods"])
    assert moods_conj["indicativo"]["passato-prossimo"] == expected_result
