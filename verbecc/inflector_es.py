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
        return ['Participo-Participo']

    def _get_helping_verb(self, infinitive):
        return 'haber'

    def _get_participle_mood_name(self):
        return 'Participo'

    def _get_participle_tense_name(self):
        return 'Participo-Participo'

    def _get_compound_conjugations_hv_map(self):
        return {
            'Indicativo': {
                'Indicativo-pretérito-perfecto-compuesto': 'Indicativo-presente'
            }
        }
