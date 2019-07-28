# -*- coding: utf-8 -*-

from . import (
    inflector_fr,
    inflector_es,
    inflector_it,
    inflector_pt,
    inflector_ro)


SUPPORTED_LANGUAGES = {
    'fr': 'français',
    'es': 'español',
    'it': 'italiano',
    'pt': 'português',
    'ro': 'română'
}

class Conjugator:
    """
    :param lang: two-letter language code
    """
    def __init__(self, lang):
        if lang == 'fr':
            self._inflector = inflector_fr.InflectorFr()
        elif lang == 'es':
            self._inflector = inflector_es.InflectorEs()
        elif lang == 'it':
            self._inflector = inflector_it.InflectorIt()
        elif lang == 'pt':
            self._inflector = inflector_pt.InflectorPt()
        elif lang == 'ro':
            self._inflector = inflector_ro.InflectorRo()
        else:
            raise InvalidLangError
    
    def conjugate(self, infinitive):
        return self._inflector.conjugate(infinitive)

    def conjugate_mood(self, infinitive, mood_name):
        return self._inflector.conjugate_mood(infinitive, mood_name)

    def conjugate_mood_tense(self, infinitive, mood_name, tense_name, alternate=False):
        return self._inflector.conjugate_mood_tense( 
            infinitive, mood_name, tense_name, alternate)

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
