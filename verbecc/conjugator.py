# -*- coding: utf-8 -*-

from typing import Dict, List

from verbecc import verb
from verbecc.exceptions import InvalidLangError
from verbecc import conjugation_template

from verbecc import (
    inflector_ca,
    inflector_es,
    inflector_fr,
    inflector_it,
    inflector_pt,
    inflector_ro)


SUPPORTED_LANGUAGES: Dict[str,str] = {
    'ca': 'català',
    'es': 'español',
    'fr': 'français',
    'it': 'italiano',
    'pt': 'português',
    'ro': 'română'
}

class Conjugator:
    """
    :param lang: two-letter language code
    """
    def __init__(self, lang: str):
        if lang == 'ca':
            self._inflector = inflector_ca.InflectorCa()
        elif lang == 'es':
            self._inflector = inflector_es.InflectorEs()
        elif lang == 'fr':
            self._inflector = inflector_fr.InflectorFr()
        elif lang == 'it':
            self._inflector = inflector_it.InflectorIt()
        elif lang == 'pt':
            self._inflector = inflector_pt.InflectorPt()
        elif lang == 'ro':
            self._inflector = inflector_ro.InflectorRo()
        else:
            raise InvalidLangError
    
    def conjugate(self, infinitive: str):
        return self._inflector.conjugate(infinitive)

    def conjugate_mood(self, infinitive: str, mood_name: str):
        return self._inflector.conjugate_mood(infinitive, mood_name)

    def conjugate_mood_tense(self, infinitive: str, mood_name: str, tense_name: str, alternate: bool=False):
        return self._inflector.conjugate_mood_tense( 
            infinitive, mood_name, tense_name, alternate)

    def get_verbs(self) -> List[verb.Verb]:
        return self._inflector.get_verbs()

    def get_infinitives(self) -> List[str]:
        return self._inflector.get_infinitives()

    def get_templates(self) -> List[conjugation_template.ConjugationTemplate]:
        return self._inflector.get_templates()

    def get_template_names(self) -> List[str]:
        return self._inflector.get_template_names()

    def find_verb_by_infinitive(self, infinitive: str) -> verb.Verb:
        return self._inflector.find_verb_by_infinitive(infinitive)

    def find_template(self, name: str) -> conjugation_template.ConjugationTemplate:
        return self._inflector.find_template(name)

    def get_verbs_that_start_with(self, query: str, max_results: int):
        return self._inflector.get_verbs_that_start_with(query, max_results)
