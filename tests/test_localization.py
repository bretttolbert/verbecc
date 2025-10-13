import pytest

from verbecc.src.defs.constants.localization import xmood, xtense


@pytest.mark.parametrize(
    "lang,mood,expected",
    [
        ("es", "subjunctive", "subjuntivo"),
        ("fr", "indicative", "indicatif"),
        ("ca", "indicative", "indicatiu"),
    ],
)
def test_xmood(lang, mood, expected):
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
def test_xtense(lang, tense, expected):
    assert xtense(lang, tense) == expected
