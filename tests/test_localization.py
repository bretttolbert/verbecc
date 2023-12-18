import pytest

from verbecc.localization import localize_mood, localize_tense


@pytest.mark.parametrize(
    "lang,mood,xmood",
    [
        ("es", "subjunctive", "subjuntivo"),
        ("fr", "indicative", "indicatif"),
        ("ca", "indicative", "indicatiu"),
    ],
)
def test_localize_mood(lang, mood, xmood):
    assert localize_mood(lang, mood) == xmood


@pytest.mark.parametrize(
    "lang,tense,xtense",
    [
        ("es", "present", "presente"),
        ("es", "gerund", "gerundio"),
        ("fr", "gerund", "participe-présent"),
    ],
)
def test_localize_tense(lang, tense, xtense):
    assert localize_tense(lang, tense) == xtense
