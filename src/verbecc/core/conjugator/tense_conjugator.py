from typing import Optional, cast

from verbecc.core.conjugator.conjugation_object import ConjugationObjects
from verbecc.core.defs.types.mood import Mood
from verbecc.core.defs.types.tense import Tense
from verbecc.core.defs.types.exceptions import InvalidTenseError
from verbecc.core.defs.types.conjugation.tense_conjugation import TenseConjugation
from verbecc.core.defs.types.lang_specific_options import LangSpecificOptions
from verbecc.core.defs.types.lang_code import LangCodeISO639_1
from verbecc.core.inflectors.inflector import Inflector
from verbecc.core.conjugator.abstract_conjugator import AbstractConjugator
from verbecc.core.conjugator.tense_conjugator_simple import TenseConjugatorSimple
from verbecc.core.conjugator.tense_conjugator_compound import TenseConjugatorCompound
from verbecc.core.utils.warnings import NonApiWarning


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
        mood: Mood | str,
        tense: Tense | str,
        conjugate_pronouns: bool = True,
    ) -> TenseConjugation:
        co = self.get_co(infinitive)
        return self.co_conjugate_mood_tense(
            co,
            mood,
            tense,
            conjugate_pronouns=conjugate_pronouns,
        )

    def co_conjugate_mood_tense(
        self,
        co: ConjugationObjects,
        mood: Mood | str,
        tense: Tense | str,
        conjugate_pronouns: bool = True,
    ) -> TenseConjugation:
        comp_conj_map = self._inflector.get_compound_conjugations_aux_verb_map()
        mood_key = cast(Mood, mood)
        tense_key = cast(Tense, tense)
        if mood_key in comp_conj_map and tense_key in comp_conj_map[mood_key]:
            aux_mood, aux_tense = comp_conj_map[mood_key][tense_key]
            aux_uses_alternate = (
                self._inflector.auxiliary_verb_uses_alternate_conjugation(tense_key)
            )
            return self._tense_conjugator_compound.co_conjugate_compound_mood_tense(
                co,
                mood_key,
                tense_key,
                aux_mood,
                aux_tense,
                aux_uses_alternate,
                conjugate_pronouns=conjugate_pronouns,
            )
        else:
            mood_template = co.template.mood_templates[mood_key]
            if tense_key not in mood_template.tense_templates:
                raise InvalidTenseError()
            tense_template = mood_template.tense_templates[tense_key]
            return self._tense_conjugator_simple.conjugate_simple_mood_tense(
                co.verb_stem,
                mood_key,
                tense_key,
                tense_template,
                is_reflexive=co.is_reflexive,
                modify_stem_strip_accents=bool(
                    co.template.modify_stem == "strip-accents"
                ),
                conjugate_pronouns=conjugate_pronouns,
            )

    def private_get_tense_conjugator_simple(self) -> TenseConjugatorSimple:
        NonApiWarning.warn()
        return self._tense_conjugator_simple

    def private_get_tense_conjugator_compound(self) -> TenseConjugatorCompound:
        NonApiWarning.warn()
        return self._tense_conjugator_compound
