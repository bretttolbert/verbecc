# -*- coding: utf-8 -*-

from lxml import etree
from verbecc.string_utils import strip_accents
from verbecc.exceptions import VerbsParserError


class Verb:
    def __init__(self, v_elem: etree._Element):
        if v_elem.tag != "v":
            raise VerbsParserError("Unexpected element")
        try:
            self.predicted = False
            self.pred_score = 1.0
            self.infinitive = ""
            e = v_elem.find("i", None)
            if e is not None:
                self.infinitive: str = e.text if e.text is not None else ""
            self.infinitive_no_accents = strip_accents(self.infinitive)
            self.template = ""
            e = v_elem.find("t", None)
            if e is not None:
                self.template: str = e.text if e.text is not None else ""
            self.translation_en = ""
            e = v_elem.find("en", None)
            if e is not None:
                self.translation_en: str = e.text if e.text is not None else ""
            self.impersonal = False
        except AttributeError as e:
            raise VerbsParserError(
                "Error parsing {}: {}".format(etree.tostring(v_elem), str(e))
            )

    def __repr__(self) -> str:
        return "infinitive={} infinitive_no_accents={} template={} translation_en={} impersonal={} predicted={} pred_score={}".format(
            self.infinitive,
            self.infinitive_no_accents,
            self.template,
            self.translation_en,
            self.impersonal,
            self.predicted,
            self.pred_score,
        )
