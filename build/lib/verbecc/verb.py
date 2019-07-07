# -*- coding: utf-8 -*-

from lxml import etree
from . import string_utils
from . import exceptions

class Verb:
    def __init__(self, v_elem):
        if v_elem.tag != 'v':
            raise exceptions.VerbsParserError("Unexpected element")
        try:
            self.infinitive = u'' + v_elem.find('i').text
            self.infinitive_no_accents = \
                string_utils.strip_accents(self.infinitive)
            self.template = u'' + v_elem.find('t').text
            self.translation_en = ''
            en_node = v_elem.find('en')
            if en_node is not None:
                self.translation_en = u'' + en_node.text
            self.impersonal = False
        except AttributeError as e:
            raise exceptions.VerbsParserError(
                "Error parsing {}: {}".format(
                    etree.tostring(v_elem),
                    str(e)))
