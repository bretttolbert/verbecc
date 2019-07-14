# -*- coding: utf-8 -*-

from verbecc import inflector

class InflectorEs(inflector.Inflector):
    def __init__(self):
        self.lang = 'es'
        super(InflectorEs, self).__init__()

    def _get_default_pronoun(self, person, gender='m', is_reflexive=False):
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

    def _get_tenses_conjugated_without_pronouns(self):
        return ['participo', 'gerundio', 'infinitivo', 'afirmativo', 'negativo']

    def _get_helping_verb(self, infinitive):
        return 'haber'

    def _get_participle_mood_name(self):
        return 'participo'

    def _get_participle_tense_name(self):
        return 'participo'

    def _get_alternate_hv_inflection(self, s):
        if s.endswith('hay'):
            return s[:-1]
        return s

    def _get_compound_conjugations_hv_map(self):
        return {
            'indicativo': {
                'pretérito-perfecto-compuesto': 'presente',
                'pretérito-pluscuamperfecto': 'pretérito-imperfecto',
                'pretérito-anterior': 'pretérito-perfecto-simple',
                'futuro-perfecto': 'futuro'
            },
            'condicional': {
                'perfecto': 'presente'
            },
            'subjuntivo': {
                'pretérito-perfecto': 'presente',
                'pretérito-pluscuamperfecto-1': 'pretérito-imperfecto-1',
                'pretérito-pluscuamperfecto-2': 'pretérito-imperfecto-2',
                'futuro-perfecto': 'futuro'
            }
        }
