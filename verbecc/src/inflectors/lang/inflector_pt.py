from typing import Dict, List, Tuple

from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.person import Person
from verbecc.src.inflectors.inflector import Inflector
from verbecc.src.conjugator.conjugation_object import ConjugationObjects


class InflectorPt(Inflector):
    @property
    def lang(self) -> str:
        return "pt"

    def __init__(self):
        super(InflectorPt, self).__init__()

    def _add_subjunctive_relative_pronoun(self, s: str, tense_name: str):
        if tense_name == "presente":
            return "que " + s
        elif tense_name == "pretérito-imperfeito":
            return "se " + s
        elif tense_name == "futuro":
            return "quando " + s
        return s

    def _add_adverb_if_applicable(self, s: str, mood_name: str, tense_name: str):
        if mood_name == "imperativo" and tense_name == "negativo":
            return "não " + s
        elif mood_name == "infinitivo" and tense_name == "infinitivo-pessoal-presente":
            return "por " + s
        return s

    def _add_reflexive_pronoun_or_pronoun_suffix_if_applicable(
        self,
        s: str,
        is_reflexive: bool,
        mood_name: str,
        tense_name: str,
        person: Person,
    ):
        imperative = mood_name == "imperativo"
        if imperative or (
            mood_name == "infinitivo" and tense_name == "infinitivo-pessoal-presente"
        ):
            s += " " + self._get_pronoun_suffix(person, imperative=imperative)
        return s

    def _get_default_pronoun(
        self, person: Person, gender: Gender = Gender.Masculine, is_reflexive=False
    ):
        ret = ""
        if person == Person.FirstPersonSingular:
            ret = "eu"
            if is_reflexive:
                ret += " me"
        elif person == Person.SecondPersonSingular:
            ret = "tu"
            if is_reflexive:
                ret += " te"
        elif person == Person.ThirdPersonSingular:
            ret = "ele"
            if gender == Gender.Feminine:
                ret = "ela"
            if is_reflexive:
                ret += " se"
        elif person == Person.FirstPersonPlural:
            ret = "nós"
            if is_reflexive:
                ret += " nos"
        elif person == Person.SecondPersonPlural:
            ret = "vós"
            if is_reflexive:
                ret += " se"
        elif person == Person.ThirdPersonPlural:
            ret = "eles"
            if gender == Gender.Feminine:
                ret = "elas"
            if is_reflexive:
                ret += " se"
        return ret

    def _get_pronoun_suffix(
        self, person: Person, gender: Gender = Gender.Masculine, imperative=True
    ):
        ret = ""
        if person == Person.FirstPersonSingular:
            ret = "eu"
        if person == Person.SecondPersonSingular:
            ret = "tu"
        elif person == Person.ThirdPersonSingular:
            ret = "você"
            if not imperative:
                ret = "ele"
        elif person == Person.FirstPersonPlural:
            ret = "nós"
        elif person == Person.SecondPersonPlural:
            ret = "vós"
        elif person == Person.ThirdPersonPlural:
            ret = "vocês"
            if not imperative:
                ret = "eles"
        return ret

    def _get_tenses_conjugated_without_pronouns(self) -> List[str]:
        return [
            "particípio",
            "infinitivo",
            "infinitivo-pessoal-presente",
            "infinitivo-pessoal-composto",
            "afirmativo",
            "negativo",
            "gerúndio",
        ]

    def _get_auxilary_verb(
        self,
        co: ConjugationObjects,
        mood_name: str,
        tense_name: str,
    ) -> str:
        return "ter"

    def _get_infinitive_mood_name(self):
        return "infinitivo"

    def _get_indicative_mood_name(self):
        return "indicativo"

    def _get_subjunctive_mood_name(self) -> str:
        return "subjuntivo"

    def _get_conditional_mood_name(self):
        return "condicional"

    def _get_participle_mood_name(self) -> str:
        return "particípio"

    def _get_participle_tense_name(self) -> str:
        return "particípio"

    def _get_compound_conjugations_aux_verb_map(
        self,
    ) -> Dict[str, Dict[str, Tuple[str, ...]]]:
        return {
            "indicativo": {
                "pretérito-perfeito-composto": ("indicativo", "presente"),
                "pretérito-mais-que-perfeito-composto": (
                    "indicativo",
                    "pretérito-imperfeito",
                ),
                "pretérito-mais-que-perfeito-anterior": (
                    "indicativo",
                    "pretérito-mais-que-perfeito",
                ),
                "futuro-do-presente-composto": ("indicativo", "futuro-do-presente"),
            },
            "subjuntivo": {
                "pretérito-perfeito": ("subjuntivo", "presente"),
                "pretérito-mais-que-perfeito": ("subjuntivo", "pretérito-imperfeito"),
                "futuro-composto": ("subjuntivo", "futuro"),
            },
            "condicional": {
                "futuro-do-pretérito-composto": ("condicional", "futuro-do-pretérito")
            },
            "infinitivo": {
                "infinitivo-pessoal-composto": (
                    "infinitivo",
                    "infinitivo-pessoal-presente",
                )
            },
        }
