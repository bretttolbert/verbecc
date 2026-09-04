from unittest.mock import patch

import pytest

from verbecc.core.parsers.verb_parser import VerbParser
from verbecc.core.defs.types.exceptions import VerbsParserError
from verbecc.core.defs.types.lang_code import LangCodeISO639_1 as Lang


@patch("lxml.etree._Element")
def test_verb_invalid_xml(mock_v_elem):
    v = VerbParser()
    mock_v_elem.tag.return_value = "not-v"
    with pytest.raises(VerbsParserError):
        v.parse(mock_v_elem)
