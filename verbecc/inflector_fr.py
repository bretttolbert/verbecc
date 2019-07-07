import copy

from . import inflector
from . import parse_conjugations
from . import parse_verbs
from . import grammar_defines
from . import string_utils
from . import exceptions

class InflectorFr(inflector.Inflector):
    def __init__(self):
        self.lang = 'fr'
        self._verb_parser = parse_verbs.VerbsParser(self.lang)
        self._conj_parser = parse_conjugations.ConjugationsParser(self.lang)

    def _get_compound_conjugations_map(self):
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

    def _conjugate_mood_tense(self, co, mood_name, tense_name):
        comp_conj_map = self._get_compound_conjugations_map()
        if tense_name in comp_conj_map[mood_name]:
            hv_tense_name = comp_conj_map[mood_name][tense_name]
            return self._conjugate_compound(co, mood_name, hv_tense_name)
        else:
            tense_template = co.template.moods[mood_name].tenses[tense_name]
            return self._conjugate_simple_mood_tense(
                co.verb_stem, mood_name, tense_template,
                co.is_reflexive)

    def _conjugate_compound(self, co, mood_name, hv_tense_name):
        """Conjugate a compound tense
        Args:
            co: ConjugationObjects for the verb being conjugated
            mood_name: mood verb is being conjugated in
            hv_tense_name: tense_name for conjugating helping verb
        """
        ret = []
        if (co.is_reflexive and mood_name == 'imperatif' 
            and hv_tense_name == 'imperatif-présent'):
            return ret
        persons = [pe.person for pe in 
            co.template.moods[mood_name].tenses[hv_tense_name].person_endings]
        helping_verb = 'avoir'
        if (co.verb.infinitive in grammar_defines.VERBS_CONJUGATED_WITH_ETRE
            or co.is_reflexive):
            helping_verb = 'être'
        hvco = self._get_conj_obs(helping_verb)
        hvtense_template = copy.deepcopy(
            hvco.template.moods[mood_name].tenses[hv_tense_name])
        hvperson_endings = []
        for pe in hvtense_template.person_endings:
            if pe.person in persons:
                hvperson_endings.append(pe)
        hvtense_template.person_endings = hvperson_endings
        hvconj = self._conjugate_simple_mood_tense(
            hvco.verb_stem, 
            'indicatif', 
            hvtense_template,
            co.is_reflexive)
        participle = self._conjugate_simple_mood_tense(
            co.verb_stem, 
            'participe', 
            co.template.moods['participe'].tenses['participe-passé'])
        if helping_verb == 'avoir':
            for hv in hvconj:
                p = participle[0]
                ret.append(hv + ' ' + p)
        else:
            for i, hv in enumerate(hvconj):
                participle_inflection = \
                    grammar_defines.get_default_participle_inflection_for_person(persons[i])
                p = participle[grammar_defines.PARTICIPLE_INFLECTIONS.index(participle_inflection)]
                ret.append(hv + ' ' + p)
        if mood_name == 'subjonctif':
            ret = [string_utils.prepend_with_que(i) for i in ret]
        return ret

    def _conjugate_simple_mood_tense(self, verb_stem, mood_name, 
                                  tense_template, is_reflexive=False):
        ret = []
        if tense_template.name in grammar_defines.TENSES_CONJUGATED_WITHOUT_PRONOUNS:
            for person_ending in tense_template.person_endings:
                conj = ''
                if is_reflexive and tense_template.name == 'participe-passé':
                    conj += 'étant '
                conj += verb_stem + person_ending.get_ending()
                if is_reflexive:
                    if mood_name != 'imperatif':
                        conj = string_utils.prepend_with_se(conj)
                    else:
                        conj += grammar_defines.get_pronoun_suffix(person_ending.get_person())
                ret.append(conj)
        else:
            for person_ending in tense_template.person_endings:
                pronoun = grammar_defines.get_default_pronoun(
                    person_ending.get_person(), is_reflexive)
                ending = person_ending.get_ending()
                conjugation = self._conjugate_simple_mood_tense_pronoun(
                    verb_stem, ending, pronoun)
                if mood_name == 'subjonctif':
                    conjugation = string_utils.prepend_with_que(conjugation)
                ret.append(conjugation)
        return ret

    def _conjugate_simple_mood_tense_pronoun(self, verb_stem, ending, pronoun):
        ret = u''
        conjugated_verb = verb_stem + ending
        if pronoun[-1] == "e" and string_utils.starts_with_vowel(conjugated_verb):
            ret += pronoun[:-1] + "'"
        else:
            ret += pronoun + " "
        ret += conjugated_verb
        return ret