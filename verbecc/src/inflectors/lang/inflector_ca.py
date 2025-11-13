from typing import Dict, List, Optional, Tuple

from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.number import Number
from verbecc.src.defs.types.mood import Mood, Moods
from verbecc.src.defs.types.tense import Tense, Tenses
from verbecc.src.defs.types import exceptions
from verbecc.src.defs.types.lang_code import LangCodeISO639_1
from verbecc.src.defs.types.lang_specific_options import (
    LangSpecificOptions,
)
from verbecc.src.inflectors import inflector
from verbecc.src.utils.string_utils import get_common_letter_count, strip_accents
from verbecc.src.conjugator.conjugation_object import ConjugationObjects


class InflectorCa(inflector.Inflector):
    def __init__(
        self, lang_specific_options: Optional[LangSpecificOptions] = None
    ) -> None:
        super(InflectorCa, self).__init__()

    @property
    def lang(self) -> LangCodeISO639_1:
        return LangCodeISO639_1.ca

    def add_adverb_if_applicable(self, s: str, mood: Mood, tense: Tense) -> str:
        return s

    def get_pronoun_gender(self, pronoun: str) -> Optional[Gender]:
        if pronoun in ("ella", "elles"):
            return Gender.f
        elif pronoun in ("ell", "ells"):
            return Gender.m
        return None

    def get_pronouns(
        self,
        person: Optional[Person] = None,
        number: Optional[Number] = None,
        gender: Optional[Gender] = None,
    ) -> List[str]:
        ret = []
        if (person is None or person == Person.First) and (
            number is None or number == Number.Singular
        ):
            p = "jo"
            ret.append(p)
        if (person is None or person == Person.Second) and (
            number is None or number == Number.Singular
        ):
            p = "tu"
            ret.append(p)
        if (person is None or person == Person.Third) and (
            number is None or number == Number.Singular
        ):
            pronouns = ["ell", "ella"]
            if gender is not None:
                if gender == Gender.m:
                    pronouns = ["ell"]
                else:
                    pronouns = ["ella"]
            ret.extend(pronouns)
        if (person is None or person == Person.First) and (
            number is None or number == Number.Plural
        ):
            p = "nosaltres"
            ret.append(p)
        if (person is None or person == Person.Second) and (
            number is None or number == Number.Plural
        ):
            p = "vosaltres"
            ret.append(p)
        if (person is None or person == Person.Third) and (
            number is None or number == Number.Plural
        ):
            pronouns = ["ells", "elles"]
            if gender is not None:
                if gender == Gender.m:
                    pronouns = ["ells"]
                else:
                    pronouns = ["elles"]
            ret.extend(pronouns)
        return ret

    def make_pronoun_reflexive(self, pronoun: str) -> str:
        if pronoun == "jo":
            return pronoun + " me"
        elif pronoun == "tu":
            return pronoun + " te"
        elif pronoun == "vosaltres":
            return pronoun + " os"
        elif pronoun == "nosaltres":
            return pronoun + " nos"
        else:
            return pronoun + " se"

    def get_tenses_conjugated_without_pronouns(self) -> List[Tense]:
        return [
            Tenses.ca.Particip,
            Tenses.ca.Gerundi,
            Tenses.ca.InfinitiuPresent,
            Tenses.ca.ImperatiuPresent,
        ]

    def get_auxiliary_verb(
        self,
        co: ConjugationObjects,
        mood: Mood,
        tense: Tense,
    ) -> str:
        return "haver"

    def get_infinitive_mood(self) -> Mood:
        return Moods.ca.Infinitiu

    def get_indicative_mood(self) -> Mood:
        return Moods.ca.Indicatiu

    def get_subjunctive_mood(self) -> Mood:
        return Moods.ca.Subjuntiu

    def get_conditional_mood(self) -> Mood:
        return Moods.ca.Condicional

    def get_participle_mood(self) -> Mood:
        return Moods.ca.Participi

    def get_participle_tense(self) -> Tense:
        return Tenses.ca.Particip

    def get_alternate_hv_inflection(self, s: str) -> str:
        # if s.endswith('hay'):
        #     return s[:-1]
        return s

    def get_compound_conjugations_aux_verb_map(
        self,
    ) -> Dict[Mood, Dict[Tense, Tuple[Mood, Tense]]]:
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

    def get_verb_stem_from_template_name(
        self, infinitive: str, template_name: str
    ) -> str:
        """Get the verb stem given an ininitive and a colon-delimited template name.
        E.g. infinitive='parlar' template_name='cant:ar' -> 'parl'

        Note: Base class get_verb_stem_from_template_name raises exception if template
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
