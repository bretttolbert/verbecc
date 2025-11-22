from typing import List, Optional

from verbecc.src.conjugator.abstract_conjugator import AbstractConjugator
from verbecc.src.defs.constants import grammar_defines
from verbecc.src.defs.types.conjugation.conjugation import Conjugation
from verbecc.src.defs.types.data.person_ending import PersonEnding
from verbecc.src.defs.types.data.tense_template import TenseTemplate
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.lang_code import LangCodeISO639_1
from verbecc.src.defs.types.lang_specific_options import LangSpecificOptions
from verbecc.src.defs.types.mood import Mood
from verbecc.src.defs.types.number import Number
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.tense import Tense
from verbecc.src.inflectors.inflector import Inflector
from verbecc.src.defs.types.pronoun import Pronoun


class Conjugator(AbstractConjugator):
    """
    Conjugator for a specific Conjugation.
    A Conjugation is the fundamental unit of verbecc representing a single*, specific, inflected conjugation.
    The conjugation(s) for a specific person*, number*, gender* and pronoun*, for a specific
    mood and tense, for a specific verb,
    *including alternate conjugation(s) (if applicable)
    *pronoun is omitted for tenses conjugated without pronouns (e.g. participle or imperative)
    *person/pronoun are omitted for participle tense (only has gender and number)
    *person/number/gender/pronoun are omitted for the infinitive mood
    (e.g. infinitif présent tense)
    """

    def __init__(
        self,
        lang: LangCodeISO639_1,
        lang_specific_options: Optional[LangSpecificOptions] = None,
        inflector: Optional[Inflector] = None,
    ) -> None:
        super().__init__(
            lang, lang_specific_options, self.__class__.__name__, inflector
        )

    def conjugate(
        self,
        verb_stem: str,
        mood: Mood,
        tense: Tense,
        tense_template: TenseTemplate,
        person: Optional[Person],
        person_ending: PersonEnding,
        number: Optional[Number],
        pronoun: Optional[Pronoun],
        is_reflexive: bool = False,
        primary_tense: Optional[Tense] = None,
        tense_conjugated_with_pronoun: bool = True,
    ) -> Conjugation:
        # here's where the voseo magic happens
        person_ending = self._inflector.modify_person_ending_if_applicable(
            person_ending, mood, tense, tense_template, pronoun
        )

        # person_ending.gender will be None unless it's a participle ending
        # gender will be None/null unless it matters.
        conjugation_gender = None
        if pronoun is not None:
            conjugation_gender = self._inflector.get_pronoun_gender(pronoun)
        if conjugation_gender is None and person_ending.gender is not None:
            conjugation_gender = person_ending.gender

        conjugation = Conjugation(
            person,
            number,
            conjugation_gender,
            pronoun,
        )
        pronoun_str = "" if pronoun is None else str(pronoun)
        if is_reflexive and pronoun is not None:
            pronoun_str = self._inflector.make_pronoun_reflexive(pronoun)

        # get endings i.e. primary and optional alternate(s)
        endings: List[str] = []
        endings.extend(person_ending.get_endings())

        if len(endings) == 0:
            self._logger.warning("endings is empty")

        # there may be one or more alternate endings
        for ending in endings:
            s = grammar_defines.NO_VALUE
            if tense_conjugated_with_pronoun:
                if ending != grammar_defines.NO_VALUE:
                    conj = self._inflector.combine_verb_stem_and_ending(
                        verb_stem, ending
                    )
                    if len(pronoun_str):
                        s = self._inflector.combine_pronoun_and_conj(pronoun_str, conj)
                    if mood == self._inflector.get_subjunctive_mood():
                        t = tense
                        if primary_tense:
                            t = primary_tense
                        s = self._inflector.add_subjunctive_relative_pronoun(s, t)
            else:
                # conjugation without pronoun
                # e.g. fr:participe:participe-passé
                # and also currently conjugations that have pronoun suffixes
                # see test test_conjugate_ter_infinitivo_pessoal_presente

                s = self._inflector.add_present_participle_if_applicable(
                    "", is_reflexive, tense
                )
                if ending != grammar_defines.NO_VALUE:
                    s += self._inflector.combine_verb_stem_and_ending(verb_stem, ending)
                else:
                    s += grammar_defines.NO_VALUE
                # TODO: Need to iterate over all the pronouns
                # like we do for simple conjugations now
                # See failing test test_conjugate_ter_infinitivo_pessoal_presente
                # currently it's just doing
                if ending != grammar_defines.NO_VALUE:
                    person = person_ending.get_person()
                    number = Number.Singular
                    person_ending_number = person_ending.get_number()
                    if person_ending_number is not None:
                        number = person_ending_number
                    if person is not None:
                        gender = Gender.m
                        if pronoun is not None:
                            pronoun_gender = self._inflector.get_pronoun_gender(pronoun)
                            if pronoun_gender is not None:
                                gender = pronoun_gender
                        s = self._inflector.add_reflexive_pronoun_or_pronoun_suffix_if_applicable(
                            s,
                            is_reflexive,
                            mood,
                            tense if primary_tense is None else primary_tense,
                            person,
                            number,
                            gender,
                        )
                    else:
                        self._logger.debug("person is None")
                if ending != grammar_defines.NO_VALUE:
                    t = tense
                    if primary_tense:
                        t = primary_tense
                    s = self._inflector.add_adverb_if_applicable(s, mood, t)
            conjugation.append(s)
        return conjugation
