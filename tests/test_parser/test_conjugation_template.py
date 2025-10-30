from unittest.mock import patch

import pytest

from verbecc.src.parsers.conjugation_template_parser import ConjugationTemplateParser
from verbecc.src.defs.types.exceptions import ConjugationTemplateError
from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang


@patch("lxml.etree._Element")
def test_template_invalid_tag_template(mock_template_elem):
    mock_template_elem.tag.return_value = "not-template"
    with pytest.raises(ConjugationTemplateError):
        template = ConjugationTemplateParser(Lang.fr).parse(mock_template_elem)


@patch("lxml.etree._Element")
def test_template_invalid_tag_name(mock_template_elem):
    mock_template_elem.get.return_value = "not-name"
    with pytest.raises(ConjugationTemplateError):
        template = ConjugationTemplateParser(Lang.ca).parse(mock_template_elem)
