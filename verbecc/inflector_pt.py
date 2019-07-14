# -*- coding: utf-8 -*-

from verbecc import inflector

class InflectorPt(inflector.Inflector):
    def __init__(self):
        self.lang = 'pt'
        super(InflectorPt, self).__init__()

    def _add_subjunctive_relative_pronoun(self, s, tense_name):
        if tense_name == 'Conjuntivo--Subjuntivo-Presente':
            return 'que ' + s
        elif tense_name == 'Conjuntivo--Subjuntivo-Pretérito-Imperfeito':
            return 'se ' + s
        elif tense_name == 'Conjuntivo--Subjuntivo-Futuro-Simples':
            return 'quando ' + s
        return s

    def _get_default_pronoun(self, person, gender='m', is_reflexive=False):
        ret = ''
        if person == '1s':
            ret = 'eu'
            if is_reflexive:
                ret += ' me'
        elif person == '2s':
            ret = 'tu'
            if is_reflexive:
                ret += ' te'
        elif person == '3s':
            ret = 'ele'
            if gender == 'f':
                ret = 'ela'
            if is_reflexive:
                ret += ' se'
        elif person == '1p':
            ret = 'nós'
            if is_reflexive:
                ret += ' nos'
        elif person == '2p':
            ret = 'vós'
            if is_reflexive:
                ret += ' se'
        elif person == '3p':
            ret = 'eles'
            if gender == 'f':
                ret = 'elas'
            if is_reflexive:
                ret += ' se'
        return ret

    def _get_tenses_conjugated_without_pronouns(self):
        return ['Particípio-Particípio']

    def _get_helping_verb(self, infinitive):
        return 'ter'

    def _get_subjunctive_mood_name(self):
        return 'Conjuntivo'

    def _get_participle_mood_name(self):
        return 'Particípio'

    def _get_participle_tense_name(self):
        return 'Particípio-Particípio'

    def _get_compound_conjugations_hv_map(self):
        return {
            'Indicativo': {
                'Indicativo-Pretérito-Perfeito-Composto': 'Indicativo-presente',
                'Indicativo-Pretérito-Mais-que-Perfeito-Composto': 'Indicativo-pretérito-imperfeito',
                'Indicativo-Pretérito-Mais-que-Perfeito-Anterior': 'Indicativo-Pretérito-Mais-que-Perfeito-Simples',
                'Indicativo-Futuro-do-Presente-Composto': 'Indicativo-Futuro-do-Presente-Simples'
            },
            'Conjuntivo': {
                'Conjuntivo--Subjuntivo-Pretérito-Perfeito': 'Conjuntivo--Subjuntivo-Presente',
                'Conjuntivo--Subjuntivo-Pretérito-Mais-que-Perfeito': 'Conjuntivo--Subjuntivo-Pretérito-Imperfeito',
                'Conjuntivo--Subjuntivo-Futuro-Composto': 'Conjuntivo--Subjuntivo-Futuro-Simples'
            }
        }
