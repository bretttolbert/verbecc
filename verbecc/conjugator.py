# -*- coding: utf-8 -*-

from __future__ import print_function
import copy

from . import parse_conjugations
from . import parse_verbs
from . import grammar_defines
from . import string_utils

class ConjugatorError(Exception):
    pass

class InvalidMoodError(Exception):
    pass

class VerbNotFoundError(Exception):
    pass

class TemplateNotFoundError(Exception):
    pass

class Conjugator:
    def __init__(self, lang='fr'):
        self._verb_parser = parse_verbs.VerbsParser(lang)
        self._conj_parser = parse_conjugations.ConjugationsParser(lang)
        
    def conjugate(self, infinitive):
        co = self._get_conj_obs(infinitive)
        moods = {}
        for mood in co.template.moods:
            moods[mood] = self._conjugate_mood(co, mood)
        return {'verb': {'infinitive': co.verb.infinitive, 
                         'template': co.verb.template,
                         'translation_en': co.verb.translation_en,
                         'stem': co.verb_stem}, 
                'moods': moods}

    def conjugate_mood(self, infinitive, mood_name):
        co = self._get_conj_obs(infinitive)
        return self._conjugate_mood(co, mood_name)

    def conjugate_mood_tense(self, infinitive, mood_name, tense_name):
        co = self._get_conj_obs(infinitive)
        return self._conjugate_mood_tense(co, mood_name, tense_name)

    def find_verb_by_infinitive(self, infinitive):
        ret = None
        try:
            ret = self._verb_parser.find_verb_by_infinitive(infinitive)
        except parse_verbs.VerbNotFoundError:
            raise VerbNotFoundError
        return ret

    def find_template(self, name):
        ret = None
        try:
            ret = self._conj_parser.find_template(name)
        except parse_conjugations.TemplateNotFoundError:
            raise TemplateNotFoundError
        return ret

    def get_verbs_that_start_with(self, query, max_results):
        query = query.lower()
        is_reflexive, query = string_utils.split_reflexive(query)
        matches = self._verb_parser.get_verbs_that_start_with(query, max_results)
        if is_reflexive:
            matches = [string_utils.prepend_with_se(m) 
            for m in matches if self._verb_can_be_reflexive(m)]
        return matches

    #private:

    def _get_verb_stem(self, infinitive, template_name):
        template_beg, template_ending = template_name.split(u':')
        if not infinitive.endswith(template_ending):
            raise ConjugatorError(
                "Template {} ending doesn't "
                "match infinitive {}"
                .format(template_name, infinitive))
        return infinitive[:len(infinitive) - len(template_ending)]

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
            grammar_defines.VERBS_THAT_CANNOT_BE_REFLEXIVE_OTHER_THAN_IMPERSONAL_VERBS) 

    class ConjugationObjects:
        def __init__(self, infinitive, verb, template, verb_stem, is_reflexive):
            self.infinitive = infinitive
            self.verb = verb
            self.template = template
            self.verb_stem = verb_stem
            self.is_reflexive = is_reflexive

    def _get_conj_obs(self, infinitive):
        infinitive = infinitive.lower()
        is_reflexive, infinitive = string_utils.split_reflexive(infinitive)
        if is_reflexive and not self._verb_can_be_reflexive(infinitive):
            raise VerbNotFoundError("Verb cannot be reflexive")
        verb = self.find_verb_by_infinitive(infinitive)
        template = self.find_template(verb.template)
        verb_stem = self._get_verb_stem(verb.infinitive, template.name)
        return Conjugator.ConjugationObjects(
            infinitive, verb, template, verb_stem, is_reflexive)     

    def _conjugate_mood(self, co, mood_name):
        if mood_name not in co.template.moods:
            raise InvalidMoodError
        ret = {}
        ret.update(self._get_simple_conjugations_for_mood(co, mood_name))
        ret.update(self._get_compound_conjugations_for_mood(co, mood_name))
        return ret

    def _get_simple_conjugations_for_mood(self, co, mood_name):
        ret = {}
        mood = co.template.moods[mood_name]
        for tense_name, tense_template in mood.tenses.items():
            ret[tense_name] = self._conjugate_simple_mood_tense(
                co.verb_stem, mood_name, tense_template,
                co.is_reflexive)
        return ret

    def _get_compound_conjugations_for_mood(self, co, mood_name):
        ret = {}
        comp_conj_map = self._get_compound_conjugations_map()
        if mood_name in comp_conj_map:
            for tense_name in comp_conj_map[mood_name]:
                ret[tense_name] = self._conjugate_mood_tense(co, mood_name, tense_name)
        return ret

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
