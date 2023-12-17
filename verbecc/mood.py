# -*- coding: utf-8 -*-

from lxml import etree
from typing import Dict

from verbecc.tense_template import TenseTemplate

class Mood():
    def __init__(self, mood_elem: etree._Element):
        self.name = mood_elem.tag.lower()
        self.tenses: Dict[str, TenseTemplate] = {}
        for tense_elem in mood_elem:
            self.tenses[tense_elem.tag] = TenseTemplate(tense_elem)

    def __repr__(self):
        return 'name={} tenses={}'.format(self.name, self.tenses)
