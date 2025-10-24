import logging

from verbecc.src.defs.constants.config import DEVEL_MODE
from verbecc.src.defs.types.mood import MoodEn as Mood
from verbecc.src.defs.types.tense import TenseEn as Tense
from verbecc.src.parsers.person_ending import PersonEnding

logging_level = logging.CRITICAL + 1  # effectively disables logging
if DEVEL_MODE:
    logging_level = logging.DEBUG

logging.basicConfig(
    level=logging_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("verbecc.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.constants.grammar_defines import PARTICIPLE_INFLECTIONS
from verbecc.src.defs.types.exceptions import ConjugatorError
from verbecc.src.defs.types.lang_code import LangCodeISO639_1
from verbecc.src.defs.types.partiple_inflection import ParticipleInflection
from verbecc.src.defs.types.person import Person, is_singular
from verbecc.src.defs.types.lang_specific_options import (
    LangSpecificOptions,
)
from verbecc.src.parsers.conjugations_parser import ConjugationsParser
from verbecc.src.parsers.conjugation_template import ConjugationTemplate
from verbecc.src.parsers.tense_template import TenseTemplate
from verbecc.src.conjugator.conjugation_object import ConjugationObjects
from verbecc.src.parsers.verb import Verb
from verbecc.src.parsers.verbs_parser import VerbsParser


class Inflector(ABC):
    """
    Abstract base class, with an implementation for each specific language supported.
    Inflector is for all conjugation logic that is language-specific.
    """

    @property
    @abstractmethod
    def lang(self) -> LangCodeISO639_1:
        raise NotImplementedError

    def __init__(self) -> None:
        self._verb_parser = VerbsParser(self.lang)
        self._conj_parser = ConjugationsParser(self.lang)

    def get_verbs(self) -> List[Verb]:
        return self._verb_parser.verbs

    def get_infinitives(self) -> List[str]:
        return [v.infinitive for v in self._verb_parser.verbs]

    def get_templates(self) -> List[ConjugationTemplate]:
        return self._conj_parser.templates

    def get_template_names(self) -> List[str]:
        return [t.name for t in self._conj_parser.templates]

    def find_verb_by_infinitive(self, infinitive: str) -> Verb:
        return self._verb_parser.find_verb_by_infinitive(infinitive)

    def find_template(self, name: str) -> ConjugationTemplate:
        return self._conj_parser.find_template(name)

    def get_verbs_that_start_with(self, query: str, max_results: int) -> List[str]:
        query = query.lower()
        matches = self._verb_parser.get_verbs_that_start_with(query, max_results)
        return matches

    def _get_verb_stem_from_template_name(
        self, infinitive: str, template_name: str
    ) -> str:
        """Get the verb stem given an ininitive and a colon-delimited template name.
        E.g. infinitive='parler' template_name='aim:er' -> 'parl'
        Note: Catalan overrides this base class implementation to allow looser matching
        (only requires the last n-1 chars of template ending to match infinitive ending)
        """
        _, template_ending = template_name.split(":")
        if not infinitive.endswith(template_ending):
            raise ConjugatorError(
                "Template {} ending doesn't "
                "match infinitive {}".format(template_name, infinitive)
            )
        return infinitive[: len(infinitive) - len(template_ending)]

    def _is_impersonal_verb(self, infinitive: str) -> bool:
        return False

    def _verb_can_be_reflexive(self, infinitive: str) -> bool:
        return not self._is_impersonal_verb(infinitive)

    def _split_reflexive(self, infinitive: str) -> Tuple[bool, str]:
        """
        Tests whether an infinitive is reflexive
        Returns a 2-tuple of whether it is reflexive
        and the non-reflexive form of the infinitive.

        E.g. French:
        "se raser" => (True, "raser")
        "s'habiller" => (True, "habiller")
        "parler" => (False, "parler")
        E.g. Italian:
        "alzarsi" => (True, "alzare")
        "preoccuparsi" => (True, "preoccupare")
        """
        return (False, infinitive)

    def _add_reflexive_pronoun(self, s: str) -> str:
        return s

    def _add_subjunctive_relative_pronoun(self, s: str, tense: Tense) -> str:
        return s

    def _auxilary_verb_uses_alternate_conjugation(self, tense: Tense) -> bool:
        return False

    def _get_tenses_conjugated_without_pronouns(self) -> List[str]:
        return []

    def _get_auxilary_verb(
        self, co: ConjugationObjects, mood: Mood, tense: Tense
    ) -> str:
        return ""

    def _is_auxilary_verb_inflected(self, auxilary_verb: str) -> bool:
        return False

    def _get_infinitive_mood(self) -> Mood:
        return Mood.Infinitive

    def _get_indicative_mood(self) -> Mood:
        return Mood.Indicative

    def _get_subjunctive_mood(self) -> Mood:
        return Mood.Subjunctive

    def _get_conditional_mood(self) -> Mood:
        return Mood.Conditional

    def _get_participle_mood(self) -> Mood:
        return Mood.Participle

    def _get_participle_tense(self) -> Tense:
        return Tense.PastParticiple

    def _add_present_participle_if_applicable(
        self, s: str, is_reflexive: bool, tense: Tense
    ) -> str:
        return s

    def _get_alternate_hv_inflection(self, s: str) -> str:
        """Some language override this e.g. Spanish changes ending in 'hay' to 'ay'"""
        return s

    @abstractmethod
    def _get_compound_conjugations_aux_verb_map(
        self,
    ) -> Dict[str, Dict[str, Tuple[str, ...]]]:
        """Returns a map of the tense of the helping verb for each compound mood and tense"""
        raise NotImplementedError

    def _get_participle_index_for_participle_inflection(
        self, participle_inflection: ParticipleInflection
    ) -> int:
        """
        Default order is like French XML file, i.e. MS, MP, FS, FP
        But in some lang XML files, e.g. Italian, the order is MS, FS, MP, FP
        TODO: Standardize the XML files
        """
        return PARTICIPLE_INFLECTIONS.index(participle_inflection)

    def _get_default_participle_inflection_for_person(
        self, person: Person, gender: Gender = Gender.m
    ) -> ParticipleInflection:
        if is_singular(person):
            if gender == Gender.m:
                return ParticipleInflection.MasculineSingular
            else:
                return ParticipleInflection.FeminineSingular
        else:
            if gender == Gender.m:
                return ParticipleInflection.MasculinePlural
            else:
                return ParticipleInflection.FemininePlural

    def get_default_pronoun(
        self,
        person: Person,
        gender: Gender = Gender.m,
        is_reflexive: bool = False,
        lang_specific_options: LangSpecificOptions = None,
    ) -> str:
        return ""

    def _combine_pronoun_and_conj(self, pronoun: str, conj: str) -> str:
        return pronoun + " " + conj

    def _combine_verb_stem_and_ending(self, verb_stem: str, ending: str) -> str:
        """
        Originally this would simply combine the verb_stem and the ending.
        E.g. "parl" + "er" = "parler"

        Now for Catalan/enhanced templates we need to support stem-modifying verbs.

        E.g. for infintive "pertànyer" in the indicative mood simple-past tense,
        two new stem-modifying template feature will be used:

        First the template's modify-stem="strip-accents" attribute is used to
        remove the accent from the stem for all inflected forms.

        infinitive "pertànyer" matches template "pertàny:er" which has
        modify-stem="strip-accents"
        So the stem "pertàny" becomes "pertany"

        modify-stem="strip-accents" is applied in _conjugate_simple_mood_tense,
        so the verb_stem argument to this function is presumed to already have
        applicable modifications applied.

        Next, the "pertàny:er" template endings will use the new delete operator
        to delete one letter from the end of the stem.

        For "pertàny:er" in the i

        "pertany" + "-guí" = "pertanguí"

        Caution: A single "-" is also used as the placeholder for tenses that are
        not conjugated, in some verbs. "-" should only delete from the stem if it
        is followed by one or more characters.
        """
        while ending != "-" and ending.startswith("-"):
            ending = ending[1:]
            verb_stem = verb_stem[:-1]
        return verb_stem + ending

    def _get_pronoun_suffix(
        self, person: Person, gender: Gender = Gender.m, imperative: bool = True
    ) -> str:
        return " " + self.get_default_pronoun(person, gender)

    def _add_adverb_if_applicable(self, s: str, mood: Mood, tense: Tense) -> str:
        return s

    def _add_reflexive_pronoun_or_pronoun_suffix_if_applicable(
        self, s: str, is_reflexive: bool, mood: Mood, tense: Tense, person: Person
    ) -> str:
        if is_reflexive:
            s += self._get_pronoun_suffix(person)
        return s

    def _compound_conjugation_not_applicable(
        self, is_reflexive: bool, mood: Mood, aux_tense: Tense
    ) -> bool:
        return False

    def _compound_primary_verb_conjugation_uses_infinitive(
        self, mood: Mood, tense: Tense
    ) -> bool:
        return False

    def _modify_aux_verb_conj_if_applicable(
        self, aux_conj: List[str], mood: Mood, tense: Tense
    ) -> List[str]:
        """
        Hook for certain languages e.g. Romanian that use a different
        aux_conj for certain tenses
        Only used for Romanian conditional prezent and perfect, currently
        """
        return aux_conj

    def _add_compound_aux_verb_suffix_if_applicable(
        self, s: str, mood: Mood, tense: Mood
    ) -> str:
        """
        Hook for certain languages e.g. Romanian that add prefixes
        like ' fi' and 'să fi' for certain tenses
        Currently only used for certain Romanian verb tenses.
        """
        return s

    def _insert_compound_aux_verb_prefix_if_applicable(
        self, s: str, mood: Mood, tense: Tense
    ) -> str:
        """
        Used by Romanian viitor-1-popular
        "eu o să fac, tu o să faci, ..."
        """
        return s

    def _compound_has_no_primary_verb(self, mood: Mood, tense: Tense) -> bool:
        """Used for Romanian viitor-1-popular"""
        return False

    def _compound_has_no_aux_verb(self, mood: Mood, tense: Tense) -> bool:
        """Used for Romanian conjunctiv perfect"""
        return False

    def modify_person_ending_if_applicable(
        self,
        person_ending: PersonEnding,
        mood: Mood,
        tense: Tense,
        tense_template: TenseTemplate,
        lang_specific_options: LangSpecificOptions,
    ) -> PersonEnding:
        """
        Hook for certain languages e.g. Spanish that modify
        the standard person endings for certain persons depending
        on language specific options (e.g. Voseo)
        """
        return person_ending
