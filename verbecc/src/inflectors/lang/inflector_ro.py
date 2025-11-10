from typing import Dict, List, Optional, Tuple

from verbecc.src.conjugator.conjugation_object import ConjugationObjects
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.number import Number
from verbecc.src.defs.types.lang_code import LangCodeISO639_1
from verbecc.src.defs.types.mood import Mood, Moods
from verbecc.src.defs.types.tense import Tense, Tenses
from verbecc.src.defs.types.lang_specific_options import (
    LangSpecificOptions,
)
from verbecc.src.inflectors.inflector import Inflector


class InflectorRo(Inflector):
    def __init__(
        self, lang_specific_options: Optional[LangSpecificOptions] = None
    ) -> None:
        super(InflectorRo, self).__init__()

    @property
    def lang(self) -> LangCodeISO639_1:
        return LangCodeISO639_1.ro

    def add_subjunctive_relative_pronoun(self, s: str, tense: Tense) -> str:
        tokens = s.split(" ")
        if tense == Tenses.ro.Prezent:
            tokens.insert(1, "să")
        elif tense == Tenses.ro.Perfect:
            tokens.insert(1, "să fi")
        return " ".join(tokens)

    def add_adverb_if_applicable(self, s: str, mood: Mood, tense: Tense) -> str:
        if mood == Moods.ro.Imperativ and tense == Tenses.ro.Negativ:
            return "nu " + s
        return s

    """TODO: There are two types of reflexive verbs in Romanian: 
    preceded by the reflexive pronouns “se” (in the accusative) and “și” (in the dative).
    """

    def get_default_pronoun(
        self,
        person: Person,
        number: Number = Number.Singular,
        gender: Gender = Gender.m,
        is_reflexive: bool = False,
    ) -> str:
        ret = ""
        if person == Person.First and number == Number.Singular:
            ret = "eu"
            if is_reflexive:
                ret += " mă"
        elif person == Person.Second and number == Number.Singular:
            ret = "tu"
            if is_reflexive:
                ret += " te"
        elif person == Person.Third and number == Number.Singular:
            ret = "el"
            if gender == Gender.f:
                ret = "ea"
            if is_reflexive:
                ret += " se"
        elif person == Person.First and number == Number.Plural:
            ret = "noi"
            if is_reflexive:
                ret += " ne"
        elif person == Person.Second and number == Number.Plural:
            ret = "voi"
            if is_reflexive:
                ret += " vă"
        elif person == Person.Third and number == Number.Plural:
            ret = "ei"
            if gender == Gender.f:
                ret = "ele"
            if is_reflexive:
                ret += " se"
        return ret

    def get_tenses_conjugated_without_pronouns(self) -> List[Tense]:
        return [
            Tenses.ro.Participiu,
            Tenses.ro.Afirmativ,
            Tenses.ro.Imperativ,
            Tenses.ro.Negativ,
            Tenses.ro.Gerunziu,
        ]

    def get_auxiliary_verb(
        self, co: ConjugationObjects, mood: Mood, tense: Tense
    ) -> str:
        if tense in (Tenses.ro.Viitor1, Tenses.ro.Viitor2):
            return "voi"
        elif tense == Tenses.ro.Viitor1Popular:
            return co.verb.infinitive
        return "avea"

    def get_infinitive_mood(self) -> Mood:
        return Moods.ro.Infinitiv

    def get_indicative_mood(self) -> Mood:
        return Moods.ro.Indicativ

    def get_subjunctive_mood(self) -> Mood:
        return Moods.ro.Conjunctiv

    def get_conditional_mood(self) -> Mood:
        return Moods.ro.Condițional

    def get_participle_mood(self) -> Mood:
        return Moods.ro.Participiu

    def get_participle_tense(self) -> Tense:
        return Tenses.ro.Participiu

    def get_compound_conjugations_aux_verb_map(
        self,
    ) -> Dict[Mood, Dict[Tense, Tuple[Mood, Tense]]]:
        # TODO: those last three don't actually use an auxiliary verb, refactor to make aux verb optional
        return {
            Moods.ro.Indicativ: {
                Tenses.ro.PerfectCompus: (Moods.ro.Indicativ, Tenses.ro.Prezent),
                Tenses.ro.Viitor1: (Moods.ro.Indicativ, Tenses.ro.Prezent),
                Tenses.ro.Viitor2: (Moods.ro.Indicativ, Tenses.ro.Prezent),
                Tenses.ro.Viitor1Popular: (Moods.ro.Conjunctiv, Tenses.ro.Prezent),
                Tenses.ro.Viitor2Popular: (Moods.ro.Indicativ, Tenses.ro.Prezent),
            },
            Moods.ro.Conjunctiv: {
                Tenses.ro.Perfect: (Moods.ro.Indicativ, Tenses.ro.Prezent)
            },
            Moods.ro.Condițional: {
                Tenses.ro.Prezent: (Moods.ro.Indicativ, Tenses.ro.Prezent),
                Tenses.ro.Perfect: (Moods.ro.Indicativ, Tenses.ro.Prezent),
            },
        }

    def auxiliary_verb_uses_alternate_conjugation(self, tense: Tense) -> bool:
        return tense.startswith("viitor")

    def compound_primary_verb_conjugation_uses_infinitive(
        self, mood: Mood, tense: Tense
    ) -> bool:
        if mood == Moods.ro.Indicativ and tense == Tenses.ro.Viitor1:
            return True
        elif mood == Moods.ro.Condițional and tense == Tenses.ro.Prezent:
            return True
        return False

    def modify_aux_verb_conj_if_applicable(
        self, aux_conj: List[str], mood: Mood, tense: Tense
    ) -> List[str]:
        """E.g. for Romanian conditional present 'eu aş avea, tu ai avea, el ar avea, ...'
        and also the Romanian conditional present e.g. 'eu	aş fi avut, tu ai fi avut, ...'
        although the ' fi' is added by add_compound_aux_verb_suffix_if_applicable

        Normally Romanian aux_conj would be the indicativ prezent tense of avea i.e.
            ["eu am", "tu ai", "el a", "noi am", "voi aţi", "ei au"]
        but for conditional it's supposed to be
            ["eu aş", "tu ai", "el ar", "noi am", "voi aţi", "ei ar"]
        """
        if mood == Moods.ro.Condițional and tense in (Tenses.ro.Prezent, "perfect"):
            sub_aux_conj = ["aş", "ai", "ar", "am", "aţi", "ar"]
            for i, c in enumerate(aux_conj):
                pronoun, _ = c.split(" ")
                aux_conj[i] = f"{pronoun} {sub_aux_conj[i]}"
        return aux_conj

    def add_compound_aux_verb_suffix_if_applicable(
        self, s: str, mood: Mood, tense: Tense
    ) -> str:
        """
        E.g. for Romanian indicativ viitor-ii this appends " fi" to make "eu am să fi avut" etc.
        """
        if (mood == Moods.ro.Indicativ and tense == Tenses.ro.Viitor2) or (
            mood == Moods.ro.Condițional and tense == Tenses.ro.Perfect
        ):
            return s + " fi"
        elif mood == Moods.ro.Indicativ and tense == Tenses.ro.Viitor2Popular:
            return s + " să fi"
        # TODO: Research. Some sources e.g. verbix.com don't include " să"
        # elif mood == Moods.ro.Indicativ and tense == "viitor-1":
        #    return s + " să"
        return s

    def insert_compound_aux_verb_prefix_if_applicable(
        self, s: str, mood: Mood, tense: Tense
    ) -> str:
        """
        Used by Romanian viitor-1-popular
        "eu o să fac, tu o să faci, ..."
        """
        if mood == Moods.ro.Indicativ and tense == Tenses.ro.Viitor1Popular:
            tokens = s.split()
            return tokens[0] + " o să " + tokens[1]
        return s

    def compound_has_no_primary_verb(self, mood: Mood, tense: Tense) -> bool:
        """Used for Romanian viitor-1-popular"""
        if mood == Moods.ro.Indicativ and tense == Tenses.ro.Viitor1Popular:
            return True
        return False

    def compound_has_no_aux_verb(self, mood: Mood, tense: Tense) -> bool:
        """Used for Romanian conjunctiv perfect"""
        if mood == Moods.ro.Conjunctiv and tense == Tenses.ro.Perfect:
            return True
        return False
