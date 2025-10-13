from typing import Dict, List, Tuple

from verbecc.src.defs.types import exceptions
from verbecc.src.inflectors import inflector
from verbecc.src.utils.string_utils import get_common_letter_count, strip_accents
from verbecc.src.conjugator.conjugation_object import ConjugationObjects


class InflectorCa(inflector.Inflector):
    @property
    def lang(self) -> str:
        return "ca"

    def __init__(self):
        super(InflectorCa, self).__init__()

    def _add_adverb_if_applicable(self, s: str, mood_name: str, tense_name: str) -> str:
        return s

    def _get_default_pronoun(
        self, person: str, gender: str = "m", is_reflexive: bool = False
    ) -> str:
        ret = ""
        if person == "1s":
            ret = "jo"
            if is_reflexive:
                ret += " me"
        elif person == "2s":
            ret = "tu"
            if is_reflexive:
                ret += " te"
        elif person == "3s":
            ret = "ell"
            if gender == "f":
                ret = "ella"
            if is_reflexive:
                ret += " se"
        elif person == "1p":
            ret = "nosaltres"
            if is_reflexive:
                ret += " nos"
        elif person == "2p":
            ret = "vosaltres"
            if is_reflexive:
                ret += " os"
        elif person == "3p":
            ret = "ells"
            if gender == "f":
                ret = "elles"
            if is_reflexive:
                ret += " se"
        return ret

    def _get_tenses_conjugated_without_pronouns(self) -> List[str]:
        return ["particip", "gerundi", "infinitiu-present", "imperatiu-present"]

    def _get_auxilary_verb(
        self,
        co: ConjugationObjects,
        mood_name: str,
        tense_name: str,
    ) -> str:
        return "haver"

    def _get_infinitive_mood_name(self):
        return "infinitiu"

    def _get_indicative_mood_name(self):
        return "indicatiu"

    def _get_subjunctive_mood_name(self):
        return "subjuntiu"

    def _get_conditional_mood_name(self):
        return "condicional"

    def _get_participle_mood_name(self) -> str:
        return "particip"

    def _get_participle_tense_name(self) -> str:
        return "particip"

    def _get_alternate_hv_inflection(self, s: str) -> str:
        # if s.endswith('hay'):
        #     return s[:-1]
        return s

    def _get_compound_conjugations_aux_verb_map(
        self,
    ) -> Dict[str, Dict[str, Tuple[str, ...]]]:
        """
        TODO: Implement all these compound tenses (Spanish compound tenses in this commment, for reference)
        return {
            'indicatiu': {
                'pretèrit-perfet-compuest': ('indicatiu', 'present'),
                'pretèrit-pluscuamperfet': ('indicatiu', 'imperfet'),
                'pretèrit-anterior': ('indicatiu', 'pretèrit'),
                'futur-perfet': ('indicatiu', 'futuro')
            },
            'condicional': {
                'perfet': ('condicional', 'present')
            },
            'subjuntiu': {
                'pretèrit-perfet': ('subjuntiu', 'present'),
                'pretèrit-pluscuamperfet': ('subjuntiu', 'imperfet'),
                'futur-perfet': ('subjuntiu', 'futur')
            }
        }
        """
        return {}

    def _get_verb_stem_from_template_name(self, infinitive: str, template_name: str):
        """Get the verb stem given an ininitive and a colon-delimited template name.
        E.g. infinitive='parlar' template_name='cant:ar' -> 'parl'

        Note: Base class _get_verb_stem_from_template_name raises exception if template
        ending doesn't match infinitive ending exactly but for Catalan, some verbs
        have endings where at least the first letter doesn't match.

        E.g. both 'jaure' and and 'jeure' are apparently conjugated
        identically, so we want either one to use the 'j:aure' template.
        So since this is Catalan, let it pass if the last n-1 letters of the
        template ending match the infinitive ending

        New problem: Template comen:çar ending doesn't match infinitive tòrcer

        Solution we'll just verify that, ignoring accents, the template either
        matches exactly or has at least len(template_ending)-1 characters in
        common.
        Ignoring accents, "çar" and "cer" have 2 characters in common which is at least 3-1
        "aure" and "eure" have 3 characters in common which is at least 4-1
        """
        _, template_ending = template_name.split(":")
        infinitive_no_accents = strip_accents(infinitive)
        template_ending_no_accents = strip_accents(infinitive)
        infinitive_ending_no_accents = infinitive_no_accents[-len(template_ending) :]
        if (
            not infinitive_ending_no_accents == template_ending_no_accents
            and not infinitive_no_accents[1:] == template_ending_no_accents[1:]
            and get_common_letter_count(
                infinitive_ending_no_accents, template_ending_no_accents
            )
            < len(template_ending) - 1
        ):
            raise exceptions.ConjugatorError(
                "Template '{}' ending doesn't "
                "match infinitive '{}', "
                "not even a little bit".format(template_name, infinitive)
            )
        return infinitive[: len(infinitive) - len(template_ending)]
