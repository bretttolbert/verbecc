from typing import Dict, List, Tuple

from verbecc.src.conjugator.conjugation_object import ConjugationObjects
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.language_codes import LangCodeISO639_1
from verbecc.src.defs.types.mood import MoodRo as Mood
from verbecc.src.defs.types.tense import TenseRo as Tense
from verbecc.src.inflectors.inflector import Inflector


class InflectorRo(Inflector):
    @property
    def lang(self) -> LangCodeISO639_1:
        return LangCodeISO639_1.ro

    def __init__(self) -> None:
        super(InflectorRo, self).__init__()

    def _add_subjunctive_relative_pronoun(self, s: str, tense: Tense) -> str:
        tokens = s.split(" ")
        if tense == Tense.Prezent:
            tokens.insert(1, "să")
        elif tense == Tense.Perfect:
            tokens.insert(1, "să fi")
        return " ".join(tokens)

    def _add_adverb_if_applicable(self, s: str, mood: Mood, tense: Tense) -> str:
        if mood == Mood.Imperativ and tense == Tense.Negativ:
            return "nu " + s
        return s

    """TODO: There are two types of reflexive verbs in Romanian: 
    preceded by the reflexive pronouns “se” (in the accusative) and “și” (in the dative).
    """

    def _get_default_pronoun(
        self,
        person: Person,
        gender: Gender = Gender.m,
        is_reflexive: bool = False,
    ) -> str:
        ret = ""
        if person == Person.FirstPersonSingular:
            ret = "eu"
            if is_reflexive:
                ret += " mă"
        elif person == Person.SecondPersonSingular:
            ret = "tu"
            if is_reflexive:
                ret += " te"
        elif person == Person.ThirdPersonSingular:
            ret = "el"
            if gender == Gender.f:
                ret = "ea"
            if is_reflexive:
                ret += " se"
        elif person == Person.FirstPersonPlural:
            ret = "noi"
            if is_reflexive:
                ret += " ne"
        elif person == Person.SecondPersonPlural:
            ret = "voi"
            if is_reflexive:
                ret += " vă"
        elif person == Person.ThirdPersonPlural:
            ret = "ei"
            if gender == Gender.f:
                ret = "ele"
            if is_reflexive:
                ret += " se"
        return ret

    def _get_tenses_conjugated_without_pronouns(self) -> List[Tense]:
        return [
            Tense.Participiu,
            Tense.Afirmativ,
            Tense.Imperativ,
            Tense.Negativ,
            Tense.Gerunziu,
        ]

    def _get_auxilary_verb(
        self, co: ConjugationObjects, mood: Mood, tense: Tense
    ) -> str:
        if tense in (Tense.Viitor1, Tense.Viitor2):
            return "voi"
        elif tense == Tense.Viitor1Popular:
            return co.verb.infinitive
        return "avea"

    def _get_infinitive_mood(self) -> Mood:
        return Mood.Infinitiv

    def _get_indicative_mood(self) -> Mood:
        return Mood.Indicativ

    def _get_subjunctive_mood(self) -> Mood:
        return Mood.Conjunctiv

    def _get_conditional_mood(self) -> Mood:
        return Mood.Condițional

    def _get_participle_mood(self) -> Mood:
        return Mood.Participiu

    def _get_participle_tense(self) -> Tense:
        return Tense.Participiu

    def _get_compound_conjugations_aux_verb_map(
        self,
    ) -> Dict[Mood, Dict[Tense, Tuple[Mood, Tense]]]:
        # TODO: those last three don't actually use an auxiliary verb, refactor to make aux verb optional
        return {
            Mood.Indicativ: {
                Tense.PerfectCompus: (Mood.Indicativ, Tense.Prezent),
                Tense.Viitor1: (Mood.Indicativ, Tense.Prezent),
                Tense.Viitor2: (Mood.Indicativ, Tense.Prezent),
                Tense.Viitor1Popular: (Mood.Conjunctiv, Tense.Prezent),
                Tense.Viitor2Popular: (Mood.Indicativ, Tense.Prezent),
            },
            Mood.Conjunctiv: {Tense.Perfect: (Mood.Indicativ, Tense.Prezent)},
            Mood.Condițional: {
                Tense.Prezent: (Mood.Indicativ, Tense.Prezent),
                Tense.Perfect: (Mood.Indicativ, Tense.Prezent),
            },
        }

    def _auxilary_verb_uses_alternate_conjugation(self, tense: Tense) -> bool:
        return tense.startswith("viitor")

    def _compound_primary_verb_conjugation_uses_infinitive(
        self, mood: Mood, tense: Tense
    ) -> bool:
        if mood == Mood.Indicativ and tense == Tense.Viitor1:
            return True
        elif mood == Mood.Condițional and tense == Tense.Prezent:
            return True
        return False

    def _modify_aux_verb_conj_if_applicable(
        self, aux_conj: List[str], mood: Mood, tense: Tense
    ) -> List[str]:
        """E.g. for Romanian conditional present 'eu aş avea, tu ai avea, el ar avea, ...'
        and also the Romanian conditional present e.g. 'eu	aş fi avut, tu ai fi avut, ...'
        although the ' fi' is added by _add_compound_aux_verb_suffix_if_applicable

        Normally Romanian aux_conj would be the indicativ prezent tense of avea i.e.
            ["eu am", "tu ai", "el a", "noi am", "voi aţi", "ei au"]
        but for conditional it's supposed to be
            ["eu aş", "tu ai", "el ar", "noi am", "voi aţi", "ei ar"]
        """
        if mood == Mood.Condițional and tense in (Tense.Prezent, "perfect"):
            sub_aux_conj = ["aş", "ai", "ar", "am", "aţi", "ar"]
            for i, c in enumerate(aux_conj):
                pronoun, _ = c.split(" ")
                aux_conj[i] = f"{pronoun} {sub_aux_conj[i]}"
        return aux_conj

    def _add_compound_aux_verb_suffix_if_applicable(
        self, s: str, mood: Mood, tense: Tense
    ) -> str:
        """
        E.g. for Romanian indicativ viitor-ii this appends " fi" to make "eu am să fi avut" etc.
        """
        if (mood == Mood.Indicativ and tense == Tense.Viitor2) or (
            mood == Mood.Condițional and tense == Tense.Perfect
        ):
            return s + " fi"
        elif mood == Mood.Indicativ and tense == Tense.Viitor2Popular:
            return s + " să fi"
        # TODO: Research. Some sources e.g. verbix.com don't include " să"
        # elif mood == Mood.Indicativ and tense == "viitor-1":
        #    return s + " să"
        return s

    def _insert_compound_aux_verb_prefix_if_applicable(
        self, s: str, mood: Mood, tense: Tense
    ) -> str:
        """
        Used by Romanian viitor-1-popular
        "eu o să fac, tu o să faci, ..."
        """
        if mood == Mood.Indicativ and tense == Tense.Viitor1Popular:
            tokens = s.split()
            return tokens[0] + " o să " + tokens[1]
        return s

    def _compound_has_no_primary_verb(self, mood: Mood, tense: Tense) -> bool:
        """Used for Romanian viitor-1-popular"""
        if mood == Mood.Indicativ and tense == Tense.Viitor1Popular:
            return True
        return False

    def _compound_has_no_aux_verb(self, mood: Mood, tense: Tense) -> bool:
        """Used for Romanian conjunctiv perfect"""
        if mood == Mood.Conjunctiv and tense == Tense.Perfect:
            return True
        return False
