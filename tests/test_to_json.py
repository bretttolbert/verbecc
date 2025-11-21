import pytest

from verbecc.src.conjugator.tense_conjugator import TenseConjugator
from verbecc.src.defs.types.tense import Tenses
from verbecc.src.defs.types.mood import Moods
from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang


@pytest.fixture(scope="module")
def tcg():
    tcg = TenseConjugator(lang=Lang.fr)
    yield tcg


def test_ensure_ascii(tcg):
    """
    Test to ensure json.dumps is being called with ensure_ascii=True

    With ensure_ascii=True:
        "que j\'eusse mangé"
    Without ensure_ascii=True:
        "que j\'eusse mang\\u00e9"
    """
    tc = tcg.conjugate_mood_tense(
        "manger", Moods.fr.Subjonctif, Tenses.fr.PlusQueParfait
    )
    c = tc[0]
    assert (
        c.to_json(indent=None, beautify=False)
        == '{"c": ["que j\'eusse mangé"], "g": null, "n": "s", "p": "1", "pr": "je"}'
    )
