from typing import Dict, List, Tuple

from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.language_codes import LangISOCode639_1
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.mood import MoodEs as Mood
from verbecc.src.defs.types.tense import TenseEs as Tense
from verbecc.src.inflectors.inflector import Inflector
from verbecc.src.conjugator.conjugation_object import ConjugationObjects


class InflectorEs(Inflector):
    @property
    def lang(self) -> LangISOCode639_1:
        return LangISOCode639_1.Es

    def __init__(self) -> None:
        super(InflectorEs, self).__init__()

    def _add_adverb_if_applicable(self, s: str, mood: Mood, tense: Tense) -> str:
        if mood == Mood.Imperativo and tense == Tense.Negativo:
            return "no " + s
        return s

    def _get_default_pronoun(
        self,
        person: Person,
        gender: Gender = Gender.M,
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
            if gender == Gender.F:
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
            if gender == Gender.F:
                ret = "ellas"
            if is_reflexive:
                ret += " se"
        return ret

    def _get_tenses_conjugated_without_pronouns(self) -> List[Tense]:
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
        mood: Mood,
        tense: Tense,
    ) -> str:
        return "haber"

    def _get_infinitive_mood(self) -> Mood:
        return Mood.Infinitivo

    def _get_indicative_mood(self) -> Mood:
        return Mood.Indicativo

    def _get_subjunctive_mood(self) -> Mood:
        return Mood.Subjuntivo

    def _get_conditional_mood(self) -> Mood:
        return Mood.Condicional

    def _get_participle_mood(self) -> Mood:
        return Mood.Participo

    def _get_participle_tense(self) -> Mood:
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
