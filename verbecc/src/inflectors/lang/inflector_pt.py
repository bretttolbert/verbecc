from typing import Dict, List, Tuple

from verbecc.src.conjugator.conjugation_object import ConjugationObjects
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.language import Language
from verbecc.src.defs.types.mood import MoodPt as Mood
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.tense import TensePt as Tense
from verbecc.src.inflectors.inflector import Inflector


class InflectorPt(Inflector):
    @property
    def lang(self) -> str:
        return Language.Português

    def __init__(self):
        super(InflectorPt, self).__init__()

    def _add_subjunctive_relative_pronoun(self, s: str, tense_name: Tense):
        if tense_name == Tense.Presente:
            return "que " + s
        elif tense_name == Tense.PretéritoImperfeito:
            return "se " + s
        elif tense_name == Tense.Futuro:
            return "quando " + s
        return s

    def _add_adverb_if_applicable(self, s: str, mood_name: Mood, tense_name: Tense):
        if mood_name == Mood.Imperativo and tense_name == Tense.Negativo:
            return "não " + s
        elif (
            mood_name == Mood.Infinitivo
            and tense_name == Tense.InfinitivoPessoalPresente
        ):
            return "por " + s
        return s

    def _add_reflexive_pronoun_or_pronoun_suffix_if_applicable(
        self,
        s: str,
        is_reflexive: bool,
        mood_name: Mood,
        tense_name: Tense,
        person: Person,
    ):
        imperative = mood_name == Mood.Imperativo
        if imperative or (
            mood_name == Mood.Infinitivo
            and tense_name == Tense.InfinitivoPessoalPresente
        ):
            s += " " + self._get_pronoun_suffix(person, imperative=imperative)
        return s

    def _get_default_pronoun(
        self, person: Person, gender: Gender = Gender.Masculine, is_reflexive=False
    ):
        ret = ""
        if person == Person.FirstPersonSingular:
            ret = "eu"
            if is_reflexive:
                ret += " me"
        elif person == Person.SecondPersonSingular:
            ret = "tu"
            if is_reflexive:
                ret += " te"
        elif person == Person.ThirdPersonSingular:
            ret = "ele"
            if gender == Gender.Feminine:
                ret = "ela"
            if is_reflexive:
                ret += " se"
        elif person == Person.FirstPersonPlural:
            ret = "nós"
            if is_reflexive:
                ret += " nos"
        elif person == Person.SecondPersonPlural:
            ret = "vós"
            if is_reflexive:
                ret += " se"
        elif person == Person.ThirdPersonPlural:
            ret = "eles"
            if gender == Gender.Feminine:
                ret = "elas"
            if is_reflexive:
                ret += " se"
        return ret

    def _get_pronoun_suffix(
        self, person: Person, gender: Gender = Gender.Masculine, imperative=True
    ):
        ret = ""
        if person == Person.FirstPersonSingular:
            ret = "eu"
        if person == Person.SecondPersonSingular:
            ret = "tu"
        elif person == Person.ThirdPersonSingular:
            ret = "você"
            if not imperative:
                ret = "ele"
        elif person == Person.FirstPersonPlural:
            ret = "nós"
        elif person == Person.SecondPersonPlural:
            ret = "vós"
        elif person == Person.ThirdPersonPlural:
            ret = "vocês"
            if not imperative:
                ret = "eles"
        return ret

    def _get_tenses_conjugated_without_pronouns(self) -> List[str]:
        return [
            Tense.Particípio,
            Tense.Infinitivo,
            Tense.InfinitivoPessoalPresente,
            Tense.InfinitivoPessoalComposto,
            Tense.Afirmativo,
            Tense.Negativo,
            Tense.Gerúndio,
        ]

    def _get_auxilary_verb(
        self,
        co: ConjugationObjects,
        mood_name: Mood,
        tense_name: Tense,
    ) -> str:
        return "ter"

    def _get_infinitive_mood_name(self):
        return Mood.Infinitivo

    def _get_indicative_mood_name(self):
        return Mood.Indicativo

    def _get_subjunctive_mood_name(self) -> str:
        return Mood.Subjuntivo

    def _get_conditional_mood_name(self):
        return Mood.Condicional

    def _get_participle_mood_name(self) -> str:
        return Mood.Particípio

    def _get_participle_tense_name(self) -> str:
        return Tense.Particípio

    def _get_compound_conjugations_aux_verb_map(
        self,
    ) -> Dict[Mood, Dict[Tense, Tuple[Mood, Tense]]]:
        return {
            Mood.Indicativo: {
                Tense.PretéritoPerfeitoComposto: (Mood.Indicativo, Tense.Presente),
                Tense.PretéritoMaisQuePerfeitoComposto: (
                    Mood.Indicativo,
                    Tense.PretéritoImperfeito,
                ),
                Tense.PretéritoMaisQuePerfeitoAnterior: (
                    Mood.Indicativo,
                    Tense.PretéritoMaisQuePerfeito,
                ),
                Tense.FuturoDoPresenteComposto: (
                    Mood.Indicativo,
                    Tense.FuturoDoPresente,
                ),
            },
            Mood.Subjuntivo: {
                Tense.PretéritoPerfeito: (Mood.Subjuntivo, Tense.Presente),
                Tense.PretéritoMaisQuePerfeito: (
                    Mood.Subjuntivo,
                    Tense.PretéritoImperfeito,
                ),
                Tense.FuturoComposto: (Mood.Subjuntivo, Tense.Futuro),
            },
            Mood.Condicional: {
                Tense.FuturoDoPretéritoComposto: (
                    Mood.Condicional,
                    Tense.FuturoDoPretérito,
                )
            },
            Mood.Infinitivo: {
                Tense.InfinitivoPessoalComposto: (
                    Mood.Infinitivo,
                    Tense.InfinitivoPessoalPresente,
                )
            },
        }
