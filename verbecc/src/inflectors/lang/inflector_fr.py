from typing import Dict, List, Optional, Tuple

from verbecc.src.conjugator.conjugation_object import ConjugationObjects
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.lang_code import LangCodeISO639_1
from verbecc.src.defs.types.mood import Mood, Moods
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.number import Number
from verbecc.src.defs.constants.grammar_defines import PERSONS
from verbecc.src.defs.types.tense import Tense, Tenses
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

    def __init__(
        self, lang_specific_options: Optional[LangSpecificOptions] = None
    ) -> None:
        super(InflectorFr, self).__init__()

    @property
    def lang(self) -> LangCodeISO639_1:
        return LangCodeISO639_1.fr

    def get_verbs_that_start_with(self, query: str, max_results: int) -> List[str]:
        query = query.lower()
        is_reflexive, query = self.split_reflexive(query)
        matches = self._verbs.get_verbs_that_start_with(query, max_results)
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

    def get_pronoun_gender(self, pronoun: str) -> Optional[Gender]:
        if pronoun in ("elle", "elles"):
            return Gender.f
        elif pronoun in ("il", "ils"):
            return Gender.m
        return None

    def get_pronouns(
        self,
        person: Optional[Person] = None,
        number: Optional[Number] = None,
        gender: Optional[Gender] = None,
    ) -> List[str]:
        """
        Returns a list of all pronouns matching the provided filters,
        in the typical order, with the default pronoun first.
        E.g. Person.Second, Number.Singular => ["tú", "vos"]
        """
        ret = []
        if (person is None or person == Person.First) and (
            number is None or number == Number.Singular
        ):
            p = "je"
            ret.append(p)
        if (person is None or person == Person.Second) and (
            number is None or number == Number.Singular
        ):
            p = "tu"
            ret.append(p)
        if (person is None or person == Person.Third) and (
            number is None or number == Number.Singular
        ):
            pronouns = ["il", "elle", "on"]
            if gender is not None:
                if gender == Gender.m:
                    pronouns = ["il"]
                else:
                    pronouns = ["elle"]
            ret.extend(pronouns)
        if (person is None or person == Person.First) and (
            number is None or number == Number.Plural
        ):
            p = "nous"
            ret.append(p)
        if (person is None or person == Person.Second) and (
            number is None or number == Number.Plural
        ):
            p = "vous"
            ret.append(p)
        if (person is None or person == Person.Third) and (
            number is None or number == Number.Plural
        ):
            pronouns = ["ils", "elles"]
            if gender is not None:
                if gender == Gender.m:
                    pronouns = ["ils"]
                else:
                    pronouns = ["elles"]
            ret.extend(pronouns)
        return ret

    def make_pronoun_reflexive(self, pronoun: str) -> str:
        if pronoun == "je":
            return pronoun + " me"
        elif pronoun == "tu":
            return pronoun + " te"
        elif pronoun == "vous":
            return pronoun + " vous"
        elif pronoun == "nous":
            return pronoun + " nous"
        else:
            return pronoun + " se"

    def get_tenses_conjugated_without_pronouns(self) -> List[Tense]:
        return [
            Tenses.fr.InfinitifPrésent,
            Tenses.fr.ParticipePresent,
            Tenses.fr.ImperatifPrésent,
            Tenses.fr.ImperatifPassé,
            Tenses.fr.ParticipePassé,
        ]

    def get_auxiliary_verb(
        self,
        co: ConjugationObjects,
        mood: Mood,
        tense: Tense,
    ) -> str:
        ret = "avoir"
        if co.verb.infinitive in VERBS_CONJUGATED_WITH_ETRE or co.is_reflexive:
            ret = "être"
        return ret

    def is_auxiliary_verb_inflected(self, auxiliary_verb: str) -> bool:
        return auxiliary_verb == "être"

    def get_infinitive_mood(self) -> Mood:
        return Moods.fr.Infinitif

    def get_indicative_mood(self) -> Mood:
        return Moods.fr.Indicatif

    def get_subjunctive_mood(self) -> Mood:
        return Moods.fr.Subjonctif

    def get_conditional_mood(self) -> Mood:
        return Moods.fr.Conditionnel

    def get_participle_mood(self) -> Mood:
        return Moods.fr.Participe

    def get_participle_tense(self) -> Tense:
        return Tenses.fr.ParticipePassé

    def combine_pronoun_and_conj(self, pronoun: str, conj: str) -> str:
        ret = ""
        if pronoun == "je" and string_utils.starts_with_vowel(conj, h_is_vowel=True):
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
        number: Number,
    ) -> str:
        if is_reflexive:
            if mood != Moods.fr.Imperatif:
                s = self.add_reflexive_pronoun(s)
            else:
                s += self._get_pronoun_suffix(person, number)
        return s

    def compound_conjugation_not_applicable(
        self, is_reflexive: bool, mood: Mood, aux_tense: Tense
    ) -> bool:
        return (
            is_reflexive
            and mood == Moods.fr.Imperatif
            and aux_tense == Tenses.fr.ImperatifPrésent
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
            Moods.fr.Indicatif: {
                Tenses.fr.PasséCompose: (Moods.fr.Indicatif, Tenses.fr.Présent),
                Tenses.fr.PlusQueParfait: (Moods.fr.Indicatif, Tenses.fr.Imparfait),
                Tenses.fr.FutureAntériuer: (Moods.fr.Indicatif, Tenses.fr.FuturSimple),
                Tenses.fr.PasséAntérieur: (Moods.fr.Indicatif, Tenses.fr.PasséSimple),
            },
            Moods.fr.Subjonctif: {
                Tenses.fr.Passé: (Moods.fr.Subjonctif, Tenses.fr.Présent),
                Tenses.fr.PlusQueParfait: (Moods.fr.Subjonctif, Tenses.fr.Imparfait),
            },
            Moods.fr.Conditionnel: {
                Tenses.fr.Passé: (Moods.fr.Conditionnel, Tenses.fr.Présent)
            },
            Moods.fr.Imperatif: {
                Tenses.fr.ImperatifPassé: (
                    Moods.fr.Imperatif,
                    Tenses.fr.ImperatifPrésent,
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
        return "-" + self.get_pronouns(person, number, gender)[0].replace("tu", "toi")

    def _is_impersonal_verb(self, infinitive: str) -> bool:
        ret = False
        verb = self.find_verb_by_infinitive(infinitive)
        template = self.find_template(verb.template)
        if len(
            template.mood_templates[Moods.fr.Indicatif]
            .tense_templates[Tenses.fr.Présent]
            .person_endings
        ) < len(PERSONS):
            ret = True
        return ret
