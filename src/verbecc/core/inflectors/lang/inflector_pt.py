from typing import Optional, Tuple

from verbecc.core.conjugator.conjugation_object import ConjugationObjects
from verbecc.core.defs.types.gender import Gender
from verbecc.core.defs.types.lang_code import LangCodeISO639_1
from verbecc.core.defs.types.mood import Mood, Moods
from verbecc.core.defs.types.person import Person
from verbecc.core.defs.types.number import Number
from verbecc.core.defs.types.tense import Tense, Tenses
from verbecc.core.defs.types.lang_specific_options import (
    LangSpecificOptions,
)
from verbecc.core.inflectors.inflector import Inflector
from verbecc.core.defs.types.pronoun import Pronoun, Pronouns


class InflectorPt(Inflector):

    # public:

    def __init__(
        self, lang_specific_options: Optional[LangSpecificOptions] = None
    ) -> None:
        super(InflectorPt, self).__init__()

    def get_lang(self) -> LangCodeISO639_1:
        return LangCodeISO639_1.pt

    def add_subjunctive_relative_pronoun(self, s: str, tense: Tense | str | None) -> str:
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
        pronoun: Optional[Pronoun],
    ) -> str:
        if tense == Tenses.pt.InfinitivoPessoalComposto:
            return s

        if is_reflexive and pronoun is not None:
            s += "-" + self._get_reflexive_suffix_for_pronoun(pronoun)
        else:
            imperative = mood == Moods.pt.Imperativo
            if imperative or (
                mood == Moods.pt.Infinitivo
                and tense == Tenses.pt.InfinitivoPessoalPresente
            ):
                s += " " + self.private_get_pronoun_suffix(
                    person, number, gender, imperative=imperative
                )

        return s

    def get_pronoun_gender(self, pronoun: str) -> Optional[Gender]:
        if pronoun in (Pronouns.pt.ela, Pronouns.pt.elas):
            return Gender.f
        elif pronoun in (Pronouns.pt.ele, Pronouns.pt.eles):
            return Gender.m
        return None

    def get_pronouns(  # noqa: C901
        self,
        person: Optional[Person] = None,
        number: Optional[Number] = None,
        gender: Optional[Gender] = None,
        imperative: bool = False,
    ) -> list[Pronoun]:
        ret = []
        if (person is None or person == Person.First) and (
            number is None or number == Number.Singular
        ):
            p = Pronouns.pt.eu
            ret.append(p)
        if (person is None or person == Person.Second) and (
            number is None or number == Number.Singular
        ):
            p = Pronouns.pt.tu
            ret.append(p)
        if (person is None or person == Person.Third) and (
            number is None or number == Number.Singular
        ):
            pronouns = [Pronouns.pt.ele, Pronouns.pt.ela, Pronouns.pt.você]
            if gender is not None:
                if gender == Gender.m:
                    pronouns = [Pronouns.pt.ele]
                else:
                    pronouns = [Pronouns.pt.ela]
            elif imperative:
                pronouns = [Pronouns.pt.você]
            ret.extend(pronouns)
        if (person is None or person == Person.First) and (
            number is None or number == Number.Plural
        ):
            p = Pronouns.pt.nós
            ret.append(p)
        if (person is None or person == Person.Second) and (
            number is None or number == Number.Plural
        ):
            p = Pronouns.pt.vós
            ret.append(p)
        if (person is None or person == Person.Third) and (
            number is None or number == Number.Plural
        ):
            pronouns = [Pronouns.pt.eles, Pronouns.pt.elas, Pronouns.pt.vocês]
            if gender is not None:
                if gender == Gender.m:
                    pronouns = [Pronouns.pt.eles]
                else:
                    pronouns = [Pronouns.pt.elas]
            elif imperative:
                pronouns = [Pronouns.pt.vocês]
            ret.extend(pronouns)
        return ret

    def make_pronoun_reflexive(self, pronoun: Pronoun) -> str:
        """
        In portuguese, some tenses use reflexive pronoun suffixes
        E.g. Presente: eu visto-me
        while others tenses don't
        E.g. Pretérito Imperfeito: se eu me vestisse
        This function is only for the latter case
        (i.e. when reflexive pronoun is together with subject pronoun)
        """
        if pronoun == Pronouns.pt.eu:
            return pronoun + " me"
        elif pronoun == Pronouns.pt.tu:
            return pronoun + " te"
        elif pronoun == Pronouns.pt.nós:
            return pronoun + " nos"
        elif pronoun == Pronouns.pt.vós:
            return pronoun + " vos"
        else:
            return pronoun + " se"

    def get_tenses_conjugated_without_pronouns(self) -> list[Tense]:
        """
        Many tenses conjugated without pronouns in Spanish are
        conjugated with pronouns in Portuguese.
        E.g. Infinitivo Pessoal (Presente) "por teres tu"
        E.g. Imperativo Afirmativo "tem tu"
        E.g. Imperativo Negativo "não tenhas tu"
        """
        return [
            Tenses.pt.Particípio,
            Tenses.pt.Infinitivo,
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

    def get_imperative_mood(self) -> Mood:
        return Moods.pt.Imperativo

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
    ) -> dict[Mood, dict[Tense, Tuple[Mood, Tense]]]:
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

    def _get_reflexive_suffix_for_pronoun(self, pronoun: Pronoun) -> str:
        if pronoun == Pronouns.pt.eu:
            return "me"
        elif pronoun == Pronouns.pt.tu:
            return "te"
        elif pronoun == Pronouns.pt.nós:
            return "nos"
        elif pronoun == Pronouns.pt.vós:
            return "vos"
        else:
            return "se"

    def private_get_pronoun_suffix(  # noqa: C901
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

    # most Portuguese tenses use a hyphenated reflexive pronoun suffix
    # e.g. "tiver-me vestido"
    # except for these tenses
    # e.g. "se eu me vestisse"
    # e.g. "quando eu me vestir"
    # also Imperativo Negativo (not currently supported)
    def get_unhyphenated_reflexive_mood_tenses(self) -> list[Tuple[Mood, Tense]]:
        return [
            (Moods.pt.Subjuntivo, Tenses.pt.Presente),
            (Moods.pt.Subjuntivo, Tenses.pt.PretéritoImperfeito),
            (Moods.pt.Subjuntivo, Tenses.pt.Futuro),
        ]

    def combine_pronoun_and_conj(
        self,
        pronoun: str,
        conj: str,
        mood: Optional[Mood] = None,
        tense: Optional[Tense] = None,
        reflexive: bool = False,
    ) -> str:
        if (
            reflexive
            and (mood, tense) not in self.get_unhyphenated_reflexive_mood_tenses()
        ):
            # e.g. "eu me" + "tenho" => "eu tenho-me"
            ps, pr = pronoun.split()
            return f"{ps} {conj}-{pr}"
        if tense == Tenses.pt.InfinitivoPessoalPresente:
            return conj + " " + pronoun
        else:
            return pronoun + " " + conj

    def split_reflexive(self, infinitive: str) -> Tuple[bool, str]:
        """
        Tests whether an infinitive is reflexive
        Returns a 2-tuple of whether it is reflexive
        and the non-reflexive form of the infinitive.

        E.g. French:
        "se raser" => (True, "raser")
        "s'habiller" => (True, "habiller")
        "parler" => (False, "parler")
        E.g. Italian:
        "alzarsi" => (True, "alzare")
        "preoccuparsi" => (True, "preoccupare")

        E.g. Spanish
        "levantarse" => (True, "levantar")

        E.g. Portuguese
        "vestir-se" => (True, "vestir")
        """
        if infinitive.endswith("-se"):
            return (True, infinitive[:-3])
        else:
            return (False, infinitive)
