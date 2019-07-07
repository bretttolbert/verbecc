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

    def _conjugate_simple_mood_tense(self, verb_stem, mood_name, 
                                     tense_template, is_reflexive=False):
        ret = []
        for person_ending in tense_template.person_endings:
            pronoun = self._get_default_pronoun(
                person_ending.get_person(), is_reflexive=is_reflexive)
            ending = person_ending.get_ending()

            conjugation = ''
            conjugated_verb = verb_stem + ending
            if pronoun[-1] == "e" and string_utils.starts_with_vowel(conjugated_verb):
                conjugation += pronoun[:-1] + "'"
            else:
                conjugation += pronoun + " "
            conjugation += conjugated_verb

            if mood_name == 'subjonctif':
                conjugation = prepend_with_que(conjugation)
            ret.append(conjugation)
        return ret
