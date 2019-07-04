# -*- coding: utf-8 -*-

from mock import patch

import pytest

from verbecc.conjugation_template import (
    ConjugationTemplate, ConjugationTemplateError
)
from verbecc.conjugations_parser import (
    ConjugationsParser, ConjugationsParserError
)


def test_conjugations_parser():
    conj = ConjugationsParser()
    assert len(conj.templates) >= 132
    assert conj.impersonal_templates == [
    "adv:enir",
    "app:aroir",
    "brui:re",
    "brumass:er",
    "cha:loir",
    "cl:ore",
    "fa:lloir",
    "forclo:re",
    "fri:re",
    "grêl:er",
    "nei:ger",
    "pl:euvoir",
    "s:eoir",
    "s:ourdre",
    "éch:oir",
    "éclo:re"]

@patch('lxml.etree._Element')
def test_TemplateInvalidXML(mock_template_elem):
    mock_template_elem.tag.return_value = "not-template"
    with pytest.raises(ConjugationTemplateError):
        template = ConjugationTemplate(mock_template_elem)
