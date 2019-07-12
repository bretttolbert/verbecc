# -*- coding: utf-8 -*-

from mock import patch

import pytest

from verbecc import parse_verbs
from verbecc import verb
from verbecc import exceptions

def test_verbs_parser():
    vp = parse_verbs.VerbsParser()
    assert len(vp.verbs) >= 7000

def test_verb():
    vp = parse_verbs.VerbsParser()
    verb = vp.find_verb_by_infinitive("manger")
    assert verb.infinitive == "manger"
    assert verb.template == "man:ger"
    assert verb.translation_en == "eat"

def test_verb_two():
    vp = parse_verbs.VerbsParser()
    verb = vp.find_verb_by_infinitive("abattre")
    assert verb.infinitive == "abattre"
    assert verb.template == "bat:tre"
    assert verb.translation_en == "tear down"

@patch('lxml.etree._Element')
def test_verb_invalid_xml(mock_v_elem):
    mock_v_elem.tag.return_value = "not-v"
    with pytest.raises(exceptions.VerbsParserError):
        v = verb.Verb(mock_v_elem)

test_data = [
    ("mang", ['mangeotter', 'manger']),
    ("Mang", ['mangeotter', 'manger']),
]

@pytest.mark.parametrize("query,expected_matches", test_data)
def test_get_verbs_that_start_with(query, expected_matches):
    vp = parse_verbs.VerbsParser()
    matches = vp.get_verbs_that_start_with(query)
    assert matches == expected_matches
