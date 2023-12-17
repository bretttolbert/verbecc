# -*- coding: utf-8 -*-

from unittest.mock import patch

import pytest

from verbecc.conjugation_template import ConjugationTemplate
from verbecc.exceptions import ConjugationTemplateError

@patch('lxml.etree._Element')
def test_template_invalid_tag_template(mock_template_elem):
    mock_template_elem.tag.return_value = "not-template"
    with pytest.raises(ConjugationTemplateError):
        template = ConjugationTemplate(mock_template_elem)

@patch('lxml.etree._Element')
def test_template_invalid_tag_name(mock_template_elem):
    mock_template_elem.get.return_value = "not-name"
    with pytest.raises(ConjugationTemplateError):
        template = ConjugationTemplate(mock_template_elem)
