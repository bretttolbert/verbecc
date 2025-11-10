from typing import Dict, List, Optional, Tuple

from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.lang_code import LangCodeISO639_1
from verbecc.src.defs.types.mood import Mood, Moods
from verbecc.src.defs.types.participle_inflection import ParticipleInflection
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.number import Number
from verbecc.src.defs.types.tense import Tense, Tenses
from verbecc.src.defs.types.lang_specific_options import (
    LangSpecificOptions,
)
from verbecc.src.conjugator.conjugation_object import ConjugationObjects
from verbecc.src.inflectors.inflector import Inflector
from verbecc.src.utils import string_utils

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

    @property
    def lang(self) -> LangCodeISO639_1:
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

    def add_subjunctive_relative_pronoun(self, s: str, tense: Tense) -> str:
        return "che " + s

    def get_default_pronoun(
        self,
        person: Person,
        number: Number,
        gender: Gender = Gender.m,
        is_reflexive: bool = False,
    ) -> str:
        ret = ""
        if person == Person.First and number == Number.Singular:
            ret = "io"
            if is_reflexive:
                ret += " mi"
        elif person == Person.Second and number == Number.Singular:
            ret = "tu"
            if is_reflexive:
                ret += " ti"
        elif person == Person.Third and number == Number.Singular:
            ret = "lui"
            if gender == Gender.f:
                ret = "lei"
            if is_reflexive:
                ret += " si"
        elif person == Person.First and number == Number.Plural:
            ret = "noi"
            if is_reflexive:
                ret += " ci"
        elif person == Person.Second and number == Number.Plural:
            ret = "voi"
            if is_reflexive:
                ret += " vi"
        elif person == Person.Third and number == Number.Plural:
            ret = "loro"
            if is_reflexive:
                ret += " si"
        return ret

    def get_tenses_conjugated_without_pronouns(self) -> List[Tense]:
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
    ) -> Dict[Mood, Dict[Tense, Tuple[Mood, Tense]]]:
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
