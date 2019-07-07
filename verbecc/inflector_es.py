# -*- coding: utf-8 -*-

from verbecc import inflector

class InflectorEs(inflector.Inflector):
    def __init__(self):
        self.lang = 'es'
        super(InflectorEs, self).__init__()

    def _get_default_pronoun(self, person, gender='m', is_reflexive=False):
        ret = ''
        if person == '1s':
            ret = 'je'
            if is_reflexive:
                ret += ' me'
        elif person == '2s':
            ret = 'tu'
            if is_reflexive:
                ret += ' te'
        elif person == '3s':
            ret = 'il'
            if gender == 'f':
                ret = 'elle'
            if is_reflexive:
                ret += ' se'
        elif person == '1p':
            ret = 'nous'
            if is_reflexive:
                ret += ' nous'
        elif person == '2p':
            ret = 'vous'
            if is_reflexive:
                ret += ' vous'
        elif person == '3p':
            ret = 'ils'
            if gender == 'f':
                ret = 'elles'
            if is_reflexive:
                ret += ' se'
        return ret

    def _conjugate_simple_mood_tense(self, verb_stem, mood_name, 
                                     tense_template, is_reflexive=False):
        return {}
