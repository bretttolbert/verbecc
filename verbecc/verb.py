# -*- coding: utf-8 -*-

from lxml import etree
from .string_utils import strip_accents

class VerbsParserError(SyntaxError):
    pass


class Verb:
    def __init__(self, v_elem):
        if v_elem.tag != 'v':
            raise VerbsParserError("parse_verb: not a 'v' elem")
        try:
            self.infinitive = u'' + v_elem.find('i').text
            self.infinitive_no_accents = strip_accents(self.infinitive)
            self.template = u'' + v_elem.find('t').text
            self.translation_en = u'' + v_elem.find('en').text
            self.impersonal = False
        except AttributeError as e:
            raise VerbsParserError(
                "Error parsing {}: {}".format(
                    etree.tostring(v_elem),
                    str(e)))
