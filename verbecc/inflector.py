from abc import ABC, abstractmethod

from . import grammar_defines
from . import string_utils
from . import exceptions

class Inflector(ABC):
    def __init__(self):
        self._verb_parser = None
        self._conj_parser = None

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
        return self._verb_parser.find_verb_by_infinitive(infinitive)

    def find_template(self, name):
        return self._conj_parser.find_template(name)

    def get_verbs_that_start_with(self, query, max_results):
        query = query.lower()
        is_reflexive, query = string_utils.split_reflexive(query)
        matches = self._verb_parser.get_verbs_that_start_with(query, max_results)
        if is_reflexive:
            matches = [string_utils.prepend_with_se(m) 
            for m in matches if self._verb_can_be_reflexive(m)]
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
        return {}
