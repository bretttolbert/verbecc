from abc import ABC, abstractmethod
from typing import Tuple, Optional

from verbecc.core.utils.logging_utils import LoggingUtils
from verbecc.core.conjugator.conjugation_object import ConjugationObjects
from verbecc.core.defs.constants.grammar_defines import PARTICIPLE_INFLECTIONS
from verbecc.core.defs.types.data.conjugation_template import ConjugationTemplate
from verbecc.core.defs.types.data.person_ending import PersonEnding
from verbecc.core.defs.types.data.tense_template import TenseTemplate
from verbecc.core.defs.types.data.verb import Verb
from verbecc.core.defs.types.data.verbs import Verbs
from verbecc.core.defs.types.exceptions import ConjugatorError
from verbecc.core.defs.types.gender import Gender
from verbecc.core.defs.types.lang_code import LangCodeISO639_1
from verbecc.core.defs.types.mood import Mood, Moods
from verbecc.core.defs.types.participle_inflection import ParticipleInflection
from verbecc.core.defs.types.person import Person
from verbecc.core.defs.types.number import Number
from verbecc.core.defs.types.tense import Tense, Tenses
from verbecc.core.defs.types.pronoun import Pronoun
from verbecc.core.parsers.conjugations_parser import ConjugationsParser
from verbecc.core.parsers.verbs_parser import VerbsParser


