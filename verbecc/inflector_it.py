# -*- coding: utf-8 -*-

from verbecc import inflector

class InflectorIt(inflector.Inflector):
    def __init__(self):
        self.lang = 'it'
        super(InflectorIt, self).__init__()

    def _split_reflexive(self, infinitive):
        is_reflexive = False
        if infinitive.startswith("si "):
            is_reflexive = True
            infinitive = infinitive[3:]
        elif infinitive.startswith("s'"):
            is_reflexive = True
            infinitive = infinitive[2:]
        return is_reflexive, infinitive

    def _add_reflexive_pronoun(self, s):
        if string_utils.starts_with_vowel(s):
            return "s'" + s
        else:
            return "si " + s

    def _add_subjunctive_relative_pronoun(self, s, tense_name):
        return 'che ' + s

    def _get_default_pronoun(self, person, gender='m', is_reflexive=False):
        ret = ''
        if person == '1s':
            ret = 'io'
            if is_reflexive:
                ret = 'mi'
        elif person == '2s':
            ret = 'tu'
            if is_reflexive:
                ret = 'ti'
        elif person == '3s':
            ret = 'lui'
            if gender == 'f':
                ret = 'lei'
            if is_reflexive:
                ret = 'si'
        elif person == '1p':
            ret = 'noi'
            if is_reflexive:
                ret = 'ci'
        elif person == '2p':
            ret = 'voi'
            if is_reflexive:
                ret = 'vi'
        elif person == '3p':
            ret = 'loro'
            if is_reflexive:
                ret = 'si'
        return ret

    def _get_tenses_conjugated_without_pronouns(self):
        return ['Imperativo-Affermativo', 'Imperativo-Non', 
                'Infinito--Gerundio', 'Participio-Participio']

    def _get_helping_verb(self, infinitive):
        return 'avere'

    def _get_subjunctive_mood_name(self):
        return 'Congiuntivo'

    def _get_participle_mood_name(self):
        return 'Participio'

    def _get_participle_tense_name(self):
        return 'Participio-Participio'

    def _get_compound_conjugations_hv_map(self):
        return {
            'indicativo': {
                'Indicativo-passato-prossimo': 'Indicativo-presente',
                'Indicativo-trapassato-prossimo': 'Indicativo-imperfetto',
                'Indicativo-trapassato-remoto': 'Indicativo-passato-remoto',
                'Indicativo-futuro-anteriore': 'Indicativo-futuro-semplice'
            },
            'congiuntivo': {
                'Congiuntivo-passato': 'Congiuntivo-presente',
                'Congiuntivo-trapassato': 'Congiuntivo-imperfetto'
            },
            'condizionale': {
                'Condizionale-passato': 'Condizionale-presente'
            }
        }
