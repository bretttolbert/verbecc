# -*- coding: utf-8 -*-

from typing import Dict, List, Tuple

from verbecc import inflector
from verbecc import string_utils


class InflectorIt(inflector.Inflector):
    @property
    def lang(self) -> str:
        return "it"

    def __init__(self):
        super(InflectorIt, self).__init__()

    def _split_reflexive(self, infinitive):
        is_reflexive = False
        if infinitive.startswith("si "):
            is_reflexive = True
            infinitive = infinitive[3:]
        elif infinitive.startswith("s'"):
            is_reflexive = True
            infinitive = infinitive[2:]
        return is_reflexive, infinitive

    def _add_reflexive_pronoun(self, s):
        if string_utils.starts_with_vowel(s):
            return "s'" + s
        else:
            return "si " + s

    def _add_subjunctive_relative_pronoun(self, s, tense_name):
        return "che " + s

    def _get_default_pronoun(self, person, gender="m", is_reflexive=False):
        ret = ""
        if person == "1s":
            ret = "io"
            if is_reflexive:
                ret = "mi"
        elif person == "2s":
            ret = "tu"
            if is_reflexive:
                ret = "ti"
        elif person == "3s":
            ret = "lui"
            if gender == "f":
                ret = "lei"
            if is_reflexive:
                ret = "si"
        elif person == "1p":
            ret = "noi"
            if is_reflexive:
                ret = "ci"
        elif person == "2p":
            ret = "voi"
            if is_reflexive:
                ret = "vi"
        elif person == "3p":
            ret = "loro"
            if is_reflexive:
                ret = "si"
        return ret

    def _get_tenses_conjugated_without_pronouns(self):
        return ["affermativo", "negativo", "Negativo", "gerundio", "participio"]

    def _get_auxilary_verb(self, co, mood_name, tense_name):
        return "avere"

    def _get_subjunctive_mood_name(self):
        return "congiuntivo"

    def _get_participle_mood_name(self):
        return "participio"

    def _get_participle_tense_name(self):
        return "participio"

    def _get_compound_conjugations_aux_verb_map(
        self,
    ) -> Dict[str, Dict[str, Tuple[str, ...]]]:
        return {
            "indicativo": {
                "passato-prossimo": ("indicativo", "presente"),
                "trapassato-prossimo": ("indicativo", "imperfetto"),
                "trapassato-remoto": ("indicativo", "passato-remoto"),
                "futuro-anteriore": ("indicativo", "futuro"),
            },
            "congiuntivo": {
                "passato": ("congiuntivo", "presente"),
                "trapassato": ("congiuntivo", "imperfetto"),
            },
            "condizionale": {"passato": ("condizionale", "presente")},
        }
