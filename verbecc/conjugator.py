# -*- coding: utf-8 -*-

from . import inflector_fr
from . import inflector_es

SUPPORTED_LANGUAGES = {
    'fr': 'français',
    'es': 'español'
}

class Conjugator:
    def __init__(self, lang):
        if lang == 'fr':
            self._inflector = inflector_fr.InflectorFr()
        elif lang == 'es':
            self._inflector = inflector_es.InflectorEs()
        else:
            raise InvalidLangError
    
    def conjugate(self, infinitive):
        return self._inflector.conjugate(infinitive)

    def conjugate_mood(self, infinitive, mood_name):
        return self._inflector.conjugate_mood(infinitive, mood_name)

    def conjugate_mood_tense(self, infinitive, mood_name, tense_name):
        return self._inflector.conjugate_mood_tense( 
            infinitive, mood_name, tense_name)

    def get_verbs_list(self):
        return self._inflector.get_verbs_list()

    def get_templates_list(self):
        return self._inflector.get_templates_list()

    def find_verb_by_infinitive(self, infinitive):
        return self._inflector.find_verb_by_infinitive(infinitive)

    def find_template(self, name):
        return self._inflector.find_template(name)

    def get_verbs_that_start_with(self, query, max_results):
        return self._inflector.get_verbs_that_start_with(query, max_results)
