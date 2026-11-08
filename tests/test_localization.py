import pytest

from verbecc.core.defs.constants.localization import xmood, xtense


@pytest.mark.parametrize(
    "lang,mood,expected",
    [
        ("es", "subjunctive", "subjuntivo"),
        ("fr", "indicative", "indicatif"),
        ("ca", "indicative", "indicatiu"),
    ],
)
def test_xmood(lang: str, mood: str, expected: str):
    assert xmood(lang, mood) == expected


@pytest.mark.parametrize(
    "lang,tense,expected",
    [
        ("es", "present", "presente"),
        ("es", "gerund", "gerundio"),
        ("fr", "gerund", "participe-présent"),
        ("fr", "present", "présent"),
    ],
)
def test_xtense(lang: str, tense: str, expected: str):
    assert xtense(lang, tense) == expected
