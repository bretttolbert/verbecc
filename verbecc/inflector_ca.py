# -*- coding: utf-8 -*-

from typing import Dict, List, Tuple

from verbecc import inflector

class InflectorCa(inflector.Inflector):

    @property
    def lang(self) -> str:
        return 'ca'

    def __init__(self):
        super(InflectorCa, self).__init__()

    def _add_adverb_if_applicable(self, s: str, mood_name: str, tense_name: str) -> str:
        return s

    def _get_default_pronoun(self, person: str, gender: str='m', is_reflexive: bool=False) -> str:
        ret = ''
        if person == '1s':
            ret = 'jo'
            if is_reflexive:
                ret += ' me'
        elif person == '2s':
            ret = 'tu'
            if is_reflexive:
                ret += ' te'
        elif person == '3s':
            ret = 'ell'
            if gender == 'f':
                ret = 'ella'
            if is_reflexive:
                ret += ' se'
        elif person == '1p':
            ret = 'nosaltres'
            if is_reflexive:
                ret += ' nos'
        elif person == '2p':
            ret = 'vosaltres'
            if is_reflexive:
                ret += ' os'
        elif person == '3p':
            ret = 'ells'
            if gender == 'f':
                ret = 'elles'
            if is_reflexive:
                ret += ' se'
        return ret

    def _get_tenses_conjugated_without_pronouns(self) -> List[str]:
        return ['particip', 'gerundi', 'infinitiu-present', 'imperatiu-present']

    def _get_auxilary_verb(self, co: inflector.Inflector.ConjugationObjects, mood_name: str, tense_name: str) -> str:
        return 'haver'

    def _get_participle_mood_name(self) -> str:
        return 'particip'

    def _get_participle_tense_name(self) -> str:
        return 'particip'

    def _get_alternate_hv_inflection(self, s: str) -> str:
        # if s.endswith('hay'):
        #     return s[:-1]
        return s

    def _get_compound_conjugations_aux_verb_map(self) -> Dict[str, Dict[str, Tuple[str, ...]]]:
        """
        return {
            'indicatiu': {
                'pretèrit-perfet-compuest': ('indicatiu', 'present'),
                'pretèrit-pluscuamperfet': ('indicatiu', 'imperfet'),
                'pretèrit-anterior': ('indicatiu', 'pretèrit'),
                'futur-perfet': ('indicatiu', 'futuro')
            },
            'condicional': {
                'perfet': ('condicional', 'present')
            },
            'subjuntiu': {
                'pretèrit-perfet': ('subjuntiu', 'present'),
                'pretèrit-pluscuamperfet': ('subjuntiu', 'imperfet'),
                'futur-perfet': ('subjuntiu', 'futur')
            }
        }
        """
        return {}
