from typing import Dict, List, Tuple

from verbecc.src.conjugator.conjugation_object import ConjugationObjects
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.lang_code import LangCodeISO639_1
from verbecc.src.defs.types.mood import MoodFr as Mood
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.constants.grammar_defines import PERSONS
from verbecc.src.defs.types.tense import TenseFr as Tense
from verbecc.src.defs.types.lang_specific_options import (
    LangSpecificOptions,
)
from verbecc.src.inflectors.inflector import Inflector
from verbecc.src.utils import string_utils

"""
DR & MRS VANDERTRAMPP verbs
"""
VERBS_CONJUGATED_WITH_ETRE = [
    "aller",
    "arriver",
    "descendre",
    "redescendre",
    "entrer",
    "rentrer",
    "monter",
    "remonter",
    "mourir",
    "naître",
    "renaître",
    "partir",
    "repartir",
    "passer",
    "rester",
    "retourner",
    "sortir",
    "ressortir",
    "tomber",
    "retomber",
    "venir",
    "devenir",
    "parvenir",
    "revenir",
]

VERBS_THAT_CANNOT_BE_REFLEXIVE_OTHER_THAN_IMPERSONAL_VERBS = ["être", "aller", "avoir"]


class InflectorFr(Inflector):

    # public:

    def __init__(self) -> None:
        super(InflectorFr, self).__init__()

    @property
    def lang(self) -> LangCodeISO639_1:
        return LangCodeISO639_1.fr

    def get_verbs_that_start_with(self, query: str, max_results: int) -> List[str]:
        query = query.lower()
        is_reflexive, query = self.split_reflexive(query)
        matches = self._verb_parser.get_verbs_that_start_with(query, max_results)
        if is_reflexive:
            matches = [
                self.add_reflexive_pronoun(m)
                for m in matches
                if self.verb_can_be_reflexive(m)
            ]
        return matches

    def verb_can_be_reflexive(self, infinitive: str) -> bool:
        return (
            not self._is_impersonal_verb(infinitive)
            and infinitive
            not in VERBS_THAT_CANNOT_BE_REFLEXIVE_OTHER_THAN_IMPERSONAL_VERBS
        )

    def split_reflexive(self, infinitive: str) -> Tuple[bool, str]:
        """
        "se raser" => (True, "raser")
        "s'habiller" => (True, "habiller")
        "parler" => (False, "parler")
        """
        is_reflexive = False
        if infinitive.startswith("se "):
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
            return "se " + s

    def add_subjunctive_relative_pronoun(self, s: str, tense: Tense) -> str:
        if string_utils.starts_with_vowel(s, h_is_vowel=True):
            return "qu'" + s
        else:
            return "que " + s

    def get_default_pronoun(
        self,
        person: Person,
        gender: Gender = Gender.m,
        is_reflexive: bool = False,
        lang_specific_options: LangSpecificOptions = None,
    ) -> str:
        ret = ""
        if person == Person.FirstPersonSingular:
            ret = "je"
            if is_reflexive:
                ret += " me"
        elif person == Person.SecondPersonSingular:
            ret = "tu"
            if is_reflexive:
                ret += " te"
        elif person == Person.ThirdPersonSingular:
            ret = "il"
            if gender == Gender.f:
                ret = "elle"
            if is_reflexive:
                ret += " se"
        elif person == Person.FirstPersonPlural:
            ret = "nous"
            if is_reflexive:
                ret += " nous"
        elif person == Person.SecondPersonPlural:
            ret = "vous"
            if is_reflexive:
                ret += " vous"
        elif person == Person.ThirdPersonPlural:
            ret = "ils"
            if gender == Gender.f:
                ret = "elles"
            if is_reflexive:
                ret += " se"
        return ret

    def get_tenses_conjugated_without_pronouns(self) -> List[Tense]:
        return [
            Tense.InfinitifPrésent,
            Tense.ParticipePresent,
            Tense.ImperatifPrésent,
            Tense.ParticipePassé,
        ]

    def get_auxilary_verb(
        self,
        co: ConjugationObjects,
        mood: Mood,
        tense: Tense,
    ) -> str:
        ret = "avoir"
        if co.verb.infinitive in VERBS_CONJUGATED_WITH_ETRE or co.is_reflexive:
            ret = "être"
        return ret

    def is_auxilary_verb_inflected(self, auxilary_verb: str) -> bool:
        return auxilary_verb == "être"

    def get_infinitive_mood(self) -> Mood:
        return Mood.Infinitif

    def get_indicative_mood(self) -> Mood:
        return Mood.Indicatif

    def get_subjunctive_mood(self) -> Mood:
        return Mood.Subjonctif

    def get_conditional_mood(self) -> Mood:
        return Mood.Conditionnel

    def get_participle_mood(self) -> Mood:
        return Mood.Participe

    def get_participle_tense(self) -> Tense:
        return Tense.ParticipePassé

    def combine_pronoun_and_conj(self, pronoun: str, conj: str) -> str:
        ret = ""
        if pronoun[-1] == "e" and string_utils.starts_with_vowel(conj, h_is_vowel=True):
            ret += pronoun[:-1] + "'"
        else:
            ret += pronoun + " "
        ret += conj
        return ret

    def add_present_participle_if_applicable(
        self, s: str, is_reflexive: bool, tense: Tense
    ) -> str:
        ret = s
        if is_reflexive and tense == self.get_participle_tense():
            ret += "étant "
        return ret

    def add_reflexive_pronoun_or_pronoun_suffix_if_applicable(
        self,
        s: str,
        is_reflexive: bool,
        mood: Mood,
        tense: Tense,
        person: Person,
    ) -> str:
        if is_reflexive:
            if mood != Mood.Imperatif:
                s = self.add_reflexive_pronoun(s)
            else:
                s += self._get_pronoun_suffix(person)
        return s

    def compound_conjugation_not_applicable(
        self, is_reflexive: bool, mood: Mood, hv_tense_name: Tense
    ) -> bool:
        return (
            is_reflexive
            and mood == Mood.Imperatif
            and hv_tense_name == Tense.ImperatifPrésent
        )

    def get_compound_conjugations_aux_verb_map(
        self,
    ) -> Dict[Mood, Dict[Tense, Tuple[Mood, Tense]]]:
        """
        compound conjugations are formed using an auxiliary
        verb (aka helping verb)
        this method returns a Dictionary mapping of
        [compound-mood][compound-tense] to (aux-verb-mood, aux-verb-tense)
        """
        return {
            Mood.Indicatif: {
                Tense.PasséCompose: (Mood.Indicatif, Tense.Présent),
                Tense.PlusQueParfait: (Mood.Indicatif, Tense.Imparfait),
                Tense.FutureAntériuer: (Mood.Indicatif, Tense.FuturSimple),
                Tense.PasséAntérieur: (Mood.Indicatif, Tense.PasséSimple),
            },
            Mood.Subjonctif: {
                Tense.Passé: (Mood.Subjonctif, Tense.Présent),
                Tense.PlusQueParfait: (Mood.Subjonctif, Tense.Imparfait),
            },
            Mood.Conditionnel: {Tense.Passé: (Mood.Conditionnel, Tense.Présent)},
            Mood.Imperatif: {
                Tense.ImperatifPassé: (Mood.Imperatif, Tense.ImperatifPrésent)
            },
        }

    # private:

    def _get_pronoun_suffix(self, person: Person, gender: Gender = Gender.m) -> str:
        return "-" + self.get_default_pronoun(person, gender).replace("tu", "toi")

    def _is_impersonal_verb(self, infinitive: str) -> bool:
        ret = False
        verb = self.find_verb_by_infinitive(infinitive)
        template = self.find_template(verb.template)
        if len(
            template.mood_templates[Mood.Indicatif]
            .tense_templates[Tense.Présent]
            .person_endings
        ) < len(PERSONS):
            ret = True
        return ret
