from typing import Dict, List, Tuple

from verbecc.src.conjugator.conjugation_object import ConjugationObjects
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.language_codes import LangCodeISO639_1
from verbecc.src.defs.types.mood import MoodPt as Mood
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.tense import TensePt as Tense
from verbecc.src.inflectors.inflector import Inflector


class InflectorPt(Inflector):
    @property
    def lang(self) -> LangCodeISO639_1:
        return LangCodeISO639_1.pt

    def __init__(self) -> None:
        super(InflectorPt, self).__init__()

    def _add_subjunctive_relative_pronoun(self, s: str, tense: Tense) -> str:
        if tense == Tense.Presente:
            return "que " + s
        elif tense == Tense.PretéritoImperfeito:
            return "se " + s
        elif tense == Tense.Futuro:
            return "quando " + s
        return s

    def _add_adverb_if_applicable(self, s: str, mood: Mood, tense: Tense) -> str:
        if mood == Mood.Imperativo and tense == Tense.Negativo:
            return "não " + s
        elif mood == Mood.Infinitivo and tense == Tense.InfinitivoPessoalPresente:
            return "por " + s
        return s

    def _add_reflexive_pronoun_or_pronoun_suffix_if_applicable(
        self,
        s: str,
        is_reflexive: bool,
        mood: Mood,
        tense: Tense,
        person: Person,
    ) -> str:
        imperative: bool = mood == Mood.Imperativo
        if imperative or (
            mood == Mood.Infinitivo and tense == Tense.InfinitivoPessoalPresente
        ):
            s += " " + self._get_pronoun_suffix(person, imperative=imperative)
        return s

    def _get_default_pronoun(
        self,
        person: Person,
        gender: Gender = Gender.m,
        is_reflexive: bool = False,
    ) -> str:
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
            if gender == Gender.f:
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
            if gender == Gender.f:
                ret = "elas"
            if is_reflexive:
                ret += " se"
        return ret

    def _get_pronoun_suffix(
        self, person: Person, gender: Gender = Gender.m, imperative: bool = True
    ) -> str:
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

    def _get_tenses_conjugated_without_pronouns(self) -> List[Tense]:
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
        mood: Mood,
        tense: Tense,
    ) -> str:
        return "ter"

    def _get_infinitive_mood(self) -> Mood:
        return Mood.Infinitivo

    def _get_indicative_mood(self) -> Mood:
        return Mood.Indicativo

    def _get_subjunctive_mood(self) -> Mood:
        return Mood.Subjuntivo

    def _get_conditional_mood(self) -> Mood:
        return Mood.Condicional

    def _get_participle_mood(self) -> Mood:
        return Mood.Particípio

    def _get_participle_tense(self) -> Tense:
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
