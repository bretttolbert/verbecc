from typing import Dict, List, Tuple

from verbecc.src.inflectors.inflector import Inflector
from verbecc.src.conjugator.conjugation_object import ConjugationObjects


class InflectorRo(Inflector):
    @property
    def lang(self) -> str:
        return "ro"

    def __init__(self):
        super(InflectorRo, self).__init__()

    def _add_subjunctive_relative_pronoun(self, s, tense_name):
        tokens = s.split(" ")
        if tense_name == "prezent":
            tokens.insert(1, "să")
        elif tense_name == "perfect":
            tokens.insert(1, "să fi")
        return " ".join(tokens)

    def _add_adverb_if_applicable(self, s, mood_name, tense_name):
        if mood_name == "imperativ" and tense_name == "negativ":
            return "nu " + s
        return s

    """TODO: There are two types of reflexive verbs in Romanian: 
    preceded by the reflexive pronouns “se” (in the accusative) and “și” (in the dative).
    """

    def _get_default_pronoun(self, person, gender="m", is_reflexive=False):
        ret = ""
        if person == "1s":
            ret = "eu"
            if is_reflexive:
                ret += " mă"
        elif person == "2s":
            ret = "tu"
            if is_reflexive:
                ret += " te"
        elif person == "3s":
            ret = "el"
            if gender == "f":
                ret = "ea"
            if is_reflexive:
                ret += " se"
        elif person == "1p":
            ret = "noi"
            if is_reflexive:
                ret += " ne"
        elif person == "2p":
            ret = "voi"
            if is_reflexive:
                ret += " vă"
        elif person == "3p":
            ret = "ei"
            if gender == "f":
                ret = "ele"
            if is_reflexive:
                ret += " se"
        return ret

    def _get_tenses_conjugated_without_pronouns(self):
        return ["participiu", "afirmativ", "imperativ", "negativ", "gerunziu"]

    def _get_auxilary_verb(self, co, mood_name, tense_name):
        if tense_name in ("viitor-1", "viitor-2"):
            return "voi"
        elif tense_name == "viitor-1-popular":
            return co.verb.infinitive
        return "avea"

    def _get_infinitive_mood_name(self):
        return "infinitiv"

    def _get_indicative_mood_name(self):
        return "indicativ"

    def _get_subjunctive_mood_name(self):
        return "conjunctiv"

    def _get_conditional_mood_name(self):
        return "conditional"

    def _get_participle_mood_name(self):
        return "participiu"

    def _get_participle_tense_name(self):
        return "participiu"

    def _get_compound_conjugations_aux_verb_map(
        self,
    ) -> Dict[str, Dict[str, Tuple[str, ...]]]:
        # TODO: those last three don't actually use an auxiliary verb, refactor to make aux verb optional
        return {
            "indicativ": {
                "perfect-compus": ("indicativ", "prezent"),
                "viitor-1": ("indicativ", "prezent"),
                "viitor-2": ("indicativ", "prezent"),
                "viitor-1-popular": ("conjunctiv", "prezent"),
                "viitor-2-popular": ("indicativ", "prezent"),
            },
            "conjunctiv": {"perfect": ("indicativ", "prezent")},
            "conditional": {
                "prezent": ("indicativ", "prezent"),
                "perfect": ("indicativ", "prezent"),
            },
        }

    def _auxilary_verb_uses_alternate_conjugation(self, tense_name) -> bool:
        return tense_name.startswith("viitor")

    def _compound_primary_verb_conjugation_uses_infinitive(
        self, mood_name: str, tense_name: str
    ):
        if mood_name == "indicativ" and tense_name == "viitor-1":
            return True
        elif mood_name == "conditional" and tense_name == "prezent":
            return True
        return False

    def _modify_aux_verb_conj_if_applicable(
        self, aux_conj: List[str], mood_name: str, tense_name: str
    ):
        """E.g. for Romanian conditional present 'eu aş avea, tu ai avea, el ar avea, ...'
        and also the Romanian conditional present e.g. 'eu	aş fi avut, tu ai fi avut, ...'
        although the ' fi' is added by _add_compound_aux_verb_suffix_if_applicable

        Normally Romanian aux_conj would be the indicativ prezent tense of avea i.e.
            ["eu am", "tu ai", "el a", "noi am", "voi aţi", "ei au"]
        but for conditional it's supposed to be
            ["eu aş", "tu ai", "el ar", "noi am", "voi aţi", "ei ar"]
        """
        if mood_name == "conditional" and tense_name in ("prezent", "perfect"):
            sub_aux_conj = ["aş", "ai", "ar", "am", "aţi", "ar"]
            for i, c in enumerate(aux_conj):
                pronoun, _ = c.split(" ")
                aux_conj[i] = f"{pronoun} {sub_aux_conj[i]}"
        return aux_conj

    def _add_compound_aux_verb_suffix_if_applicable(
        self, s: str, mood_name: str, tense_name: str
    ) -> str:
        """
        E.g. for Romanian indicativ viitor-ii this appends " fi" to make "eu am să fi avut" etc.
        """
        if (mood_name == "indicativ" and tense_name == "viitor-2") or (
            mood_name == "conditional" and tense_name == "perfect"
        ):
            return s + " fi"
        elif mood_name == "indicativ" and tense_name == "viitor-2-popular":
            return s + " să fi"
        # TODO: Research. Some sources e.g. verbix.com don't include " să"
        # elif mood_name == "indicativ" and tense_name == "viitor-1":
        #    return s + " să"
        return s

    def _insert_compound_aux_verb_prefix_if_applicable(
        self, s: str, mood_name: str, tense_name: str
    ) -> str:
        """
        Used by Romanian viitor-1-popular
        "eu o să fac, tu o să faci, ..."
        """
        if mood_name == "indicativ" and tense_name == "viitor-1-popular":
            tokens = s.split()
            return tokens[0] + " o să " + tokens[1]
        return s

    def _compound_has_no_primary_verb(self, mood_name: str, tense_name: str) -> bool:
        """Used for Romanian viitor-1-popular"""
        if mood_name == "indicativ" and tense_name == "viitor-1-popular":
            return True
        return False

    def _compound_has_no_aux_verb(self, mood_name: str, tense_name: str) -> bool:
        """Used for Romanian conjunctiv perfect"""
        if mood_name == "conjunctiv" and tense_name == "perfect":
            return True
        return False
