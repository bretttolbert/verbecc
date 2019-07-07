# -*- coding: utf-8 -*-

from .tense_template import TenseTemplate

class Mood():
    def __init__(self, mood_elem):
        self.name = mood_elem.tag
        self.tenses = {}
        for tense_elem in list(mood_elem):
            self.tenses[tense_elem.tag] = TenseTemplate(tense_elem)
