from typing import Optional, Tuple

from verbecc.core.defs.types.gender import Gender
from verbecc.core.defs.types.lang_code import LangCodeISO639_1
from verbecc.core.defs.types.mood import Mood, Moods
from verbecc.core.defs.types.person import Person
from verbecc.core.defs.types.number import Number
from verbecc.core.defs.types.tense import Tense, Tenses
from verbecc.core.defs.types.lang_specific_options import (
    LangSpecificOptions,
)
from verbecc.core.conjugator.conjugation_object import ConjugationObjects
from verbecc.core.inflectors.inflector import Inflector
from verbecc.core.utils import string_utils
from verbecc.core.defs.types.pronoun import Pronoun, Pronouns

VERBS_CONJUGATED_WITH_ESSERE = [
    "essere",
    "andare",
    "arrivare",
    "cadere",
    "entrare",
    "partire",
    "rimanere",
    "uscire",
    "venire",
    "stare",
    "passare",
    "diventare",
    "crescere",
    "morire",
    "nascere",
]


class InflectorIt(Inflector):
    def __init__(
        self, lang_specific_options: Optional[LangSpecificOptions] = None
    ) -> None:
        super(InflectorIt, self).__init__()

    def get_lang(self) -> LangCodeISO639_1:
        return LangCodeISO639_1.it

    def is_auxiliary_verb_inflected(self, auxiliary_verb: str) -> bool:
        return auxiliary_verb == "essere"

    def split_reflexive(self, infinitive: str) -> Tuple[bool, str]:
        """
        E.g. Italian:
        "alzarsi" => (True, "alzare")
        "preoccuparsi" => (True, "preoccupare")

        TODO:
        Negative reflextive verbs:
        "non capire"
        """
        is_reflexive = False
        if infinitive.endswith("si"):
            is_reflexive = True
            infinitive = infinitive[:-2] + "e"  # "alzarsi" => "alzare"
        elif infinitive.startswith("si "):
            is_reflexive = True
            infinitive = infinitive[3:]
        elif infinitive.startswith("s'"):
            is_reflexive = True
            infinitive = infinitive[2:]
        return is_reflexive, infinitive

    def add_reflexive_pronoun(self, s: str) -> str:
        if string_utils.starts_with_vowel(s, h_is_vowel=True):
            return "s'" + s
        else:
            return "si " + s

    def add_subjunctive_relative_pronoun(self, s: str, tense: Tense | str | None) -> str:
        return "che " + s

    def get_pronoun_gender(self, pronoun: Pronoun) -> Optional[Gender]:
        if pronoun == Pronouns.it.lei:
            return Gender.f
        elif pronoun == Pronouns.it.lui:
            return Gender.m
        return None

    def get_pronouns(
        self,
        person: Optional[Person] = None,
        number: Optional[Number] = None,
        gender: Optional[Gender] = None,
        imperative: bool = False,
    ) -> list[Pronoun]:
        ret: list[Pronoun] = []
        if (person is None or person == Person.First) and (
            number is None or number == Number.Singular
        ):
            p = Pronouns.it.io
            ret.append(p)
        if (person is None or person == Person.Second) and (
            number is None or number == Number.Singular
        ):
            p = Pronouns.it.tu
            ret.append(p)
        if (person is None or person == Person.Third) and (
            number is None or number == Number.Singular
        ):
            pronouns = [Pronouns.it.lui, Pronouns.it.lei]
            if gender is not None:
                if gender == Gender.m:
                    pronouns = [Pronouns.it.lui]
                else:
                    pronouns = [Pronouns.it.lei]
            ret.extend(pronouns)
        if (person is None or person == Person.First) and (
            number is None or number == Number.Plural
        ):
            p = Pronouns.it.noi
            ret.append(p)
        if (person is None or person == Person.Second) and (
            number is None or number == Number.Plural
        ):
            p = Pronouns.it.voi
            ret.append(p)
        if (person is None or person == Person.Third) and (
            number is None or number == Number.Plural
        ):
            p = Pronouns.it.loro
            ret.append(p)
        return ret

    def make_pronoun_reflexive(self, pronoun: Pronoun) -> str:
        if pronoun == Pronouns.it.io:
            return pronoun + " mi"
        elif pronoun == Pronouns.it.tu:
            return pronoun + " ti"
        elif pronoun == Pronouns.it.voi:
            return pronoun + " vi"
        elif pronoun == Pronouns.it.noi:
            return pronoun + " ci"
        else:
            return pronoun + " si"

    def get_tenses_conjugated_without_pronouns(self) -> list[Tense]:
        return [
            Tenses.it.Affermativo,
            Tenses.it.negativo,
            Tenses.it.Negativo,
            Tenses.it.Gerundio,
            Tenses.it.ParticipioPresente,
            Tenses.it.ParticipioPassato,
        ]

    def get_auxiliary_verb(
        self, co: ConjugationObjects, mood: Mood, tense: Tense
    ) -> str:
        ret = "avere"
        if co.verb.infinitive in VERBS_CONJUGATED_WITH_ESSERE or co.is_reflexive:
            ret = "essere"
        return ret

    def get_infinitive_mood(self) -> Mood:
        return Moods.it.Infinito

    def get_imperative_mood(self) -> Mood:
        return Moods.it.Imperativo

    def get_indicative_mood(self) -> Mood:
        return Moods.it.Indicativo

    def get_subjunctive_mood(self) -> Mood:
        return Moods.it.Congiuntivo

    def get_conditional_mood(self) -> Mood:
        return Moods.it.Condizionale

    def get_participle_mood(self) -> Mood:
        return Moods.it.Participio

    def get_participle_tense(self) -> Tense:
        return Tenses.it.ParticipioPassato

    def get_compound_conjugations_aux_verb_map(
        self,
    ) -> dict[Mood, dict[Tense, Tuple[Mood, Tense]]]:
        return {
            Moods.it.Indicativo: {
                Tenses.it.PassatoProssimo: (Moods.it.Indicativo, Tenses.it.Presente),
                Tenses.it.TrapassatoProssimo: (
                    Moods.it.Indicativo,
                    Tenses.it.Imperfetto,
                ),
                Tenses.it.TrapassatoRemoto: (
                    Moods.it.Indicativo,
                    Tenses.it.PassatoRemoto,
                ),
                Tenses.it.FuturoAnteriore: (Moods.it.Indicativo, Tenses.it.Futuro),
            },
            Moods.it.Congiuntivo: {
                Tenses.it.Passato: (Moods.it.Congiuntivo, Tenses.it.Presente),
                Tenses.it.Trapassato: (Moods.it.Congiuntivo, Tenses.it.Imperfetto),
            },
            Moods.it.Condizionale: {
                Tenses.it.Passato: (Moods.it.Condizionale, Tenses.it.Presente)
            },
        }
