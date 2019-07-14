# -*- coding: utf-8 -*-

from .tense_template import TenseTemplate

class Mood():
    def __init__(self, mood_elem):
        self.name = mood_elem.tag.lower()
        self.tenses = {}
        for tense_elem in mood_elem:
            self.tenses[tense_elem.tag] = TenseTemplate(tense_elem)
