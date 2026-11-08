from unittest.mock import MagicMock, patch

import pytest

from verbecc.core.parsers.conjugation_template_parser import ConjugationTemplateParser
from verbecc.core.defs.types.exceptions import ConjugationTemplateError
from verbecc.core.defs.types.lang_code import LangCodeISO639_1 as Lang


@patch("lxml.etree._Element")
def test_template_invalid_tag_template(mock_template_elem: MagicMock):
    mock_template_elem.tag.return_value = "not-template"
    with pytest.raises(ConjugationTemplateError):
        ConjugationTemplateParser(Lang.fr).parse(mock_template_elem)


@patch("lxml.etree._Element")
def test_template_invalid_tag_name(mock_template_elem: MagicMock):
    mock_template_elem.get.return_value = "not-name"
    with pytest.raises(ConjugationTemplateError):
        ConjugationTemplateParser(Lang.ca).parse(mock_template_elem)
