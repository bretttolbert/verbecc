import copy
from typing import cast, Dict, List, Tuple

from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.lang_code import LangCodeISO639_1
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.mood import MoodEs as Mood
from verbecc.src.defs.types.tense import TenseEs as Tense
from verbecc.src.defs.types.lang_specific_options import (
    LangSpecificOptions,
)
from verbecc.src.defs.types.lang.es.lang_specific_options_es import (
    LangSpecificOptionsEs,
)
from verbecc.src.defs.types.lang.es.voseo_options import VoseoOptions
from verbecc.src.inflectors.inflector import Inflector
from verbecc.src.conjugator.conjugation_object import ConjugationObjects
from verbecc.src.parsers.tense_template import TenseTemplate
from verbecc.src.parsers.person_ending import PersonEnding


class InflectorEs(Inflector):
    @property
    def lang(self) -> LangCodeISO639_1:
        return LangCodeISO639_1.es

    def __init__(self) -> None:
        super(InflectorEs, self).__init__()

    def _add_adverb_if_applicable(self, s: str, mood: Mood, tense: Tense) -> str:
        if mood == Mood.Imperativo and tense == Tense.Negativo:
            return "no " + s
        return s

    def get_default_pronoun(
        self,
        person: Person,
        gender: Gender = Gender.m,
        is_reflexive: bool = False,
        lang_specific_options: LangSpecificOptions = None,
    ) -> str:
        lang_opts = None
        if lang_specific_options is not None:
            lang_opts = cast(LangSpecificOptionsEs, lang_specific_options)

        ret = ""
        if person == Person.FirstPersonSingular:
            ret = "yo"
            if is_reflexive:
                ret += " me"
        elif person == Person.SecondPersonSingular:
            if (
                lang_opts is not None
                and lang_opts.voseo_options != VoseoOptions.NoVoseo
            ):
                ret = "vos"
            else:
                ret = "tú"
            if is_reflexive:
                ret += " te"
        elif person == Person.ThirdPersonSingular:
            ret = "él"
            if gender == Gender.f:
                ret = "ella"
            if is_reflexive:
                ret += " se"
        elif person == Person.FirstPersonPlural:
            ret = "nosotros"
            if is_reflexive:
                ret += " nos"
        elif person == Person.SecondPersonPlural:
            ret = "vosotros"
            if is_reflexive:
                ret += " os"
        elif person == Person.ThirdPersonPlural:
            ret = "ellos"
            if gender == Gender.f:
                ret = "ellas"
            if is_reflexive:
                ret += " se"
        return ret

    def _get_tenses_conjugated_without_pronouns(self) -> List[Tense]:
        return [
            Tense.Participo,
            Tense.Gerundio,
            Tense.Infinitivo,
            Tense.Afirmativo,
            Tense.Negativo,
        ]

    def _get_auxilary_verb(
        self,
        co: ConjugationObjects,
        mood: Mood,
        tense: Tense,
    ) -> str:
        return "haber"

    def _get_infinitive_mood(self) -> Mood:
        return Mood.Infinitivo

    def _get_indicative_mood(self) -> Mood:
        return Mood.Indicativo

    def _get_subjunctive_mood(self) -> Mood:
        return Mood.Subjuntivo

    def _get_conditional_mood(self) -> Mood:
        return Mood.Condicional

    def _get_participle_mood(self) -> Mood:
        return Mood.Participo

    def _get_participle_tense(self) -> Mood:
        return Tense.Participo

    def _get_alternate_hv_inflection(self, s: str) -> str:
        if s.endswith("hay"):
            return s[:-1]
        return s

    def _get_compound_conjugations_aux_verb_map(
        self,
    ) -> Dict[Mood, Dict[Tense, Tuple[Mood, Tense]]]:
        return {
            Mood.Indicativo: {
                Tense.PretéritoPerfectoCompuesto: (
                    Mood.Indicativo,
                    Tense.Presente,
                ),
                Tense.PretéritoPluscuamperfecto: (
                    Mood.Indicativo,
                    Tense.PretéritoImperfecto,
                ),
                Tense.PretéritoAnterior: (
                    Mood.Indicativo,
                    Tense.PretéritoPerfectoSimple,
                ),
                Tense.FuturoPerfecto: (Mood.Indicativo, Tense.Futuro),
            },
            Mood.Condicional: {Tense.Perfecto: (Mood.Condicional, Tense.Presente)},
            Mood.Subjuntivo: {
                Tense.PretéritoPerfecto: (Mood.Subjuntivo, Tense.Presente),
                Tense.PretéritoPluscuamperfecto1: (
                    Mood.Subjuntivo,
                    Tense.PretéritoImperfecto1,
                ),
                Tense.PretéritoPluscuamperfecto2: (
                    Mood.Subjuntivo,
                    Tense.PretéritoImperfecto2,
                ),
                Tense.FuturoPerfecto: (Mood.Subjuntivo, Tense.Futuro),
            },
        }

    def modify_person_ending_if_applicable(
        self,
        person_ending: PersonEnding,
        mood: Mood,
        tense: Tense,
        tense_template: TenseTemplate,
        lang_specific_options: LangSpecificOptions,
    ) -> PersonEnding:
        """
        Hook for certain languages e.g. Spanish that modify
        the standard person endings for certain persons depending
        on language specific options (e.g. Voseo)

        Vos may be used in place of tú in the second person singular
        with corresponding changes to verb endings.
        The verb endings for vos are different from those for tú in
        the present indicative, present subjunctive, and imperative moods.
        Vos is conjugated like the vosotros form but without the 'i' in the ending.
        For example, the present indicative forms are:

        vosotros bebéis -> vos bebés
        vosotros habláis -> vos hablás
        vosotros dormís -> vos dormís

        "éis" -> "és"
        "áis" -> "ás"
        "ís" -> "ís"

        For the imperativo affirmativo we just drop the 'd' and accent the vowel e.g.
        (vosotros) hablad -> (vos) hablá
        The imperativo negativo is the same as tú.

        """
        # map of vosotros endings to vos endings
        # for the present indicative, present subjunctive
        VOSEO_ENDINGS_MAP_INDICATIVE_OR_SUBJUNCTIVE_PRESENT: Dict[str, str] = {
            "as": "ás",
            "es": "és",
            "ís": "ís",
            "áis": "ás",
            "éis": "és",
        }
        VOSEO_ENDINGS_MAP_IMPERATIVE: Dict[str, str] = {"ad": "á", "id": "í", "ed": "é"}
        lang_opts = None
        if lang_specific_options is not None:
            lang_opts = cast(LangSpecificOptionsEs, lang_specific_options)
            if (
                lang_opts is not None
                and lang_opts.voseo_options != VoseoOptions.NoVoseo
                and person_ending.person == Person.SecondPersonSingular
            ):
                if lang_opts.voseo_options != VoseoOptions.VoseoTipo3:
                    # only voseo tipo 3 (voseo típico aka Rioplatense) is supported at the moment
                    raise NotImplementedError

                if (
                    (mood == Mood.Indicativo and tense == Tense.Presente)
                    or (mood == Mood.Subjuntivo and tense == Tense.Presente)
                    or (mood == Mood.Imperativo and tense == Tense.Afirmativo)
                ):
                    # first replace with given SecondPersonSingular (tú) ending(s)
                    # with the SecondPersonPlural (vosotros) ending(s)
                    replacement_person_ending = copy.deepcopy(
                        tense_template.get_person_ending(Person.SecondPersonPlural)
                    )
                    # change replacement PersonEnding Person from second person plural to singular
                    replacement_person_ending.person = Person.SecondPersonSingular

                    # modify the endings for voseo
                    for i, ending in enumerate(replacement_person_ending.get_endings()):
                        endings_map = (
                            VOSEO_ENDINGS_MAP_INDICATIVE_OR_SUBJUNCTIVE_PRESENT
                        )
                        if mood == Mood.Imperativo:
                            endings_map = VOSEO_ENDINGS_MAP_IMPERATIVE
                        for e in endings_map:
                            # e.g. if ending is "sed", it endswith "ed", so "s" + "é" -> "sé"
                            if ending.endswith(e):
                                replacement_person_ending.endings[i] = (
                                    ending[: -len(e)] + endings_map[e]
                                )
                                break
                    return replacement_person_ending
        return person_ending
