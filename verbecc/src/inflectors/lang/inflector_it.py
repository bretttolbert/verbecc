from typing import Dict, List, Tuple

from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.language_codes import LangCodeISO639_1
from verbecc.src.defs.types.mood import MoodIt as Mood
from verbecc.src.defs.types.partiple_inflection import ParticipleInflection
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.tense import TenseIt as Tense
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
    @property
    def lang(self) -> LangCodeISO639_1:
        return LangCodeISO639_1.it

    def __init__(self) -> None:
        super(InflectorIt, self).__init__()

    def _is_auxilary_verb_inflected(self, auxilary_verb: str) -> bool:
        return auxilary_verb == "essere"

    def _split_reflexive(self, infinitive: str) -> Tuple[bool, str]:
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

    def _add_reflexive_pronoun(self, s: str) -> str:
        if string_utils.starts_with_vowel(s, h_is_vowel=True):
            return "s'" + s
        else:
            return "si " + s

    def _add_subjunctive_relative_pronoun(self, s: str, tense: Tense) -> str:
        return "che " + s

    def _get_default_pronoun(
        self,
        person: Person,
        gender: Gender = Gender.m,
        is_reflexive: bool = False,
    ) -> str:
        ret = ""
        if person == Person.FirstPersonSingular:
            ret = "io"
            if is_reflexive:
                ret += " mi"
        elif person == Person.SecondPersonSingular:
            ret = "tu"
            if is_reflexive:
                ret += " ti"
        elif person == Person.ThirdPersonSingular:
            ret = "lui"
            if gender == Gender.f:
                ret = "lei"
            if is_reflexive:
                ret += " si"
        elif person == Person.FirstPersonPlural:
            ret = "noi"
            if is_reflexive:
                ret += " ci"
        elif person == Person.SecondPersonPlural:
            ret = "voi"
            if is_reflexive:
                ret += " vi"
        elif person == Person.ThirdPersonPlural:
            ret = "loro"
            if is_reflexive:
                ret += " si"
        return ret

    def _get_tenses_conjugated_without_pronouns(self) -> List[Tense]:
        return [
            Tense.Affermativo,
            Tense.negativo,
            Tense.Negativo,
            Tense.Gerundio,
            Tense.ParticipioPresente,
            Tense.ParticipioPassato,
        ]

    def _get_auxilary_verb(
        self, co: ConjugationObjects, mood: Mood, tense: Tense
    ) -> str:
        ret = "avere"
        if co.verb.infinitive in VERBS_CONJUGATED_WITH_ESSERE or co.is_reflexive:
            ret = "essere"
        return ret

    def _get_infinitive_mood(self) -> Mood:
        return Mood.Infinito

    def _get_indicative_mood(self) -> Mood:
        return Mood.Indicativo

    def _get_subjunctive_mood(self) -> Mood:
        return Mood.Congiuntivo

    def _get_conditional_mood(self) -> Mood:
        return Mood.Condizionale

    def _get_participle_mood(self) -> Mood:
        return Mood.Participio

    def _get_participle_tense(self) -> Tense:
        return Tense.ParticipioPassato

    def _get_compound_conjugations_aux_verb_map(
        self,
    ) -> Dict[Mood, Dict[Tense, Tuple[Mood, Tense]]]:
        return {
            Mood.Indicativo: {
                Tense.PassatoProssimo: (Mood.Indicativo, Tense.Presente),
                Tense.TrapassatoProssimo: (Mood.Indicativo, Tense.Imperfetto),
                Tense.TrapassatoRemoto: (Mood.Indicativo, Tense.PassatoRemoto),
                Tense.FuturoAnteriore: (Mood.Indicativo, Tense.Futuro),
            },
            Mood.Congiuntivo: {
                Tense.Passato: (Mood.Congiuntivo, Tense.Presente),
                Tense.Trapassato: (Mood.Congiuntivo, Tense.Imperfetto),
            },
            Mood.Condizionale: {Tense.Passato: (Mood.Condizionale, Tense.Presente)},
        }

    PARTICIPLE_INFLECTIONS: Tuple[
        ParticipleInflection,
        ParticipleInflection,
        ParticipleInflection,
        ParticipleInflection,
    ] = (
        ParticipleInflection.MasculineSingular,
        ParticipleInflection.FeminineSingular,
        ParticipleInflection.MasculinePlural,
        ParticipleInflection.FemininePlural,
    )

    def _get_participle_index_for_participle_inflection(
        self, participle_inflection: ParticipleInflection
    ) -> int:
        """
        Default order is like French XML file, i.e. MS, MP, FS, FP
        But in some lang XML files, e.g. Italian, the order is MS, FS, MP, FP,
        so use the PARTICIPLE_INFLECTIONS above instead of the default one
        in grammar defines, for now.
        TODO: Standardize the XML files
        """
        return self.PARTICIPLE_INFLECTIONS.index(participle_inflection)
