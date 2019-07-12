# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import copy

from . import grammar_defines
from . import string_utils
from . import exceptions
from . import parse_verbs
from . import parse_conjugations

class Inflector(ABC):
    def __init__(self):
        self._verb_parser = parse_verbs.VerbsParser(self.lang)
        self._conj_parser = parse_conjugations.ConjugationsParser(self.lang)

    def conjugate(self, infinitive):
        co = self._get_conj_obs(infinitive)
        moods = {}
        for mood in co.template.moods:
            moods[mood] = self._conjugate_mood(co, mood)
        return {'verb': {'infinitive': co.verb.infinitive, 
                         'predicted': co.verb.predicted,
                         'pred_score': co.verb.pred_score,
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

    def get_verbs_list(self):
        return [v.infinitive for v in self._verb_parser.verbs]

    def get_templates_list(self):
        return [t.name for t in self._conj_parser.templates]

    def find_verb_by_infinitive(self, infinitive):
        return self._verb_parser.find_verb_by_infinitive(infinitive)

    def find_template(self, name):
        return self._conj_parser.find_template(name)

    def get_verbs_that_start_with(self, query, max_results):
        query = query.lower()
        matches = self._verb_parser.get_verbs_that_start_with(query, max_results)
        return matches

    def _get_verb_stem(self, infinitive, template_name):
        template_beg, template_ending = template_name.split(u':')
        if not infinitive.endswith(template_ending):
            raise exceptions.ConjugatorError(
                "Template {} ending doesn't "
                "match infinitive {}"
                .format(template_name, infinitive))
        return infinitive[:len(infinitive) - len(template_ending)]

    def _is_impersonal_verb(self, infinitive):
        return False

    def _verb_can_be_reflexive(self, infinitive):
        return not self._is_impersonal_verb(infinitive)

    def _split_reflexive(self, infinitive):
        return (False, infinitive)

    def _prepend_with_que(self, pronoun_string):
        if string_utils.starts_with_vowel(pronoun_string):
            return "qu'" + pronoun_string
        else:
            return "que " + pronoun_string

    def _prepend_with_se(self, s):
        if string_utils.starts_with_vowel(s):
            return "s'" + s
        else:
            return "se " + s

    class ConjugationObjects:
        def __init__(self, infinitive, verb, template, verb_stem, is_reflexive):
            self.infinitive = infinitive
            self.verb = verb
            self.template = template
            self.verb_stem = verb_stem
            self.is_reflexive = is_reflexive

    def _get_conj_obs(self, infinitive):
        infinitive = infinitive.lower()
        is_reflexive, infinitive = self._split_reflexive(infinitive)
        if is_reflexive and not self._verb_can_be_reflexive(infinitive):
            raise exceptions.VerbNotFoundError("Verb cannot be reflexive")
        verb = self.find_verb_by_infinitive(infinitive)
        template = self.find_template(verb.template)
        verb_stem = self._get_verb_stem(verb.infinitive, template.name)
        return Inflector.ConjugationObjects(
            infinitive, verb, template, verb_stem, is_reflexive)     

    def _conjugate_mood(self, co, mood_name):
        if mood_name not in co.template.moods:
            raise exceptions.InvalidMoodError
        ret = {}
        ret.update(self._get_simple_conjugations_for_mood(co, mood_name))
        ret.update(self._get_compound_conjugations_for_mood(co, mood_name))
        return ret

    def _get_simple_conjugations_for_mood(self, co, mood_name):
        ret = {}
        mood = co.template.moods[mood_name]
        for tense_name in mood.tenses:
            ret[tense_name] = self._conjugate_mood_tense(co, mood_name, tense_name)
        return ret

    def _get_compound_conjugations_for_mood(self, co, mood_name):
        ret = {}
        comp_conj_map = self._get_compound_conjugations_hv_map()
        if mood_name in comp_conj_map:
            for tense_name in comp_conj_map[mood_name]:
                ret[tense_name] = self._conjugate_mood_tense(co, mood_name, tense_name)
        return ret

    def _conjugate_mood_tense(self, co, mood_name, tense_name):
        comp_conj_map = self._get_compound_conjugations_hv_map()
        if mood_name in comp_conj_map and tense_name in comp_conj_map[mood_name]:
            hv_tense_name = comp_conj_map[mood_name][tense_name]
            return self._conjugate_compound(co, mood_name, hv_tense_name)
        else:
            mood = co.template.moods[mood_name]
            if tense_name not in mood.tenses:
                raise exceptions.InvalidTenseError
            tense_template = mood.tenses[tense_name]
            return self._conjugate_simple_mood_tense(
                co.verb_stem, mood_name, tense_template,
                co.is_reflexive)

    def _get_tenses_conjugated_without_pronouns(self):
        return []

    def _get_helping_verb(self, co):
        return ''

    def _is_helping_verb_inflected(self, helping_verb):
        return False

    def _get_participle_mood_name(self):
        return 'partiple'

    def _get_participle_tense_name(self):
        return 'past-participle'

    def _get_compound_conjugations_hv_map(self):
        """"Returns a map of the tense of the helping verb for each compound mood and tense"""
        return {}

    def _conjugate_compound(self, co, mood_name, hv_tense_name):
        """Conjugate a compound tense
        Args:
            co: ConjugationObjects for the verb being conjugated
            mood_name: mood verb is being conjugated in
            hv_tense_name: tense_name for conjugating helping verb
        """
        return {}

    def _get_default_participle_inflection_for_person(self, person):
        if person[1] == 's':
            return 'ms'
        else:
            return 'mp'

    def _get_default_pronoun(self, person, gender='m', is_reflexive=False):
        return ''

    def _conjugate_simple_mood_tense(self, verb_stem, mood_name, 
                                     tense_template, is_reflexive=False):
        ret = []
        if tense_template.name in self._get_tenses_conjugated_without_pronouns():
            for person_ending in tense_template.person_endings:
                conj = ''
                if self.lang == 'fr' and is_reflexive and tense_template.name == 'participe-passé':
                    conj += 'étant '
                conj += verb_stem + person_ending.get_ending()
                if is_reflexive:
                    if self.lang == 'fr' and mood_name != 'imperatif':
                        conj = self._prepend_with_se(conj)
                    else:
                        conj += self._get_pronoun_suffix(person_ending.get_person())
                ret.append(conj)
        else:
            for person_ending in tense_template.person_endings:
                pronoun = self._get_default_pronoun(
                    person_ending.get_person(), is_reflexive=is_reflexive)
                ending = person_ending.get_ending()

                conjugation = ''
                conjugated_verb = verb_stem + ending
                if self.lang == 'fr' and pronoun[-1] == "e" and string_utils.starts_with_vowel(conjugated_verb):
                    conjugation += pronoun[:-1] + "'"
                else:
                    conjugation += pronoun + " "
                conjugation += conjugated_verb

                if self.lang == 'fr' and mood_name == 'subjonctif':
                    conjugation = self._prepend_with_que(conjugation)
                ret.append(conjugation)
        return ret

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
        helping_verb = self._get_helping_verb(co)
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
            '', 
            hvtense_template,
            co.is_reflexive)
        pmood = self._get_participle_mood_name()
        ptense = self._get_participle_tense_name()
        participle = self._conjugate_simple_mood_tense(
            co.verb_stem, 
            pmood, 
            co.template.moods[pmood].tenses[ptense])
        if not self._is_helping_verb_inflected(helping_verb):
            for hv in hvconj:
                p = participle[0]
                if self.lang == 'es' and hv == 'él hay':
                    hv = 'él ha'
                ret.append(hv + ' ' + p)
        else:
            for i, hv in enumerate(hvconj):
                participle_inflection = \
                    self._get_default_participle_inflection_for_person(
                        persons[i])
                p = participle[
                    grammar_defines.PARTICIPLE_INFLECTIONS.index(
                        participle_inflection)]
                ret.append(hv + ' ' + p)
        if mood_name == 'subjonctif':
            ret = [self._prepend_with_que(i) for i in ret]
        return ret
