from unittest.mock import patch

import pytest

from verbecc.src.parsers.verbs_parser import VerbsParser
from verbecc.src.defs.types.data.verbs import Verbs
from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang


@pytest.fixture(scope="module")
def verbs():
    vp = VerbsParser(Lang.fr)
    verbs = vp.parse()
    yield verbs


def test_verb(verbs):
    verb = verbs.find_verb_by_infinitive("manger")
    assert verb.infinitive == "manger"
    assert verb.template == "man:ger"
    assert verb.translation_en == "eat"


def test_verb_two(verbs):
    verb = verbs.find_verb_by_infinitive("abattre")
    assert verb.infinitive == "abattre"
    assert verb.template == "bat:tre"
    assert verb.translation_en == "tear down"


@pytest.mark.parametrize(
    "query,expected_matches",
    [
        ("mang", ["mangeotter", "manger"]),
        ("Mang", ["mangeotter", "manger"]),
    ],
)
def test_get_verbs_that_start_with(query, expected_matches, verbs):
    matches = verbs.get_verbs_that_start_with(query)
    assert matches == expected_matches
