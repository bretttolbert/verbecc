from typing import Dict, List, Tuple

from verbecc.src.inflectors.inflector import Inflector
from verbecc.src.utils import string_utils
from verbecc.src.conjugator.conjugation_object import ConjugationObjects

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
    @property
    def lang(self) -> str:
        return "fr"

    def __init__(self):
        super(InflectorFr, self).__init__()

    def get_verbs_that_start_with(self, query: str, max_results: int) -> List[str]:
        query = query.lower()
        is_reflexive, query = self._split_reflexive(query)
        matches = self._verb_parser.get_verbs_that_start_with(query, max_results)
        if is_reflexive:
            matches = [
                self._add_reflexive_pronoun(m)
                for m in matches
                if self._verb_can_be_reflexive(m)
            ]
        return matches

    def _is_impersonal_verb(self, infinitive: str) -> bool:
        ret = False
        verb = self.find_verb_by_infinitive(infinitive)
        template = self.find_template(verb.template)
        if len(template.moods["indicatif"].tenses["présent"].person_endings) < 6:
            ret = True
        return ret

    def _verb_can_be_reflexive(self, infinitive: str) -> bool:
        return (
            not self._is_impersonal_verb(infinitive)
            and infinitive
            not in VERBS_THAT_CANNOT_BE_REFLEXIVE_OTHER_THAN_IMPERSONAL_VERBS
        )

    def _split_reflexive(self, infinitive: str) -> Tuple[bool, str]:
        is_reflexive = False
        if infinitive.startswith("se "):
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
            return "se " + s

    def _add_subjunctive_relative_pronoun(self, s: str, tense_name: str) -> str:
        if string_utils.starts_with_vowel(s, h_is_vowel=True):
            return "qu'" + s
        else:
            return "que " + s

    def _get_pronoun_suffix(self, person: str, gender: str = "m") -> str:
        return "-" + self._get_default_pronoun(person, gender).replace("tu", "toi")

    def _get_default_pronoun(
        self, person: str, gender: str = "m", is_reflexive: bool = False
    ) -> str:
        ret = ""
        if person == "1s":
            ret = "je"
            if is_reflexive:
                ret += " me"
        elif person == "2s":
            ret = "tu"
            if is_reflexive:
                ret += " te"
        elif person == "3s":
            ret = "il"
            if gender == "f":
                ret = "elle"
            if is_reflexive:
                ret += " se"
        elif person == "1p":
            ret = "nous"
            if is_reflexive:
                ret += " nous"
        elif person == "2p":
            ret = "vous"
            if is_reflexive:
                ret += " vous"
        elif person == "3p":
            ret = "ils"
            if gender == "f":
                ret = "elles"
            if is_reflexive:
                ret += " se"
        return ret

    def _get_tenses_conjugated_without_pronouns(self) -> List[str]:
        return [
            "infinitif-présent",
            "participe-présent",
            "imperatif-présent",
            "participe-passé",
        ]

    def _get_auxilary_verb(
        self,
        co: ConjugationObjects,
        mood_name: str,
        tense_name: str,
    ) -> str:
        ret = "avoir"
        if co.verb.infinitive in VERBS_CONJUGATED_WITH_ETRE or co.is_reflexive:
            ret = "être"
        return ret

    def _is_auxilary_verb_inflected(self, auxilary_verb: str) -> bool:
        return auxilary_verb == "être"

    def _get_infinitive_mood_name(self) -> str:
        return "infinitif"

    def _get_indicative_mood_name(self) -> str:
        return "indicatif"

    def _get_subjunctive_mood_name(self) -> str:
        return "subjonctif"

    def _get_conditional_mood_name(self) -> str:
        return "conditionnel"

    def _get_participle_mood_name(self) -> str:
        return "participe"

    def _get_participle_tense_name(self) -> str:
        return "participe-passé"

    def _combine_pronoun_and_conj(self, pronoun: str, conj: str) -> str:
        ret = ""
        if pronoun[-1] == "e" and string_utils.starts_with_vowel(conj, h_is_vowel=True):
            ret += pronoun[:-1] + "'"
        else:
            ret += pronoun + " "
        ret += conj
        return ret

    def _add_present_participle_if_applicable(
        self, s: str, is_reflexive: bool, tense_name: str
    ) -> str:
        ret = s
        if is_reflexive and tense_name == self._get_participle_tense_name():
            ret += "étant "
        return ret

    def _add_reflexive_pronoun_or_pronoun_suffix_if_applicable(
        self, s: str, is_reflexive: bool, mood_name: str, tense_name: str, person: str
    ) -> str:
        if is_reflexive:
            if mood_name != "imperatif":
                s = self._add_reflexive_pronoun(s)
            else:
                s += self._get_pronoun_suffix(person)
        return s

    def _compound_conjugation_not_applicable(
        self, is_reflexive, mood_name, hv_tense_name
    ) -> bool:
        return (
            is_reflexive
            and mood_name == "imperatif"
            and hv_tense_name == "imperatif-présent"
        )

    def _get_compound_conjugations_aux_verb_map(
        self,
    ) -> Dict[str, Dict[str, Tuple[str, ...]]]:
        """
        compound conjugations are formed using an auxiliary
        verb (aka helping verb)
        this method returns a Dictionary mapping of
        [compound-mood][compound-tense] to (aux-verb-mood, aux-verb-tense)
        """
        return {
            "indicatif": {
                "passé-composé": ("indicatif", "présent"),
                "plus-que-parfait": ("indicatif", "imparfait"),
                "futur-antérieur": ("indicatif", "futur-simple"),
                "passé-antérieur": ("indicatif", "passé-simple"),
            },
            "subjonctif": {
                "passé": ("subjonctif", "présent"),
                "plus-que-parfait": ("subjonctif", "imparfait"),
            },
            "conditionnel": {"passé": ("conditionnel", "présent")},
            "imperatif": {"imperatif-passé": ("imperatif", "imperatif-présent")},
        }
