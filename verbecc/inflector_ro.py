# -*- coding: utf-8 -*-

from verbecc import inflector

class InflectorRo(inflector.Inflector):
    def __init__(self):
        self.lang = 'ro'
        super(InflectorRo, self).__init__()

    def _add_adverb_if_applicable(self, s, mood_name, tense_name):
        if mood_name == 'imperativ' and tense_name == 'Imperativ-Negativ':
            return 'nu ' + s
        return s

    """TODO: There are two types of reflexive verbs in Romanian: 
    preceded by the reflexive pronouns “se” (in the accusative) and “și” (in the dative).
    """

    def _get_default_pronoun(self, person, gender='m', is_reflexive=False):
        ret = ''
        if person == '1s':
            ret = 'eu'
            if is_reflexive:
                ret += ' mă'
        elif person == '2s':
            ret = 'tu'
            if is_reflexive:
                ret += ' te'
        elif person == '3s':
            ret = 'el'
            if gender == 'f':
                ret = 'ea'
            if is_reflexive:
                ret += ' se'
        elif person == '1p':
            ret = 'noi'
            if is_reflexive:
                ret += ' ne'
        elif person == '2p':
            ret = 'voi'
            if is_reflexive:
                ret += ' vă'
        elif person == '3p':
            ret = 'ei'
            if gender == 'f':
                ret = 'ele'
            if is_reflexive:
                ret += ' se'
        return ret

    def _get_tenses_conjugated_without_pronouns(self):
        return ['Participiu', 
                'Infinitiv-Afirmativ', 
                'Imperativ-Imperativ', 'Imperativ-Negativ', 
                'Gerunziu-Gerunziu']

    def _get_helping_verb(self, infinitive):
        return 'avea'

    def _get_subjunctive_mood_name(self):
        return 'conjunctiv'

    def _get_participle_mood_name(self):
        return 'participiu'

    def _get_participle_tense_name(self):
        return 'Participiu'

    def _get_compound_conjugations_hv_map(self):
        return {
            'indicativo': {

            },
            'conjunctiv': {

            },
            'conditional': {

            },
            'infinitiv': {

            }
        }
