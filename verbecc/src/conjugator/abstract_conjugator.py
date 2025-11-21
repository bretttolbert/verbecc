from abc import ABC
from typing import List, Optional

from verbecc.src.conjugator.conjugation_object import ConjugationObjects
from verbecc.src.defs.types.conjugation.conjugation import Conjugation
from verbecc.src.defs.types.conjugation.tense_conjugation import TenseConjugation
from verbecc.src.defs.types.data.conjugation_template import ConjugationTemplate
from verbecc.src.defs.types.data.person_ending import PersonEnding
from verbecc.src.defs.types.data.verb import Verb
from verbecc.src.defs.types.exceptions.verb_not_found_error import VerbNotFoundError
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.lang_code import LangCodeISO639_1
from verbecc.src.defs.types.lang_specific_options import LangSpecificOptions
from verbecc.src.defs.types.number import Number
from verbecc.src.defs.types.person import Person
from verbecc.src.inflectors.inflector_factory import InflectorFactory
from verbecc.src.utils.logging_utils import LoggingUtils


class AbstractConjugator(ABC):

    def __init__(
        self,
        lang: LangCodeISO639_1,
        lang_specific_options: Optional[LangSpecificOptions],
        subclass_name: str,
    ) -> None:
        self._inflector = InflectorFactory.make_inflector(lang, lang_specific_options)
        self._logger = LoggingUtils.get_logger(subclass_name)
        super().__init__()

    def _get_conj_obs(self, infinitive: str) -> ConjugationObjects:
        infinitive = infinitive.lower()
        is_reflexive, infinitive = self._inflector.split_reflexive(infinitive)
        if is_reflexive and not self._inflector.verb_can_be_reflexive(infinitive):
            raise VerbNotFoundError("Verb cannot be reflexive")
        verb = self.find_verb_by_infinitive(infinitive)
        template = self.find_template(verb.template)
        verb_stem = self._inflector.get_verb_stem_from_template_name(
            verb.infinitive, template.name
        )
        return ConjugationObjects(infinitive, verb, template, verb_stem, is_reflexive)

    def get_verbs(self) -> List[Verb]:
        return self._inflector.get_verbs()

    def get_infinitives(self) -> List[str]:
        return self._inflector.get_infinitives()

    def get_templates(self) -> List[ConjugationTemplate]:
        return self._inflector.get_templates()

    def get_template_names(self) -> List[str]:
        return self._inflector.get_template_names()

    def find_verb_by_infinitive(self, infinitive: str) -> Verb:
        return self._inflector.find_verb_by_infinitive(infinitive)

    def find_template(self, name: str) -> ConjugationTemplate:
        return self._inflector.find_template(name)

    def get_verbs_that_start_with(self, query: str, max_results: int) -> List[str]:
        return self._inflector.get_verbs_that_start_with(query, max_results)

    def get_person_ending_by_gender_and_number(
        self,
        person_endings: List[PersonEnding],
        gender: Optional[Gender],
        number: Optional[Number],
    ) -> PersonEnding:
        resolved_gender = Gender.m
        resolved_number = Number.Singular
        if gender is not None:
            resolved_gender = gender
        if number is not Number:
            resolved_number = number
        for pe in person_endings:
            if pe.gender == resolved_gender and pe.number == resolved_number:
                return pe
        self._logger.warning(
            "Failed find matching PersonEnding for gender=%s number=%s", gender, number
        )
        return person_endings[0]

    def get_conjugation_by_gender_and_number(
        self,
        tense_conjugation: TenseConjugation,
        gender: Optional[Gender],
        number: Optional[Number],
    ) -> Conjugation:
        resolved_gender = Gender.m
        resolved_number = Number.Singular
        if gender is not None:
            resolved_gender = gender
        if number is not Number:
            resolved_number = number
        for c in tense_conjugation:
            if c.get_gender() == resolved_gender and c.get_number() == resolved_number:
                return c
        self._logger.warning(
            "Failed find matching Conjugation for gender=%s number=%s", gender, number
        )
        if len(tense_conjugation) == 0:
            self._logger.error("Failed to get conjugation, tense_conjugation is empty")
            raise Exception("Failed to get conjugation, tense_conjugation is empty")
        return tense_conjugation[0]
