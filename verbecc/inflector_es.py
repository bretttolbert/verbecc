# -*- coding: utf-8 -*-

from typing import Dict, List, Tuple

from verbecc import inflector

class InflectorEs(inflector.Inflector):

    @property
    def lang(self) -> str:
        return 'es'

    def __init__(self):
        super(InflectorEs, self).__init__()

    def _add_adverb_if_applicable(self, s: str, mood_name: str, tense_name: str) -> str:
        if mood_name == 'imperativo' and tense_name == 'negativo':
            return 'no ' + s
        return s

    def _get_default_pronoun(self, person: str, gender: str='m', is_reflexive: bool=False) -> str:
        ret = ''
        if person == '1s':
            ret = 'yo'
            if is_reflexive:
                ret += ' me'
        elif person == '2s':
            ret = 'tú'
            if is_reflexive:
                ret += ' te'
        elif person == '3s':
            ret = 'él'
            if gender == 'f':
                ret = 'ella'
            if is_reflexive:
                ret += ' se'
        elif person == '1p':
            ret = 'nosotros'
            if is_reflexive:
                ret += ' nos'
        elif person == '2p':
            ret = 'vosotros'
            if is_reflexive:
                ret += ' os'
        elif person == '3p':
            ret = 'ellos'
            if gender == 'f':
                ret = 'ellas'
            if is_reflexive:
                ret += ' se'
        return ret

    def _get_tenses_conjugated_without_pronouns(self) -> List[str]:
        return ['participo', 'gerundio', 'infinitivo', 'afirmativo', 'negativo']

    def _get_auxilary_verb(self, co: inflector.Inflector.ConjugationObjects, mood_name: str, tense_name: str) -> str:
        return 'haber'

    def _get_participle_mood_name(self) -> str:
        return 'participo'

    def _get_participle_tense_name(self) -> str:
        return 'participo'

    def _get_alternate_hv_inflection(self, s: str) -> str:
        if s.endswith('hay'):
            return s[:-1]
        return s

    def _get_compound_conjugations_aux_verb_map(self) -> Dict[str, Dict[str, Tuple[str, ...]]]:
        return {
            'indicativo': {
                'pretérito-perfecto-compuesto': ('indicativo', 'presente'),
                'pretérito-pluscuamperfecto': ('indicativo', 'pretérito-imperfecto'),
                'pretérito-anterior': ('indicativo', 'pretérito-perfecto-simple'),
                'futuro-perfecto': ('indicativo', 'futuro')
            },
            'condicional': {
                'perfecto': ('condicional', 'presente')
            },
            'subjuntivo': {
                'pretérito-perfecto': ('subjuntivo', 'presente'),
                'pretérito-pluscuamperfecto-1': ('subjuntivo', 'pretérito-imperfecto-1'),
                'pretérito-pluscuamperfecto-2': ('subjuntivo', 'pretérito-imperfecto-2'),
                'futuro-perfecto': ('subjuntivo', 'futuro')
            }
        }
