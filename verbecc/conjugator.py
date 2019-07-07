# -*- coding: utf-8 -*-

from functools import partial as op

from . import parse_conjugations
from . import parse_verbs
from . import inflector

class ConjugatorError(Exception):
    pass

class InvalidMoodError(Exception):
    pass

class TemplateNotFoundError(Exception):
    pass

class VerbNotFoundError(Exception):
    pass

class Conjugator:
    def __init__(self, lang='fr'):
        self._inflector = inflector.Inflector(lang)
        
    def conjugate(self, infinitive):
        return do_op(op(self._inflector.conjugate, infinitive))

    def conjugate_mood(self, infinitive, mood_name):
        return do_op(op(self._inflector.conjugate_mood, infinitive))

    def conjugate_mood_tense(self, infinitive, mood_name, tense_name):
        return do_op(op(self._inflector.conjugate_mood_tense, 
            infinitive, mood_name, tense_name))

    def find_verb_by_infinitive(self, infinitive):
        return do_op(op(self._inflector.find_verb_by_infinitive, infinitive))

    def find_template(self, name):
        return do_op(op(self._inflector.find_template, name))

    def get_verbs_that_start_with(self, query, max_results):
        return self._inflector.get_verbs_that_start_with(query, max_results)

def do_op(op):
    ret = None
    try:
        ret = op()
    except inflector.ConjugatorError:
        raise ConjugatorError
    except inflector.InvalidMoodError:
        raise InvalidMoodError
    except parse_conjugations.TemplateNotFoundError:
        raise TemplateNotFoundError
    except parse_verbs.VerbNotFoundError:
        raise VerbNotFoundError
    return ret
