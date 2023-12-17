# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import copy
from typing import Dict, List, Tuple

from verbecc import grammar_defines
from verbecc import exceptions
from verbecc import conjugations_parser
from verbecc import conjugation_template
from verbecc import verb
from verbecc import verbs_parser

class Inflector(ABC):
    
    @property
    @abstractmethod
    def lang(self) -> str:
        pass

    def __init__(self):
        self._verb_parser = verbs_parser.VerbsParser(self.lang)
        self._conj_parser = conjugations_parser.ConjugationsParser(self.lang)

    def conjugate(self, infinitive: str):
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

    def conjugate_mood(self, infinitive: str, mood_name: str):
        co = self._get_conj_obs(infinitive)
        return self._conjugate_mood(co, mood_name)

    def conjugate_mood_tense(self, infinitive: str, mood_name: str, tense_name: str, alternate=False):
        co = self._get_conj_obs(infinitive)
        return self._conjugate_mood_tense(co, mood_name, tense_name, alternate)

    def get_verbs(self) -> List[verb.Verb]:
        return self._verb_parser.verbs

    def get_infinitives(self) -> List[str]:
        return [v.infinitive for v in self._verb_parser.verbs]

    def get_templates(self) -> List[conjugation_template.ConjugationTemplate]:
        return self._conj_parser.templates

    def get_template_names(self) -> List[str]:
        return [t.name for t in self._conj_parser.templates]

    def find_verb_by_infinitive(self, infinitive) -> verb.Verb:
        return self._verb_parser.find_verb_by_infinitive(infinitive)

    def find_template(self, name: str) -> conjugation_template.ConjugationTemplate:
        return self._conj_parser.find_template(name)

    def get_verbs_that_start_with(self, query: str, max_results: int):
        query = query.lower()
        matches = self._verb_parser.get_verbs_that_start_with(query, max_results)
        return matches

    def _get_verb_stem(self, infinitive: str, template_name: str):
        """Get the verb stem given an ininitive and a colon-delimited template name.
        E.g. infinitive='parler' template_name='aim:er' -> 'parl'
        Note: Catalan overrides this base class implementation to allow looser matching
        (only requires the last n-1 chars of template ending to match infinitive ending)"""
        _, template_ending = template_name.split(u':')
        if not infinitive.endswith(template_ending):
            raise exceptions.ConjugatorError(
                "Template {} ending doesn't "
                "match infinitive {}"
                .format(template_name, infinitive))
        return infinitive[:len(infinitive) - len(template_ending)]

    def _is_impersonal_verb(self, infinitive: str):
        return False

    def _verb_can_be_reflexive(self, infinitive: str):
        return not self._is_impersonal_verb(infinitive)

    def _split_reflexive(self, infinitive: str):
        return (False, infinitive)

    def _add_reflexive_pronoun(self, s: str):
        pass

    def _add_subjunctive_relative_pronoun(self, s: str, tense_name: str):
        return s

    class ConjugationObjects:
        def __init__(self, infinitive: str, verb, template, verb_stem, is_reflexive):
            self.infinitive = infinitive
            self.verb = verb
            self.template = template
            self.verb_stem = verb_stem
            self.is_reflexive = is_reflexive
        
        def __repr__(self):
            return 'infinitive={} verb={} template={} verb_stem={} is_reflexive={}'.format(
                self.infinitive, self.verb, self.template, self.verb_stem, self.is_reflexive)

    def _get_conj_obs(self, infinitive) -> ConjugationObjects:
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

    def _get_compound_conjugations_for_mood(self, co: ConjugationObjects, mood_name: str):
        ret = {}
        comp_conj_map = self._get_compound_conjugations_aux_verb_map()
        if mood_name in comp_conj_map:
            for tense_name in comp_conj_map[mood_name]:
                ret[tense_name] = self._conjugate_mood_tense(co, mood_name, tense_name)
        return ret

    def _auxilary_verb_uses_alternate_conjugation(self, tense_name: str):
        return False

    def _conjugate_mood_tense(self, co: ConjugationObjects, mood_name: str, tense_name: str, alternate: bool=False):
        comp_conj_map = self._get_compound_conjugations_aux_verb_map()
        if mood_name in comp_conj_map and tense_name in comp_conj_map[mood_name]:
            aux_mood_name, aux_tense_name = comp_conj_map[mood_name][tense_name]
            return self._conjugate_compound(
                co, mood_name, tense_name, aux_mood_name, aux_tense_name, 
                self._auxilary_verb_uses_alternate_conjugation(tense_name))
        else:
            mood = co.template.moods[mood_name]
            if tense_name not in mood.tenses:
                raise exceptions.InvalidTenseError
            tense_template = mood.tenses[tense_name]
            return self._conjugate_simple_mood_tense(
                co.verb_stem, mood_name, tense_template,
                co.is_reflexive, alternate)

    def _get_tenses_conjugated_without_pronouns(self):
        return []

    def _get_auxilary_verb(self, co, mood_name, tense_name):
        return ''

    def _is_auxilary_verb_inflected(self, auxilary_verb):
        return False

    def _get_indicative_mood_name(self) -> str:
        return 'indicative'

    def _get_subjunctive_mood_name(self) -> str:
        return 'subjunctive'

    def _get_participle_mood_name(self) -> str:
        return 'partiple'

    def _get_participle_tense_name(self) -> str:
        return 'past-participle'

    def _add_present_participle_if_applicable(self, s: str, is_reflexive: bool, tense_name: str) -> str:
        return s

    def _get_alternate_hv_inflection(self, s: str) -> str:
        """Some language override this e.g. Spanish changes ending in 'hay' to 'ay' """
        return s

    @abstractmethod
    def _get_compound_conjugations_aux_verb_map(self) -> Dict[str, Dict[str, Tuple[str, ...]]]:
        """"Returns a map of the tense of the helping verb for each compound mood and tense"""
        pass

    def _get_default_participle_inflection_for_person(self, person):
        if person[1] == 's':
            return 'ms'
        else:
            return 'mp'

    def _get_default_pronoun(self, person, gender='m', is_reflexive=False):
        return ''

    def _combine_pronoun_and_conj(self, pronoun: str, conj: str):
        return pronoun + " " + conj

    def _conjugate_simple_mood_tense(self, verb_stem, mood_name, 
                                     tense_template, is_reflexive=False, alternate=False):
        ret = []
        tense_name = tense_template.name
        if tense_name in self._get_tenses_conjugated_without_pronouns():
            for person_ending in tense_template.person_endings:
                s = self._add_present_participle_if_applicable('', is_reflexive, tense_name)
                ending = person_ending.get_ending()
                if alternate:
                    ending = person_ending.get_alternate_ending_if_available()
                if ending != '-':
                    s += verb_stem
                s += ending
                if ending != '-':
                    s = self._add_reflexive_pronoun_or_pronoun_suffix_if_applicable(
                        s, is_reflexive, mood_name, tense_name, person_ending.get_person())
                if ending != '-':
                    s = self._add_adverb_if_applicable(s, mood_name, tense_name)
                ret.append(s)
        else:
            for person_ending in tense_template.person_endings:
                pronoun = self._get_default_pronoun(
                    person_ending.get_person(), is_reflexive=is_reflexive)
                ending = person_ending.get_ending()
                if alternate:
                    ending = person_ending.get_alternate_ending_if_available()
                conj = verb_stem + ending
                s = self._combine_pronoun_and_conj(pronoun, conj)
                if mood_name == self._get_subjunctive_mood_name():
                    s = self._add_subjunctive_relative_pronoun(s, tense_name)
                ret.append(s)
        return ret

    def _get_pronoun_suffix(self, person, gender='m', imperative=True):
        return ' ' + self._get_default_pronoun(person, gender)

    def _add_adverb_if_applicable(self, s, mood_name, tense_name):
        return s

    def _add_reflexive_pronoun_or_pronoun_suffix_if_applicable(self, s, is_reflexive, mood_name, tense_name, person):
        if is_reflexive:
            s += self._get_pronoun_suffix(person)
        return s

    def _compound_conjugation_not_applicable(self, is_reflexive, mood_name, aux_tense_name):
        return False

    def _conjugate_compound(self, co, mood_name, tense_name, aux_mood_name, aux_tense_name, aux_alternate):
        ret = []
        if self._compound_conjugation_not_applicable(co.is_reflexive, mood_name, aux_tense_name):
            return ret
        persons_mood_name = mood_name
        if mood_name not in co.template.moods:
            persons_mood_name = self._get_indicative_mood_name()
        persons = [pe.person for pe in 
            co.template.moods[persons_mood_name].tenses[aux_tense_name].person_endings]
        aux_verb = self._get_auxilary_verb(co, mood_name, tense_name)
        aux_co = self._get_conj_obs(aux_verb)
        aux_tense_template = copy.deepcopy(
            aux_co.template.moods[aux_mood_name].tenses[aux_tense_name])
        aux_person_endings = []
        for pe in aux_tense_template.person_endings:
            if pe.person in persons:
                aux_person_endings.append(pe)
        aux_tense_template.person_endings = aux_person_endings
        aux_conj = self._conjugate_simple_mood_tense(
            aux_co.verb_stem, 
            '', 
            aux_tense_template,
            co.is_reflexive,
            aux_alternate)
        ret = self._conjugate_compound_primary_verb(co, mood_name, tense_name, persons, aux_verb, aux_conj)
        if mood_name == self._get_subjunctive_mood_name():
            ret = [self._add_subjunctive_relative_pronoun(i, tense_name) for i in ret]
        return ret

    def _conjugate_compound_primary_verb(self, co, mood_name, tense_name, persons, aux_verb, aux_conj):
        ret = []
        pmood = self._get_participle_mood_name()
        ptense = self._get_participle_tense_name()
        participle = self._conjugate_simple_mood_tense(
            co.verb_stem, 
            pmood, 
            co.template.moods[pmood].tenses[ptense])
        if not self._is_auxilary_verb_inflected(aux_verb):
            for hv in aux_conj:
                p = participle[0]
                hv = self._get_alternate_hv_inflection(hv)
                ret.append(hv + ' ' + p)
        else:
            for i, hv in enumerate(aux_conj):
                participle_inflection = \
                    self._get_default_participle_inflection_for_person(
                        persons[i])
                p = participle[
                    grammar_defines.PARTICIPLE_INFLECTIONS.index(
                        participle_inflection)]
                ret.append(hv + ' ' + p)
        return ret