from typing import Optional

from verbecc.src.conjugator.abstract_conjugator import AbstractConjugator
from verbecc.src.conjugator.conjugation_object import ConjugationObjects
from verbecc.src.conjugator.tense_conjugator import TenseConjugator
from verbecc.src.defs.types.conjugation.mood_conjugation import MoodConjugation
from verbecc.src.defs.types.conjugation.mood_conjugation_util import MoodConjugationUtil
from verbecc.src.defs.types.conjugation.tense_conjugation import TenseConjugation
from verbecc.src.defs.types.exceptions import InvalidMoodError
from verbecc.src.defs.types.lang_code import LangCodeISO639_1
from verbecc.src.defs.types.lang_specific_options import LangSpecificOptions
from verbecc.src.defs.types.mood import Mood
from verbecc.src.defs.types.tense import Tense
from verbecc.src.inflectors.inflector import Inflector


class MoodConjugator(AbstractConjugator):
    def __init__(
        self,
        lang: LangCodeISO639_1,
        lang_specific_options: Optional[LangSpecificOptions] = None,
        inflector: Optional[Inflector] = None,
    ) -> None:
        super().__init__(
            lang, lang_specific_options, self.__class__.__name__, inflector
        )
        self._tense_conjugator = TenseConjugator(
            lang, lang_specific_options, self._inflector
        )

    def conjugate_mood(
        self,
        infinitive: str,
        mood: Mood,
        conjugate_pronouns: bool = True,
    ) -> MoodConjugation:
        co = self._get_conj_obs(infinitive)
        return self._conjugate_mood(co, mood, conjugate_pronouns)

    def conjugate_mood_tense(
        self,
        infinitive: str,
        mood: Mood,
        tense: Tense,
        conjugate_pronouns: bool = True,
    ) -> TenseConjugation:
        return self._tense_conjugator.conjugate_mood_tense(
            infinitive,
            mood,
            tense,
            conjugate_pronouns=conjugate_pronouns,
        )

    def _conjugate_mood(
        self,
        co: ConjugationObjects,
        mood: Mood,
        conjugate_pronouns: bool = True,
    ) -> MoodConjugation:
        if mood not in co.template.mood_templates.keys():
            raise InvalidMoodError()
        ret = self._get_simple_conjugations_for_mood(
            co,
            mood,
            conjugate_pronouns,
        )
        ret = MoodConjugationUtil.combine(
            ret,
            self._get_compound_conjugations_for_mood(
                co,
                mood,
                conjugate_pronouns,
            ),
        )
        return ret

    def _get_simple_conjugations_for_mood(
        self,
        co: ConjugationObjects,
        mood: Mood,
        conjugate_pronouns: bool = True,
    ) -> MoodConjugation:
        ret = MoodConjugation(mood)
        mood_template = co.template.mood_templates[mood]
        for tense in mood_template.tense_templates:
            ret[tense] = self._tense_conjugator._conjugate_mood_tense(
                co,
                mood,
                tense,
                conjugate_pronouns=conjugate_pronouns,
            )
        return ret

    def _get_compound_conjugations_for_mood(
        self,
        co: ConjugationObjects,
        mood: Mood,
        conjugate_pronouns: bool = True,
    ) -> MoodConjugation:
        ret = MoodConjugation(mood)
        comp_conj_map = self._inflector.get_compound_conjugations_aux_verb_map()
        if mood in comp_conj_map:
            for tense in comp_conj_map[mood]:
                ret[tense] = self._tense_conjugator._conjugate_mood_tense(
                    co,
                    mood,
                    tense,
                    conjugate_pronouns=conjugate_pronouns,
                )
        return ret
