from typing import Optional, cast

from verbecc.core.conjugator.abstract_conjugator import AbstractConjugator
from verbecc.core.conjugator.conjugation_object import ConjugationObjects
from verbecc.core.conjugator.tense_conjugator import TenseConjugator
from verbecc.core.defs.types.conjugation.mood_conjugation import MoodConjugation
from verbecc.core.defs.types.conjugation.mood_conjugation_util import MoodConjugationUtil
from verbecc.core.defs.types.conjugation.tense_conjugation import TenseConjugation
from verbecc.core.defs.types.exceptions import InvalidMoodError
from verbecc.core.defs.types.lang_code import LangCodeISO639_1
from verbecc.core.defs.types.lang_specific_options import LangSpecificOptions
from verbecc.core.defs.types.mood import Mood
from verbecc.core.defs.types.tense import Tense
from verbecc.core.inflectors.inflector import Inflector


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
        mood: Mood | str,
        conjugate_pronouns: bool = True,
    ) -> MoodConjugation:
        co = self._get_conj_objs(infinitive)
        return self._conjugate_mood(co, mood, conjugate_pronouns)

    def conjugate_mood_tense(
        self,
        infinitive: str,
        mood: Mood | str,
        tense: Tense | str,
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
        mood: Mood | str,
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
        mood: Mood | str,
        conjugate_pronouns: bool = True,
    ) -> MoodConjugation:
        ret = MoodConjugation(cast(Mood, mood))
        mood_template = co.template.mood_templates[cast(Mood, mood)]
        for tense in mood_template.tense_templates:
            ret[tense] = self._tense_conjugator._conjugate_mood_tense( # type: ignore
                co,
                mood,
                tense,
                conjugate_pronouns=conjugate_pronouns,
            )
        return ret

    def _get_compound_conjugations_for_mood(
        self,
        co: ConjugationObjects,
        mood: Mood | str,
        conjugate_pronouns: bool = True,
    ) -> MoodConjugation:
        ret = MoodConjugation(cast(Mood, mood))
        comp_conj_map = self._inflector.get_compound_conjugations_aux_verb_map()
        if cast(Mood, mood) in comp_conj_map:
            for tense in comp_conj_map[cast(Mood, mood)]:
                ret[tense] = self._tense_conjugator._conjugate_mood_tense( # type: ignore
                    co,
                    mood,
                    tense,
                    conjugate_pronouns=conjugate_pronouns,
                )
        return ret
