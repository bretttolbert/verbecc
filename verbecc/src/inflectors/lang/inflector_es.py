from typing import Dict, List, Tuple

from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.mood import MoodEs as Mood
from verbecc.src.defs.types.tense import TenseEs as Tense
from verbecc.src.inflectors.inflector import Inflector
from verbecc.src.conjugator.conjugation_object import ConjugationObjects


class InflectorEs(Inflector):
    @property
    def lang(self) -> str:
        return "es"

    def __init__(self):
        super(InflectorEs, self).__init__()

    def _add_adverb_if_applicable(
        self, s: str, mood_name: Mood, tense_name: Tense
    ) -> str:
        if mood_name == Mood.Imperativo and tense_name == Tense.Negativo:
            return "no " + s
        return s

    def _get_default_pronoun(
        self,
        person: Person,
        gender: Gender = Gender.Masculine,
        is_reflexive: bool = False,
    ) -> str:
        ret = ""
        if person == Person.FirstPersonSingular:
            ret = "yo"
            if is_reflexive:
                ret += " me"
        elif person == Person.SecondPersonSingular:
            ret = "tú"
            if is_reflexive:
                ret += " te"
        elif person == Person.ThirdPersonSingular:
            ret = "él"
            if gender == Gender.Feminine:
                ret = "ella"
            if is_reflexive:
                ret += " se"
        elif person == Person.FirstPersonPlural:
            ret = "nosotros"
            if is_reflexive:
                ret += " nos"
        elif person == Person.SecondPersonPlural:
            ret = "vosotros"
            if is_reflexive:
                ret += " os"
        elif person == Person.ThirdPersonPlural:
            ret = "ellos"
            if gender == Gender.Feminine:
                ret = "ellas"
            if is_reflexive:
                ret += " se"
        return ret

    def _get_tenses_conjugated_without_pronouns(self) -> List[str]:
        return [
            Tense.Participo,
            Tense.Gerundio,
            Tense.Infinitivo,
            Tense.Afirmativo,
            Tense.Negativo,
        ]

    def _get_auxilary_verb(
        self,
        co: ConjugationObjects,
        mood_name: Mood,
        tense_name: Tense,
    ) -> str:
        return "haber"

    def _get_infinitive_mood_name(self):
        return Mood.Infinitivo

    def _get_indicative_mood_name(self):
        return Mood.Indicativo

    def _get_subjunctive_mood_name(self):
        return Mood.Subjuntivo

    def _get_conditional_mood_name(self):
        return Mood.Condicional

    def _get_participle_mood_name(self) -> str:
        return Mood.Participo

    def _get_participle_tense_name(self) -> str:
        return Tense.Participo

    def _get_alternate_hv_inflection(self, s: str) -> str:
        if s.endswith("hay"):
            return s[:-1]
        return s

    def _get_compound_conjugations_aux_verb_map(
        self,
    ) -> Dict[Mood, Dict[Tense, Tuple[Mood, Tense]]]:
        return {
            Mood.Indicativo: {
                Tense.PretéritoPerfectoCompuesto: (
                    Mood.Indicativo,
                    Tense.Presente,
                ),
                Tense.PretéritoPluscuamperfecto: (
                    Mood.Indicativo,
                    Tense.PretéritoImperfecto,
                ),
                Tense.PretéritoAnterior: (
                    Mood.Indicativo,
                    Tense.PretéritoPerfectoSimple,
                ),
                Tense.FuturoPerfecto: (Mood.Indicativo, Tense.Futuro),
            },
            Mood.Condicional: {Tense.Perfecto: (Mood.Condicional, Tense.Presente)},
            Mood.Subjuntivo: {
                Tense.PretéritoPerfecto: (Mood.Subjuntivo, Tense.Presente),
                Tense.PretéritoPluscuamperfecto1: (
                    Mood.Subjuntivo,
                    Tense.PretéritoImperfecto1,
                ),
                Tense.PretéritoPluscuamperfecto2: (
                    Mood.Subjuntivo,
                    Tense.PretéritoImperfecto2,
                ),
                Tense.FuturoPerfecto: (Mood.Subjuntivo, Tense.Futuro),
            },
        }
