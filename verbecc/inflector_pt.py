# -*- coding: utf-8 -*-

from typing import Dict, List, Tuple

from verbecc import inflector


class InflectorPt(inflector.Inflector):
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
        self, s: str, is_reflexive: bool, mood_name: str, tense_name: str, person
    ):
        imperative = mood_name == "imperativo"
        if imperative or (
            mood_name == "infinitivo" and tense_name == "infinitivo-pessoal-presente"
        ):
            s += " " + self._get_pronoun_suffix(person, imperative=imperative)
        return s

    def _get_default_pronoun(self, person, gender="m", is_reflexive=False):
        ret = ""
        if person == "1s":
            ret = "eu"
            if is_reflexive:
                ret += " me"
        elif person == "2s":
            ret = "tu"
            if is_reflexive:
                ret += " te"
        elif person == "3s":
            ret = "ele"
            if gender == "f":
                ret = "ela"
            if is_reflexive:
                ret += " se"
        elif person == "1p":
            ret = "nós"
            if is_reflexive:
                ret += " nos"
        elif person == "2p":
            ret = "vós"
            if is_reflexive:
                ret += " se"
        elif person == "3p":
            ret = "eles"
            if gender == "f":
                ret = "elas"
            if is_reflexive:
                ret += " se"
        return ret

    def _get_pronoun_suffix(self, person, gender="m", imperative=True):
        ret = ""
        if person == "1s":
            ret = "eu"
        if person == "2s":
            ret = "tu"
        elif person == "3s":
            ret = "você"
            if not imperative:
                ret = "ele"
        elif person == "1p":
            ret = "nós"
        elif person == "2p":
            ret = "vós"
        elif person == "3p":
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
        co: inflector.Inflector.ConjugationObjects,
        mood_name: str,
        tense_name: str,
    ) -> str:
        return "ter"

    def _get_subjunctive_mood_name(self) -> str:
        return "subjuntivo"

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
