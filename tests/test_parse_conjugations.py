# -*- coding: utf-8 -*-

from mock import patch

import pytest

from verbecc.conjugation_template import ConjugationTemplate
from verbecc.exceptions import ConjugationTemplateError

@patch('lxml.etree._Element')
def test_TemplateInvalidXML(mock_template_elem):
    mock_template_elem.tag.return_value = "not-template"
    with pytest.raises(ConjugationTemplateError):
        template = ConjugationTemplate(mock_template_elem)
