# -*- coding: utf-8 -*-

from . import inflector
from . import grammar_defines
from . import string_utils
from . import exceptions

VERBS_CONJUGATED_WITH_ETRE = [
"aller",
"arriver",
"descendre",
"redescendre",
"entrer",
"rentrer",
"monter",
"remonter",
"mourir",
"naître",
"renaître",
"partir",
"repartir",
"passer",
"rester",
"retourner",
"sortir",
"ressortir",
"tomber",
"retomber",
"venir",
"devenir",
"parvenir",
"revenir"]

VERBS_THAT_CANNOT_BE_REFLEXIVE_OTHER_THAN_IMPERSONAL_VERBS = [
"être",
"aller",
"avoir"]


class InflectorFr(inflector.Inflector):
    def __init__(self):
        self.lang = 'fr'
        super(InflectorFr, self).__init__()

    def get_verbs_that_start_with(self, query, max_results):
        query = query.lower()
        is_reflexive, query = self._split_reflexive(query)
        matches = self._verb_parser.get_verbs_that_start_with(query, max_results)
        if is_reflexive:
            matches = [self._prepend_with_se(m) 
            for m in matches if self._verb_can_be_reflexive(m)]
        return matches

    def _is_impersonal_verb(self, infinitive):
        ret = False
        verb = self.find_verb_by_infinitive(infinitive)
        template = self.find_template(verb.template)
        if len(template.moods['indicatif'].tenses['présent'].person_endings) < 6:
            ret = True
        return ret

    def _verb_can_be_reflexive(self, infinitive):
        return (not self._is_impersonal_verb(infinitive) 
            and infinitive not in 
            VERBS_THAT_CANNOT_BE_REFLEXIVE_OTHER_THAN_IMPERSONAL_VERBS) 

    def _split_reflexive(self, infinitive):
        is_reflexive = False
        if infinitive.startswith("se "):
            is_reflexive = True
            infinitive = infinitive[3:]
        elif infinitive.startswith("s'"):
            is_reflexive = True
            infinitive = infinitive[2:]
        return is_reflexive, infinitive

    def _add_subjunctive_relative_pronoun(self, s, tense_name):
        if string_utils.starts_with_vowel(s):
            return "qu'" + s
        else:
            return "que " + s

    def _prepend_with_se(self, s):
        if string_utils.starts_with_vowel(s):
            return "s'" + s
        else:
            return "se " + s

    def _get_pronoun_suffix(self, person, gender='m'):
        return '-' + self._get_default_pronoun(person, gender).replace('tu', 'toi')

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

    def _get_tenses_conjugated_without_pronouns(self):
        return ['infinitif-présent', 'participe-présent', 
                'imperatif-présent', 'participe-passé']

    def _get_helping_verb(self, co):
        ret = 'avoir'
        if (co.verb.infinitive in VERBS_CONJUGATED_WITH_ETRE
            or co.is_reflexive):
            ret = 'être'
        return ret

    def _is_helping_verb_inflected(self, helping_verb):
        return helping_verb == 'être'

    def _get_subjunctive_mood_name(self):
        return 'subjonctif'

    def _get_participle_mood_name(self):
        return 'participe'

    def _get_participle_tense_name(self):
        return 'participe-passé'

    def _combine_pronoun_and_conj(self, pronoun, conj):
        ret = ''
        if pronoun[-1] == "e" and string_utils.starts_with_vowel(conj):
            ret += pronoun[:-1] + "'"
        else:
            ret += pronoun + " "
        ret += conj
        return ret

    def _add_present_participle_if_applicable(self, s, is_reflexive, tense_name):
        ret = s
        if is_reflexive and tense_name == self._get_participle_tense_name():
            ret += 'étant '
        return ret

    def _add_reflexive_pronoun_or_pronoun_suffix_if_applicable(self, s, is_reflexive, mood_name, person):
        if is_reflexive:
            if mood_name != 'imperatif':
                s = self._prepend_with_se(s)
            else:
                s += self._get_pronoun_suffix(person)
        return s

    def _get_compound_conjugations_hv_map(self):
        return {
            'indicatif': {
                'passé-composé': 'présent',
                'plus-que-parfait': 'imparfait',
                'futur-antérieur': 'futur-simple',
                'passé-antérieur': 'passé-simple'
            },
            'subjonctif': {
                'passé': 'présent',
                'plus-que-parfait': 'imparfait'
            },
            'conditionnel': {
                'passé': 'présent'
            },
            'imperatif': {
                'imperatif-passé': 'imperatif-présent'
            }
        }
