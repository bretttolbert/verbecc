from typing import Optional, cast

from verbecc.core.defs.types.mood import Mood
from verbecc.core.defs.types.tense import Tense
from verbecc.core.defs.types.conjugation.tense_conjugation import TenseConjugation
from verbecc.core.defs.types.lang_specific_options import LangSpecificOptions
from verbecc.core.defs.types.lang_code import LangCodeISO639_1
from verbecc.core.defs.types.data.tense_template import TenseTemplate
from verbecc.core.inflectors.inflector import Inflector
from verbecc.core.utils.string_utils import strip_accents
from verbecc.core.conjugator.abstract_conjugator import AbstractConjugator
from verbecc.core.conjugator.conjugator import Conjugator


class TenseConjugatorSimple(AbstractConjugator):

    def __init__(
        self,
        lang: LangCodeISO639_1,
        lang_specific_options: Optional[LangSpecificOptions] = None,
        inflector: Optional[Inflector] = None,
    ) -> None:
        super().__init__(
            lang, lang_specific_options, self.__class__.__name__, inflector
        )
        self._conjugator = Conjugator(lang, lang_specific_options, self._inflector)

    def conjugate_simple_mood_tense(
        self,
        verb_stem: str,
        mood: Mood,
        tense: Tense,
        tense_template: TenseTemplate,
        primary_tense: Optional[Tense] = None,
        is_reflexive: bool = False,
        conjugate_pronouns: bool = True,
        modify_stem_strip_accents: bool = False,
    ) -> TenseConjugation:
        """
        primary_tense: if this is being conjugated as
        an auxiliary verb as part of a compound tense conjugation,
        and we are conjugating pronouns i.e. the conjugate_pronouns
        argument is True, then this parameter should be supplied
        as it is passed to the inflector for determining
        which subjunctive relative pronouns to add.
        """
        if modify_stem_strip_accents and mood != self._inflector.get_infinitive_mood():
            verb_stem = strip_accents(verb_stem)
        ret = TenseConjugation(tense)
        tense = cast(Tense, tense_template.tense)
        tense_conjugated_with_pronoun = True
        if (
            tense in self._inflector.get_tenses_conjugated_without_pronouns()
            or not conjugate_pronouns
        ):
            tense_conjugated_with_pronoun = False

        if len(tense_template.person_endings) == 0:
            self._logger.warning("tense_template.person_endings is empty")

        # There will be at least one conjugation per person-ending and
        # potentially one or more alternate conjugations
        for person_ending in tense_template.person_endings:
            person = person_ending.get_person()
            number = person_ending.get_number()

            pronouns = self._inflector.get_pronouns(
                person=person,
                number=number,
                imperative=(mood == self._inflector.get_imperative_mood()),
            )
            # note: tense_conjugated_with_pronoun is False
            # for imperative tense but we still want to set the
            # `pronoun` field.
            # the only cases where we don't set the `pronoun` field
            # is when it's participle mood or infinitive mood.
            # participle mood because the PersonEndings
            # are participle type, i.e. each PersonEnding has
            # gender and number instead of person and number.
            if mood == self._inflector.get_participle_mood():
                # we're only conjugating person-endings
                pronouns = [None]
            # if there's a single person-ending, it won't have person/number/gender
            # examples: infinitive tense (e.g. "ayant"), Catalan gerundi tense
            elif len(tense_template.person_endings) == 1:
                pronouns = [None]
            for pronoun in pronouns:
                ret.append(
                    self._conjugator.conjugate(
                        verb_stem,
                        mood,
                        tense,
                        tense_template,
                        person,
                        person_ending,
                        number,
                        pronoun,
                        is_reflexive,
                        primary_tense,
                        tense_conjugated_with_pronoun,
                    )
                )
        if len(ret) == 0:
            self._logger.warning("conjugation is empty")
        return ret
