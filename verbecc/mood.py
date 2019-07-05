# -*- coding: utf-8 -*-

from .tense_template import TenseTemplate


MOOD_TENSES = {
    'infinitive': ['infinitive-present'],
    'indicative': ['present', 'imperfect', 'future', 'simple-past'],
    'conditional': ['present'],
    'subjunctive': ['present', 'imperfect'],
    'imperative': ['imperative-present'],
    'participle': ['present-participle', 'past-participle']
}


def is_valid_mood(mood_name):
    return mood_name in MOOD_TENSES


def is_valid_mood_tense(mood_name, tense_name):
    return mood_name in MOOD_TENSES and tense_name in MOOD_TENSES[mood_name]


class MoodError(Exception):
    pass

class Mood():
    """
    name
        the name of the mood, e.g. "indicative"
    mood_elem
        contains one or more tense_elems (see class TenseTemplate) with
        tag names as listed in MOOD_TENSES
    """
    def __init__(self, mood_elem):
        self.name = mood_elem.tag
        self.tenses = {}
        for tense_elem in list(mood_elem):
            self.tenses[tense_elem.tag] = TenseTemplate(tense_elem)