class Inflector(ABC):
    """
    Abstract base class, with an implementation for each specific language supported.
    Inflector is for all conjugation logic that is language-specific.
    """

    # public:

    def __init__(self) -> None:
        self._logger = LoggingUtils.get_logger(self.__class__.__name__)
        self._verbs: Verbs = VerbsParser(self.get_lang()).parse()
        self._conjugations = ConjugationsParser(self.get_lang()).parse()

    @abstractmethod
    def get_lang(self) -> LangCodeISO639_1:
        raise NotImplementedError()

    def get_verbs(self) -> list[Verb]:
        return list(self._verbs)

    def get_infinitives(self) -> list[str]:
        return self._verbs.infinitives

    def get_templates(self) -> list[ConjugationTemplate]:
        return list(self._conjugations)

    def get_template_names(self) -> list[str]:
        return [t.name for t in self._conjugations]

    def find_verb_by_infinitive(self, infinitive: str) -> Verb:
        return self._verbs.find_verb_by_infinitive(infinitive)

    def find_template(self, name: str) -> ConjugationTemplate:
        return self._conjugations.find_template(name)

    def get_verbs_that_start_with(self, query: str, max_results: int) -> list[str]:
        return self._verbs.get_verbs_that_start_with(query.lower(), max_results)

    def get_verb_stem_from_template_name(
        self, infinitive: str, template_name: str
    ) -> str:
        """Get the verb stem given an infinitive and a colon-delimited template name.
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

    def verb_can_be_reflexive(self, infinitive: str) -> bool:
        return not self.private_is_impersonal_verb(infinitive)

    def split_reflexive(self, infinitive: str) -> Tuple[bool, str]:
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

        E.g. Spanish
        "levantarse" => (True, "levantar")

        E.g. Portuguese
        "vestir-se" => (True, "vestir")
        """
        return (False, infinitive)

    def add_reflexive_pronoun(self, s: str) -> str:
        return s

    def add_subjunctive_relative_pronoun(self, s: str, tense: Tense | str | None) -> str:
        return s

    def auxiliary_verb_uses_alternate_conjugation(self, tense: Tense) -> bool:
        return False

    def get_tenses_conjugated_without_pronouns(self) -> list[Tense]:
        return []

    def get_auxiliary_verb(
        self, co: ConjugationObjects, mood: Mood, tense: Tense
    ) -> str:
        return ""

    def is_auxiliary_verb_inflected(self, auxiliary_verb: str) -> bool:
        return False

    def get_infinitive_mood(self) -> Mood:
        return Moods.en.Infinitive

    def get_imperative_mood(self) -> Mood:
        return Moods.en.Imperative

    def get_indicative_mood(self) -> Mood:
        return Moods.en.Indicative

    def get_subjunctive_mood(self) -> Mood:
        return Moods.en.Subjunctive

    def get_conditional_mood(self) -> Mood:
        return Moods.en.Conditional

    def get_participle_mood(self) -> Mood:
        return Moods.en.Participle

    def get_participle_tense(self) -> Tense:
        return Tenses.en.PastParticiple

    def add_present_participle_if_applicable(
        self, s: str, is_reflexive: bool, tense: Tense
    ) -> str:
        return s

    def get_alternate_hv_inflection(self, s: str) -> str:
        """Some language override this e.g. Spanish changes ending in 'hay' to 'ay'"""
        return s

    @abstractmethod
    def get_compound_conjugations_aux_verb_map(
        self,
    ) -> dict[Mood, dict[Tense, Tuple[Mood, Tense]]]:
        """Returns a map of the tense of the helping verb for each compound mood and tense"""
        raise NotImplementedError()

    def get_participle_index_for_participle_inflection(
        self, participle_inflection: ParticipleInflection
    ) -> int:
        """
        Default order is like French XML file, i.e. MS, MP, FS, FP
        But in some lang XML files, e.g. Italian, the order is MS, FS, MP, FP
        TODO: Standardize the XML files
        """
        return PARTICIPLE_INFLECTIONS[self.get_lang()].index(participle_inflection)

    def get_default_participle_inflection_for_person(
        self, number: Number, gender: Gender = Gender.m
    ) -> ParticipleInflection:
        if number == Number.Singular:
            if gender == Gender.m:
                return ParticipleInflection.MasculineSingular
            else:
                return ParticipleInflection.FeminineSingular
        else:
            if gender == Gender.m:
                return ParticipleInflection.MasculinePlural
            else:
                return ParticipleInflection.FemininePlural

    def get_pronoun_gender(self, pronoun: Pronoun) -> Optional[Gender]:
        return None

    def get_pronouns(
        self,
        person: Optional[Person] = None,
        number: Optional[Number] = None,
        gender: Optional[Gender] = None,
        imperative: bool = False,
    ) -> list[Pronoun]:
        """
        Returns a list of all pronouns matching the provided filters,
        in the typical order, with the default pronoun first.
        E.g. Person.Second, Number.Singular => ["tú", "vos"]
        """
        return []

    def make_pronoun_reflexive(self, pronoun: Pronoun) -> str:
        """
        Adds appropriate suffix to make the pronoun reflexive
        E.g. "il" -> "il se"
        """
        return pronoun

    def combine_pronoun_and_conj(
        self,
        pronoun: str,
        conj: str,
        mood: Optional[Mood] = None,
        tense: Optional[Tense] = None,
        reflexive: bool = False,
    ) -> str:
        return pronoun + " " + conj

    def combine_verb_stem_and_ending(self, verb_stem: str, ending: str) -> str:
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

    def add_adverb_if_applicable(self, s: str, mood: Mood, tense: Tense) -> str:
        return s

    def add_reflexive_pronoun_or_pronoun_suffix_if_applicable(
        self,
        s: str,
        is_reflexive: bool,
        mood: Mood,
        tense: Tense,
        person: Person,
        number: Number,
        gender: Gender,
        pronoun: Optional[Pronoun],
    ) -> str:
        if is_reflexive:
            s += self._get_pronoun_suffix(person, number, gender)
        return s

    def compound_conjugation_not_applicable(
        self, is_reflexive: bool, mood: Mood, aux_tense: Tense
    ) -> bool:
        return False

    def compound_primary_verb_conjugation_uses_infinitive(
        self, mood: Mood, tense: Tense
    ) -> bool:
        return False

    def modify_aux_verb_conj_if_applicable(
        self, aux_conj: list[str], mood: Mood, tense: Tense
    ) -> list[str]:
        """
        Hook for certain languages e.g. Romanian that use a different
        aux_conj for certain tenses
        Only used for Romanian conditional prezent and perfect, currently
        """
        return aux_conj

    def add_compound_aux_verb_suffix_if_applicable(
        self, s: str, mood: Mood, tense: Tense
    ) -> str:
        """
        Hook for certain languages e.g. Romanian that add prefixes
        like ' fi' and 'să fi' for certain tenses
        Currently only used for certain Romanian verb tenses.
        """
        return s

    def insert_compound_aux_verb_prefix_if_applicable(
        self, s: str, mood: Mood, tense: Tense
    ) -> str:
        """
        Used by Romanian viitor-1-popular
        "eu o să fac, tu o să faci, ..."
        """
        return s

    def compound_has_no_primary_verb(self, mood: Mood, tense: Tense) -> bool:
        """Used for Romanian viitor-1-popular"""
        return False

    def compound_has_no_aux_verb(self, mood: Mood, tense: Tense) -> bool:
        """Used for Romanian conjunctiv perfect"""
        return False

    def modify_person_ending_if_applicable(
        self,
        person_ending: PersonEnding,
        mood: Mood,
        tense: Tense,
        tense_template: TenseTemplate,
        pronoun: Optional[str],
    ) -> PersonEnding:
        """
        Hook for certain languages e.g. Spanish that modify
        the standard person endings for certain persons depending
        on language specific options (e.g. Voseo)
        """
        return person_ending

    # private:

    def _get_pronoun_suffix(
        self,
        person: Person,
        number: Number,
        gender: Gender = Gender.m,
        imperative: bool = True,
    ) -> str:
        return " " + self.get_pronouns(person, number, gender)[0]

    def private_is_impersonal_verb(self, infinitive: str) -> bool:
        return False

    def _get_verbs(self) -> Verbs:
        return self._verbs
