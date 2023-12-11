# -*- coding: utf-8 -*-

from lxml import etree
from verbecc.string_utils import strip_accents
from verbecc.exceptions import VerbsParserError

class Verb:
    def __init__(self, v_elem):
        if v_elem.tag != 'v':
            raise VerbsParserError("Unexpected element")
        try:
            self.predicted = False
            self.pred_score = 1.0
            self.infinitive = u'' + v_elem.find('i').text
            self.infinitive_no_accents = strip_accents(self.infinitive)
            self.template = u'' + v_elem.find('t').text
            self.translation_en = ''
            en_node = v_elem.find('en')
            if en_node is not None:
                self.translation_en = u'' + en_node.text
            self.impersonal = False
        except AttributeError as e:
            raise VerbsParserError(
                "Error parsing {}: {}".format(
                    etree.tostring(v_elem),
                    str(e)))

    def __repr__(self):
        return 'infinitive={} infinitive_no_accents={} template={} translation_en={} impersonal={} predicted={} pred_score={}'.format(
            self.infinitive, self.infinitive_no_accents, self.template, self.translation_en, self.impersonal, self.predicted, self.pred_score)
