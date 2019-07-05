# -*- coding: utf-8 -*-

from __future__ import print_function
import copy

from .conjugation_template import ConjugationTemplate
from .conjugations_parser import ConjugationsParser
from .grammar_defines import *
from .mood import Mood
from .person_ending import PersonEnding
from .string_utils import (
    prepend_with_que,
    prepend_with_se,
    split_reflexive,
    starts_with_vowel)
from .tense_template import TenseTemplate
from .verb import Verb
from .verbs_parser import (
    VerbNotFoundError, VerbsParser
)

class ConjugatorError(Exception):
    pass

class InvalidMoodError(Exception):
    pass

def get_verb_stem(infinitive, template_name):
    template_beg, template_ending = template_name.split(u':')
    if not infinitive.endswith(template_ending):
        raise ConjugatorError(
            "Template {} ending doesn't "
            "match infinitive {}"
            .format(template_name, infinitive))
    return infinitive[:len(infinitive) - len(template_ending)]

class Conjugator:
    def __init__(self, lang='fr'):
        self.verb_parser = VerbsParser()
        self.conj_parser = ConjugationsParser()

    def is_impersonal_verb(self, infinitive):
        ret = False
        verb = self.verb_parser.find_verb_by_infinitive(infinitive)
        template = self.conj_parser.find_template(verb.template)
        if len(template.moods['indicatif'].tenses['présent'].person_endings) < 6:
            ret = True
        return ret

    def verb_can_be_reflexive(self, infinitive):
        return (not self.is_impersonal_verb(infinitive)
            and infinitive not in 
            VERBS_THAT_CANNOT_BE_REFLEXIVE_OTHER_THAN_IMPERSONAL_VERBS) 

    class ConjugationObjects:
        def __init__(self, infinitive, verb, template, verb_stem, is_reflexive):
            self.infinitive = infinitive
            self.verb = verb
            self.template = template
            self.verb_stem = verb_stem
            self.is_reflexive = is_reflexive

    def _get_conj_obs(self, infinitive):
        infinitive = infinitive.lower()
        is_reflexive, infinitive = split_reflexive(infinitive)
        if is_reflexive and not self.verb_can_be_reflexive(infinitive):
            raise VerbNotFoundError("Verb cannot be reflexive")
        verb = self.verb_parser.find_verb_by_infinitive(infinitive)
        template = self.conj_parser.find_template(verb.template)
        verb_stem = get_verb_stem(verb.infinitive, template.name)
        return Conjugator.ConjugationObjects(
            infinitive, verb, template, verb_stem, is_reflexive)      

    def conjugate(self, infinitive):
        co = self._get_conj_obs(infinitive)
        moods = {}
        for mood in co.template.moods:
            moods[mood] = self._get_full_conjugation_for_mood(co, mood)
        return {'verb': {'infinitive': co.verb.infinitive, 
                         'template': co.verb.template,
                         'translation_en': co.verb.translation_en,
                         'stem': co.verb_stem}, 
                'moods': moods}

    def get_full_conjugation_for_mood(self, infinitive, mood_name):
        co = self._get_conj_obs(infinitive)
        return self._get_full_conjugation_for_mood(co, mood_name)

    def get_verbs_that_start_with(self, query, max_results):
        query = query.lower()
        is_reflexive, query = split_reflexive(query)
        matches = self.verb_parser.get_verbs_that_start_with(query, max_results)
        if is_reflexive:
            matches = [prepend_with_se(m) 
            for m in matches if self.verb_can_be_reflexive(m)]
        return matches

    def find_verb_by_infinitive(self, infinitive):
        return self.verb_parser.find_verb_by_infinitive(infinitive)

    def _get_full_conjugation_for_mood(self, co, mood_name):
        conjugations = {}
        if mood_name not in co.template.moods:
            raise InvalidMoodError
        self._get_simple_conjugations_for_mood(co, mood_name, conjugations);
        self._get_compound_conjugations_for_mood(co, mood_name, conjugations)
        return conjugations

    def _get_simple_conjugations_for_mood(self, co, mood_name, conjugations):
        mood = co.template.moods[mood_name]
        for tense in mood.tenses:
            tense_template = mood.tenses[tense]
            conjugations[tense] = self._conjugate_specific_tense(
                co.verb_stem, mood_name, tense_template,
                co.is_reflexive)        

    def _get_compound_conjugations_for_mood(self, co, mood_name, conjugations):
        if mood_name == 'indicatif':
            conjugations['passé-composé'] = self._conjugate_passe_compose(co)
            conjugations['plus-que-parfait'] = self._conjugate_plusqueparfait(co)
            conjugations['futur-antérieur'] = self._conjugate_futur_anterieur(co)
            conjugations['passé-antérieur'] = self._conjugate_passe_anterieur(co)
        elif mood_name == 'subjonctif':
            conjugations['passé'] = self._conjugate_subjonctif_passe(co)
            conjugations['plus-que-parfait'] = self._conjugate_subjonctif_plusqueparfait(co)
        elif mood_name == 'conditionnel':
            conjugations['passé'] = self._conjugate_conditionnel_passe(co)
        elif mood_name == 'imperatif':
            conjugations['imperatif-passé'] = self._conjugate_imperatif_passe(co)

    def conjugate_passe_compose(self, infinitive):
        co = self._get_conj_obs(infinitive)
        return self._conjugate_passe_compose(co)

    def conjugate_plusqueparfait(self, infinitive):
        co = self._get_conj_obs(infinitive)
        return self._conjugate_plusqueparfait(co)

    def conjugate_futur_anterieur(self, infinitive):
        co = self._get_conj_obs(infinitive)
        return self._conjugate_futur_anterieur(co)

    def conjugate_passe_anterieur(self, infinitive):
        co = self._get_conj_obs(infinitive)
        return self._conjugate_passe_anterieur(co)

    def conjugate_subjonctif_passe(self, infinitive):
        co = self._get_conj_obs(infinitive)
        return self._conjugate_subjonctif_passe(co)

    def conjugate_subjonctif_plusqueparfait(self, infinitive):
        co = self._get_conj_obs(infinitive)
        return self._conjugate_subjonctif_plusqueparfait(co)

    def conjugate_conditionnel_passe(self, infinitive):
        co = self._get_conj_obs(infinitive)
        return self._conjugate_conditionnel_passe(co)

    def conjugate_imperatif_passe(self, infinitive):
        co = self._get_conj_obs(infinitive)
        return self._conjugate_imperatif_passe(co)

    def _conjugate_passe_compose(self, co):
        return self._conjugate_compound(co, 'indicatif', 'indicatif', 'présent')

    def _conjugate_plusqueparfait(self, co):
        return self._conjugate_compound(co, 'indicatif', 'indicatif', 'imparfait')

    def _conjugate_futur_anterieur(self, co):
        return self._conjugate_compound(co, 'indicatif', 'indicatif', 'futur-simple')

    def _conjugate_passe_anterieur(self, co):
        return self._conjugate_compound(co, 'indicatif', 'indicatif', 'passé-simple')

    def _conjugate_subjonctif_passe(self, co):
        return self._conjugate_compound(co, 'subjonctif', 'subjonctif', 'présent')

    def _conjugate_subjonctif_plusqueparfait(self, co):
        return self._conjugate_compound(co, 'subjonctif', 'subjonctif', 'imparfait')

    def _conjugate_conditionnel_passe(self, co):
        return self._conjugate_compound(co, 'conditionnel', 'conditionnel', 'présent')

    def _conjugate_imperatif_passe(self, co):
        return self._conjugate_compound(co, 'imperatif', 'imperatif', 'imperatif-présent')

    def _conjugate_compound(self, co, mood_name, hv_mood_name, hv_tense_name):
        """Conjugate a compound tense
        Args:
            co: ConjugationObjects for the verb being conjugated
            mood_name: mood verb is being conjugated in
            hv_mood_name: mood_name for conjugating helping verb
            hv_tense_name: tense_name for conjugating helping verb
        """
        ret = []
        if (co.is_reflexive and mood_name == 'imperatif' 
            and hv_tense_name == 'imperatif-présent'):
            return ret
        persons = [pe.person for pe in 
            co.template.moods[mood_name].tenses[hv_tense_name].person_endings]
        helping_verb = 'avoir'
        if (co.verb.infinitive in VERBS_CONJUGATED_WITH_ETRE
            or co.is_reflexive):
            helping_verb = 'être'
        hvco = self._get_conj_obs(helping_verb)
        hvtense_template = copy.deepcopy(
            hvco.template.moods[hv_mood_name].tenses[hv_tense_name])
        hvperson_endings = []
        for pe in hvtense_template.person_endings:
            if pe.person in persons:
                hvperson_endings.append(pe)
        hvtense_template.person_endings = hvperson_endings
        hvconj = self._conjugate_specific_tense(
            hvco.verb_stem, 
            'indicatif', 
            hvtense_template,
            co.is_reflexive)
        participle = self._conjugate_specific_tense(
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
                    get_default_participle_inflection_for_person(persons[i])
                p = participle[participle_inflection.value]
                ret.append(hv + ' ' + p)
        if mood_name == 'subjonctif':
            ret = [prepend_with_que(i) for i in ret]
        return ret

    def _conjugate_specific_tense(self, verb_stem, mood_name, 
                                  tense_template, is_reflexive=False):
        ret = []
        if tense_template.name in TENSES_CONJUGATED_WITHOUT_PRONOUNS:
            for person_ending in tense_template.person_endings:
                conj = ''
                if is_reflexive and tense_template.name == 'participe-passé':
                    conj += 'étant '
                conj += verb_stem + person_ending.get_ending()
                if is_reflexive:
                    if mood_name != 'imperatif':
                        conj = prepend_with_se(conj)
                    else:
                        conj += get_pronoun_suffix(person_ending.get_person())
                ret.append(conj)
        else:
            for person_ending in tense_template.person_endings:
                pronoun = get_default_pronoun(
                    person_ending.get_person(), is_reflexive)
                ending = person_ending.get_ending()
                conjugation = self._conjugate_specific_tense_pronoun(
                    verb_stem, ending, pronoun)
                if mood_name == 'subjonctif':
                    conjugation = prepend_with_que(conjugation)
                ret.append(conjugation)
        return ret

    def _conjugate_specific_tense_pronoun(self, verb_stem, ending, pronoun):
        ret = u''
        conjugated_verb = verb_stem + ending
        if pronoun[-1] == "e" and starts_with_vowel(conjugated_verb):
            ret += pronoun[:-1] + "'"
        else:
            ret += pronoun + " "
        ret += conjugated_verb
        return ret
