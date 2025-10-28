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
from verbecc.src.utils.string_utils import strip_accents


class InflectorEs(Inflector):
    def __init__(self) -> None:
        super(InflectorEs, self).__init__()

    @property
    def lang(self) -> LangCodeISO639_1:
        return LangCodeISO639_1.es

    def add_adverb_if_applicable(self, s: str, mood: Mood, tense: Tense) -> str:
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

    def get_tenses_conjugated_without_pronouns(self) -> List[Tense]:
        return [
            Tense.Participo,
            Tense.Gerundio,
            Tense.Infinitivo,
            Tense.Afirmativo,
            Tense.Negativo,
        ]

    def get_auxiliary_verb(
        self,
        co: ConjugationObjects,
        mood: Mood,
        tense: Tense,
    ) -> str:
        return "haber"

    def get_infinitive_mood(self) -> Mood:
        return Mood.Infinitivo

    def get_indicative_mood(self) -> Mood:
        return Mood.Indicativo

    def get_subjunctive_mood(self) -> Mood:
        return Mood.Subjuntivo

    def get_conditional_mood(self) -> Mood:
        return Mood.Condicional

    def get_participle_mood(self) -> Mood:
        return Mood.Participo

    def get_participle_tense(self) -> Mood:
        return Tense.Participo

    def get_alternate_hv_inflection(self, s: str) -> str:
        if s.endswith("hay"):
            return s[:-1]
        return s

    def get_compound_conjugations_aux_verb_map(
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
        Vos is conjugated like the vosotros form but without the 'i'
        as the second-to-last letter in the ending and with the vowel
        accented.
        For example, the present indicative forms are:

        Regular (indictive):
            vosotros bebéis -> vos bebés
            vosotros habláis -> vos hablás
            vosotros dormís -> vos dormís
        Regular (subjunctive):
            vosotros seáis -> vos seas
        Irregular:
            vosotors sois -> vos sos

        Regular:
            "éis" -> "és"
            "áis" -> "ás"
            "ís" -> "ís"
        Irregular:
            "oís" -> "os"

        For the imperativo affirmativo we just drop the 'd' and accent the vowel e.g.
            (vosotros) hablad -> (vos) hablá
            (vosotros) sed -> (vos) sé
        The imperativo negativo is the same as tú.

        """
        # only need to accent 'a', 'e' and 'i', AFAIK
        VOWEL_ACCENT_MAP = {"a": "á", "e": "é", "i": "í"}
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

                    # modify the endings for voseo to form the vos endings
                    for i, ending in enumerate(replacement_person_ending.get_endings()):

                        if mood in (Mood.Indicativo, Mood.Subjuntivo):
                            # step one for indicativo and subjuntivo presente:
                            # remove 'i' in the second-to-last letter position
                            if ending[-2] == "i":
                                ending = ending[:-2] + ending[-1]
                        if mood == Mood.Imperativo:
                            # step one for imperativo: remove the trailing 'd'
                            if ending[-1] == "d":
                                ending = ending[:-1]

                        if mood == Mood.Subjuntivo:
                            # step two for subjunctivo is to strip any accents from vowels
                            # e.g. vosotros seáis -> vos seas
                            ending = strip_accents(ending)
                        else:
                            # step two for indicativo and imperativo is to accent the vowel which
                            # is now in the second-to-last or last letter position (if not already accented)

                            # accent second-to-last letter, if vowel
                            if len(ending) > 1:
                                if ending[-2] in VOWEL_ACCENT_MAP:
                                    ending = (
                                        ending[:-2]
                                        + VOWEL_ACCENT_MAP[ending[-2]]
                                        + ending[-1]
                                    )
                            # accent last letter, if vowel
                            if ending[-1] in VOWEL_ACCENT_MAP:
                                ending = ending[:-1] + VOWEL_ACCENT_MAP[ending[-1]]

                        # update the replacement person ending with the modified ending
                        replacement_person_ending.endings[i] = ending
                    return replacement_person_ending
        return person_ending
