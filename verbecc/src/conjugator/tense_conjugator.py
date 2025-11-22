from typing import Optional

from verbecc.src.conjugator.conjugation_object import ConjugationObjects
from verbecc.src.defs.types.mood import Mood
from verbecc.src.defs.types.tense import Tense
from verbecc.src.defs.types.exceptions import InvalidTenseError
from verbecc.src.defs.types.conjugation.tense_conjugation import TenseConjugation
from verbecc.src.defs.types.lang_specific_options import LangSpecificOptions
from verbecc.src.defs.types.lang_code import LangCodeISO639_1
from verbecc.src.inflectors.inflector import Inflector
from verbecc.src.conjugator.abstract_conjugator import AbstractConjugator
from verbecc.src.conjugator.tense_conjugator_simple import TenseConjugatorSimple
from verbecc.src.conjugator.tense_conjugator_compound import TenseConjugatorCompound


class TenseConjugator(AbstractConjugator):
    """
    TenseConjugator encapsulates all tense conjugation logic that is not language-specific.
    TenseConjugator uses a concrete instance of Inflector for all language-specific
    conjugation logic.
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
        self._tense_conjugator_simple = TenseConjugatorSimple(
            lang, lang_specific_options, self._inflector
        )
        self._tense_conjugator_compound = TenseConjugatorCompound(
            lang, lang_specific_options, self._tense_conjugator_simple
        )

    def conjugate_mood_tense(
        self,
        infinitive: str,
        mood: Mood,
        tense: Tense,
        conjugate_pronouns: bool = True,
    ) -> TenseConjugation:
        co = self._get_conj_obs(infinitive)
        return self._conjugate_mood_tense(
            co,
            mood,
            tense,
            conjugate_pronouns=conjugate_pronouns,
        )

    def _conjugate_mood_tense(
        self,
        co: ConjugationObjects,
        mood: Mood,
        tense: Tense,
        conjugate_pronouns: bool = True,
    ) -> TenseConjugation:
        comp_conj_map = self._inflector.get_compound_conjugations_aux_verb_map()
        if mood in comp_conj_map and tense in comp_conj_map[mood]:
            aux_mood, aux_tense = comp_conj_map[mood][tense]
            aux_uses_alternate = (
                self._inflector.auxiliary_verb_uses_alternate_conjugation(tense)
            )
            return self._tense_conjugator_compound._conjugate_compound_mood_tense(
                co,
                mood,
                tense,
                aux_mood,
                aux_tense,
                aux_uses_alternate,
                conjugate_pronouns=conjugate_pronouns,
            )
        else:
            mood_template = co.template.mood_templates[mood]
            if tense not in mood_template.tense_templates:
                raise InvalidTenseError()
            tense_template = mood_template.tense_templates[tense]
            return self._tense_conjugator_simple._conjugate_simple_mood_tense(
                co.verb_stem,
                mood,
                tense,
                tense_template,
                is_reflexive=co.is_reflexive,
                modify_stem_strip_accents=bool(
                    co.template.modify_stem == "strip-accents"
                ),
                conjugate_pronouns=conjugate_pronouns,
            )
