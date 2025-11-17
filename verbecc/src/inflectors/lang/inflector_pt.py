from typing import Dict, List, Optional, Tuple

from verbecc.src.conjugator.conjugation_object import ConjugationObjects
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.lang_code import LangCodeISO639_1
from verbecc.src.defs.types.mood import Mood, Moods
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.number import Number
from verbecc.src.defs.types.tense import Tense, Tenses
from verbecc.src.defs.types.lang_specific_options import (
    LangSpecificOptions,
)
from verbecc.src.inflectors.inflector import Inflector


class InflectorPt(Inflector):

    # public:

    def __init__(
        self, lang_specific_options: Optional[LangSpecificOptions] = None
    ) -> None:
        super(InflectorPt, self).__init__()

    def get_lang(self) -> LangCodeISO639_1:
        return LangCodeISO639_1.pt

    def add_subjunctive_relative_pronoun(self, s: str, tense: Tense) -> str:
        if tense == Tenses.pt.Presente:
            return "que " + s
        elif tense == Tenses.pt.PretéritoImperfeito:
            return "se " + s
        elif tense == Tenses.pt.Futuro:
            return "quando " + s
        return s

    def add_adverb_if_applicable(self, s: str, mood: Mood, tense: Tense) -> str:
        if mood == Moods.pt.Imperativo and tense == Tenses.pt.Negativo:
            return "não " + s
        elif (
            mood == Moods.pt.Infinitivo and tense == Tenses.pt.InfinitivoPessoalPresente
        ):
            return "por " + s
        return s

    def add_reflexive_pronoun_or_pronoun_suffix_if_applicable(
        self,
        s: str,
        is_reflexive: bool,
        mood: Mood,
        tense: Tense,
        person: Person,
        number: Number,
        gender: Gender,
    ) -> str:
        if tense == Tenses.pt.InfinitivoPessoalComposto:
            return s
        imperative: bool = mood == Moods.pt.Imperativo
        if imperative or (
            mood == Moods.pt.Infinitivo and tense == Tenses.pt.InfinitivoPessoalPresente
        ):
            s += " " + self._get_pronoun_suffix(
                person, number, gender, imperative=imperative
            )
        return s

    def get_pronoun_gender(self, pronoun: str) -> Optional[Gender]:
        if pronoun in ("ela", "elas"):
            return Gender.f
        elif pronoun in ("ele", "eles"):
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
            p = "eu"
            ret.append(p)
        if (person is None or person == Person.Second) and (
            number is None or number == Number.Singular
        ):
            p = "tu"
            ret.append(p)
        if (person is None or person == Person.Third) and (
            number is None or number == Number.Singular
        ):
            pronouns = ["ele", "ela"]
            if gender is not None:
                if gender == Gender.m:
                    pronouns = ["ele"]
                else:
                    pronouns = ["ela"]
            ret.extend(pronouns)
        if (person is None or person == Person.First) and (
            number is None or number == Number.Plural
        ):
            p = "nós"
            ret.append(p)
        if (person is None or person == Person.Second) and (
            number is None or number == Number.Plural
        ):
            p = "vós"
            ret.append(p)
        if (person is None or person == Person.Third) and (
            number is None or number == Number.Plural
        ):
            pronouns = ["eles", "elas"]
            if gender is not None:
                if gender == Gender.m:
                    pronouns = ["eles"]
                else:
                    pronouns = ["elas"]
            ret.extend(pronouns)
        return ret

    def make_pronoun_reflexive(self, pronoun: str) -> str:
        if pronoun == "eu":
            return pronoun + " me"
        elif pronoun == "tu":
            return pronoun + " te"
        elif pronoun == "nós":
            return pronoun + " nos"
        else:
            return pronoun + " se"

    def get_tenses_conjugated_without_pronouns(self) -> List[Tense]:
        return [
            Tenses.pt.Particípio,
            Tenses.pt.Infinitivo,
            Tenses.pt.InfinitivoPessoalPresente,
            Tenses.pt.InfinitivoPessoalComposto,
            Tenses.pt.Afirmativo,
            Tenses.pt.Negativo,
            Tenses.pt.Gerúndio,
        ]

    def get_auxiliary_verb(
        self,
        co: ConjugationObjects,
        mood: Mood,
        tense: Tense,
    ) -> str:
        return "ter"

    def get_infinitive_mood(self) -> Mood:
        return Moods.pt.Infinitivo

    def get_indicative_mood(self) -> Mood:
        return Moods.pt.Indicativo

    def get_subjunctive_mood(self) -> Mood:
        return Moods.pt.Subjuntivo

    def get_conditional_mood(self) -> Mood:
        return Moods.pt.Condicional

    def get_participle_mood(self) -> Mood:
        return Moods.pt.Particípio

    def get_participle_tense(self) -> Tense:
        return Tenses.pt.Particípio

    def get_compound_conjugations_aux_verb_map(
        self,
    ) -> Dict[Mood, Dict[Tense, Tuple[Mood, Tense]]]:
        return {
            Moods.pt.Indicativo: {
                Tenses.pt.PretéritoPerfeitoComposto: (
                    Moods.pt.Indicativo,
                    Tenses.pt.Presente,
                ),
                Tenses.pt.PretéritoMaisQuePerfeitoComposto: (
                    Moods.pt.Indicativo,
                    Tenses.pt.PretéritoImperfeito,
                ),
                Tenses.pt.PretéritoMaisQuePerfeitoAnterior: (
                    Moods.pt.Indicativo,
                    Tenses.pt.PretéritoMaisQuePerfeito,
                ),
                Tenses.pt.FuturoDoPresenteComposto: (
                    Moods.pt.Indicativo,
                    Tenses.pt.FuturoDoPresente,
                ),
            },
            Moods.pt.Subjuntivo: {
                Tenses.pt.PretéritoPerfeito: (Moods.pt.Subjuntivo, Tenses.pt.Presente),
                Tenses.pt.PretéritoMaisQuePerfeito: (
                    Moods.pt.Subjuntivo,
                    Tenses.pt.PretéritoImperfeito,
                ),
                Tenses.pt.FuturoComposto: (Moods.pt.Subjuntivo, Tenses.pt.Futuro),
            },
            Moods.pt.Condicional: {
                Tenses.pt.FuturoDoPretéritoComposto: (
                    Moods.pt.Condicional,
                    Tenses.pt.FuturoDoPretérito,
                )
            },
            Moods.pt.Infinitivo: {
                Tenses.pt.InfinitivoPessoalComposto: (
                    Moods.pt.Infinitivo,
                    Tenses.pt.InfinitivoPessoalPresente,
                )
            },
        }

    # private:

    def _get_pronoun_suffix(
        self,
        person: Person,
        number: Number,
        gender: Gender = Gender.m,
        imperative: bool = True,
    ) -> str:
        ret = ""
        if person == Person.First and number == Number.Singular:
            ret = "eu"
        elif person == Person.Second and number == Number.Singular:
            ret = "tu"
        elif person == Person.Third and number == Number.Singular:
            ret = "você"
            if not imperative:
                ret = "ele"
                if gender == Gender.f:
                    ret = "ela"
        elif person == Person.First and number == Number.Plural:
            ret = "nós"
        elif person == Person.Second and number == Number.Plural:
            ret = "vós"
        elif person == Person.Third and number == Number.Plural:
            ret = "vocês"
            if not imperative:
                ret = "eles"
                if gender == Gender.f:
                    ret = "elas"
        return ret
