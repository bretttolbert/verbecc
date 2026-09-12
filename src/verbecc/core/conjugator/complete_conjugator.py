from typing import Optional

from verbecc.core.conjugator.abstract_conjugator import AbstractConjugator
from verbecc.core.conjugator.mood_conjugator import MoodConjugator
from verbecc.core.defs.types.conjugation.complete_conjugation import CompleteConjugation
from verbecc.core.defs.types.conjugation.mood_conjugation import MoodConjugation
from verbecc.core.defs.types.conjugation.moods_conjugation import MoodsConjugation
from verbecc.core.defs.types.conjugation.verb_info import VerbInfo
from verbecc.core.defs.types.lang_code import LangCodeISO639_1
from verbecc.core.defs.types.lang_specific_options import LangSpecificOptions
from verbecc.core.defs.types.mood import Mood
from verbecc.core.defs.types.tense import Tense
from verbecc.core.defs.types.conjugation.tense_conjugation import TenseConjugation
from verbecc.core.inflectors.inflector import Inflector


class CompleteConjugator(AbstractConjugator):
    """
    CompleteConjugator encapsulates all conjugation logic that is not language-specific.
    CompleteConjugator uses a concrete instance of Inflector for all language-specific
    conjugation logic.
    """

    def __init__(
        self,
        lang: LangCodeISO639_1,
        lang_specific_options: Optional[LangSpecificOptions] = None,
    ) -> None:
        super().__init__(lang, lang_specific_options, self.__class__.__name__)
        self._mood_conjugator = MoodConjugator(
            lang, lang_specific_options, self._inflector
        )

    def conjugate(
        self,
        infinitive: str,
        conjugate_pronouns: bool = True,
    ) -> CompleteConjugation:
        """
        :param infinitive: the infinitive form of the verb to conjugate
        :type infinitive: str

        :param conjugate_pronouns: if True, verbecc will conjugate the pronoun together with
        its inflected form, e.g. for the French verb apprendre, for the first-person singular
        present tense you'd get "j'apprends" if True or "apprends" if False.
        :type conjugate_pronouns: bool

        :param lang_specific_options: options specific to certain languages.
        :type lang_specific_options: LangSpecificOptions
        """
        co = self._get_conj_objs(infinitive)
        moods = MoodsConjugation()
        for mood, _ in co.template.mood_templates.items():
            moods[mood] = self._mood_conjugator._conjugate_mood( # type: ignore
                co,
                mood,
                conjugate_pronouns,
            )
        return CompleteConjugation(
            VerbInfo(
                self._inflector.get_lang(),
                co.verb.infinitive,
                co.verb.predicted,
                co.verb.pred_score,
                co.verb.template,
                co.verb.translation_en,
                co.verb_stem,
            ),
            moods,
        )

    def conjugate_mood(
        self,
        infinitive: str,
        mood: Mood | str,
        conjugate_pronouns: bool = True,
    ) -> MoodConjugation:
        return self._mood_conjugator.conjugate_mood(
            infinitive,
            mood,
            conjugate_pronouns=conjugate_pronouns,
        )

    def conjugate_mood_tense(
        self,
        infinitive: str,
        mood: Mood | str,
        tense: Tense | str,
        conjugate_pronouns: bool = True,
    ) -> TenseConjugation:
        return self._mood_conjugator.conjugate_mood_tense(
            infinitive,
            mood,
            tense,
            conjugate_pronouns=conjugate_pronouns,
        )

    def _get_inflector(self) -> Inflector:
        return self._inflector
