# -*- coding: utf-8 -*-

from mock import patch

import pytest

from verbecc.verbs_parser import (
    Verb,
    VerbNotFoundError,
    VerbsParser,
    VerbsParserError
)


def test_verbs_parser():
    vp = VerbsParser()
    assert len(vp.verbs) >= 7000


def test_verb():
    vp = VerbsParser()
    verb = vp.find_verb_by_infinitive("manger")
    assert verb.infinitive == "manger"
    assert verb.template == "man:ger"
    assert verb.translation_en == "eat"


def test_verb_two():
    vp = VerbsParser()
    verb = vp.find_verb_by_infinitive("abattre")
    assert verb.infinitive == "abattre"
    assert verb.template == "bat:tre"
    assert verb.translation_en == "tear down"


def test_verb_not_found():
    vp = VerbsParser()
    with pytest.raises(VerbNotFoundError):
        verb = vp.find_verb_by_infinitive("foo")


@patch('lxml.etree._Element')
def test_verb_invalid_xml(mock_v_elem):
    mock_v_elem.tag.return_value = "not-v"
    with pytest.raises(VerbsParserError):
        v = Verb(mock_v_elem)


test_data = [
    ("mang", ['mangeotter', 'manger']),
    ("Mang", ['mangeotter', 'manger']),
]

@pytest.mark.parametrize("query,expected_matches", test_data)
def test_get_verbs_that_start_with(query, expected_matches):
    vp = VerbsParser()
    matches = vp.get_verbs_that_start_with(query)
    assert matches == expected_matches
