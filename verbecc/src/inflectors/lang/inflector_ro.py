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

    def get_lang(self) -> LangCodeISO639_1:
        return LangCodeISO639_1.ro

    def add_subjunctive_relative_pronoun(self, s: str, tense: Tense) -> str:
        """
        :param s: a conjugation, perhaps with a pronoun e.g. "eu fac"
        :tense s: the verb tense
            New behavior: If this is a compound conjugation, tense is the tense
            of the primary verb, not the auxiliary.

        Note: Updated to handle Viitor1popular but may revisit this change.
        (with compound tense Viitor1popular the aux tense is Prezent)

        In the case of Viitor1popular, this function inserts "să" and then
        insert_compound_aux_verb_prefix_if_applicable replaced it with " o să "
        """
        tokens = s.split(" ")
        if tense == Tenses.ro.Prezent or tense == Tenses.ro.Viitor1Popular:
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

    def get_pronoun_gender(self, pronoun: str) -> Optional[Gender]:
        if pronoun in ("ea", "ele"):
            return Gender.f
        elif pronoun in ("el", "ei"):
            return Gender.m
        return None

    def get_pronouns(
        self,
        person: Optional[Person] = None,
        number: Optional[Number] = None,
        gender: Optional[Gender] = None,
    ) -> List[str]:
        ret = []
        if (person is None or person == Person.First) and (
            number is None or number == Number.Singular
        ):
            p = "eu"
            ret.append(p)
        if (person is None or person == Person.Second) and (
            number is None or number == Number.Singular
        ):
            p = "tu"
            ret.append(p)
        if (person is None or person == Person.Third) and (
            number is None or number == Number.Singular
        ):
            pronouns = ["el", "ea"]
            if gender is not None:
                if gender is Gender.m:
                    pronouns = ["el"]
                else:
                    pronouns = ["ea"]
            ret.extend(pronouns)
        if (person is None or person == Person.First) and (
            number is None or number == Number.Plural
        ):
            p = "noi"
            ret.append(p)
        if (person is None or person == Person.Second) and (
            number is None or number == Number.Plural
        ):
            p = "voi"
            ret.append(p)
        if (person is None or person == Person.Third) and (
            number is None or number == Number.Plural
        ):
            pronouns = ["ei", "ele"]
            if gender is not None:
                if gender is Gender.m:
                    pronouns = ["ei"]
                else:
                    pronouns = ["ele"]
            ret.extend(pronouns)
        return ret

    def make_pronoun_reflexive(self, pronoun: str) -> str:
        if pronoun == "eu":
            return pronoun + " mă"
        elif pronoun == "tu":
            return pronoun + " te"
        elif pronoun == "voi":
            return pronoun + " vă"
        elif pronoun == "noi":
            return pronoun + " ne"
        else:
            return pronoun + " se"

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
        """
        TODO: those last three don't actually use an auxiliary verb,
        refactor to make aux verb optional

        The Romanian conjunctive perfect tense is formed by using the particle "să"
        followed by the auxiliary verb "fi" and the past participle of the main verb.

        See Inflector.compound_has_no_aux_verb()
        """
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
            ["eu am", "tu ai", "el a", "ea a", "noi am", "voi aţi", "ei au", "ele au"]
        but for conditional it's supposed to be
            ["eu aş", "tu ai", "el ar", "ea ar", "noi am", "voi aţi", "ei ar", "ele ar"]
        """
        if mood == Moods.ro.Condițional and tense in (Tenses.ro.Prezent, "perfect"):
            sub_aux_conj = ["aş", "ai", "ar", "ar", "am", "aţi", "ar", "ar"]
            for i, c in enumerate(aux_conj):
                pronoun, _ = c.split(" ")
                aux_conj[i] = f"{pronoun} {sub_aux_conj[i]}"
        return aux_conj

    def add_compound_aux_verb_suffix_if_applicable(
        self, s: str, mood: Mood, tense: Tense
    ) -> str:
        """
        E.g. for Romanian indicativ viitor-ii this appends " fi" to make "eu am să fi avut" etc.

        See also Inflector.insert_compound_aux_verb_prefix_if_applicable()
        which is used for adding "să fi" for Conjunctiv Perfect,
        e.g. to form "eu să fi făcut".

        The Romanian conjunctive perfect tense is formed by using the particle "să"
        followed by the auxiliary verb "fi" and the past participle of the main verb.
        """
        if (mood == Moods.ro.Indicativ and tense == Tenses.ro.Viitor2) or (
            mood == Moods.ro.Condițional and tense == Tenses.ro.Perfect
        ):
            return s + " fi"
        elif mood == Moods.ro.Indicativ and tense == Tenses.ro.Viitor2Popular:
            return s + " să fi"
        # elif mood == Moods.ro.Conjunctiv and tense == Tenses.ro.Perfect:
        #    # How was it working before without this?
        #    return "să fi " + s
        # TODO: Research. Some sources e.g. verbix.com don't include " să"
        # elif mood == Moods.ro.Indicativ and tense == "viitor-1":
        #    return s + " să"
        return s

    def insert_compound_aux_verb_prefix_if_applicable(
        self, s: str, mood: Mood, tense: Tense
    ) -> str:
        """
        Used for viitor-1-popular for inserting " o să "
        e.g. "eu o să fac, tu o să faci, ..."

        Used for Conjunctiv Perfect for inserting " să fi "
        e.g. to form "eu să fi făcut".

            The Romanian conjunctive perfect tense is formed by using the particle "să"
            followed by the auxiliary verb "fi" and the past participle of the main verb.

        """
        if mood == Moods.ro.Indicativ and tense == Tenses.ro.Viitor1Popular:
            return s.replace(" să ", " o să ")
        elif mood == Moods.ro.Conjunctiv and tense == Tenses.ro.Perfect:
            tokens = s.split()
            return tokens[0] + " să fi " + tokens[1]
        return s

    def compound_has_no_primary_verb(self, mood: Mood, tense: Tense) -> bool:
        """Used for Romanian viitor-1-popular"""
        if mood == Moods.ro.Indicativ and tense == Tenses.ro.Viitor1Popular:
            return True
        return False

    def compound_has_no_aux_verb(self, mood: Mood, tense: Tense) -> bool:
        """Used for Romanian Conjunctiv Perfect

        The Romanian conjunctive perfect tense is formed by using the particle "să"
        followed by the auxiliary verb "fi" and the past participle of the main verb.

        But for the purposes of this function, we consider that it has no aux verb,
        since "fi" is constant and not actually conjugated.
        """
        if mood == Moods.ro.Conjunctiv and tense == Tenses.ro.Perfect:
            return True
        return False
