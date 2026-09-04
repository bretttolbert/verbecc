import copy
from typing import cast, Optional, Tuple

from verbecc.core.conjugator.conjugation_object import ConjugationObjects
from verbecc.core.defs.types.data.person_ending import PersonEnding
from verbecc.core.defs.types.data.tense_template import TenseTemplate
from verbecc.core.defs.types.gender import Gender
from verbecc.core.defs.types.lang_code import LangCodeISO639_1
from verbecc.core.defs.types.lang_specific_options import LangSpecificOptions
from verbecc.core.defs.types.lang_specific_options import LangSpecificOptionsEs
from verbecc.core.defs.types.lang_specific_options import LangSpecificOptionsFactory
from verbecc.core.defs.types.lang_specific_options import VoseoOptions
from verbecc.core.defs.types.mood import Mood, Moods
from verbecc.core.defs.types.number import Number
from verbecc.core.defs.types.person import Person
from verbecc.core.defs.types.tense import Tense, Tenses
from verbecc.core.inflectors.inflector import Inflector
from verbecc.core.utils.string_utils import strip_accents
from verbecc.core.defs.types.pronoun import Pronoun, Pronouns


class InflectorEs(Inflector):
    def __init__(
        self, lang_specific_options: Optional[LangSpecificOptions] = None
    ) -> None:
        super(InflectorEs, self).__init__()
        if lang_specific_options is not None:
            self.lang_specific_options = cast(
                LangSpecificOptionsEs, lang_specific_options
            )
        else:
            self.lang_specific_options = cast(
                LangSpecificOptionsEs,
                LangSpecificOptionsFactory.make_lang_specific_options(self.get_lang()),
            )

    def get_lang(self) -> LangCodeISO639_1:
        return LangCodeISO639_1.es

    def add_adverb_if_applicable(self, s: str, mood: Mood, tense: Tense) -> str:
        if mood == Moods.es.Imperativo and tense == Tenses.es.Negativo:
            return "no " + s
        return s

    def get_pronoun_gender(self, pronoun: Pronoun) -> Optional[Gender]:
        if pronoun in (Pronouns.es.ella, Pronouns.es.ellas):
            return Gender.f
        elif pronoun in (Pronouns.es.él, "ello", Pronouns.es.ellos):
            return Gender.m
        return None

    def get_pronouns(
        self,
        person: Optional[Person] = None,
        number: Optional[Number] = None,
        gender: Optional[Gender] = None,
        imperative: bool = False,
    ) -> list[Pronoun]:
        ret = []
        if (person is None or person == Person.First) and (
            number is None or number == Number.Singular
        ):
            p = Pronouns.es.yo
            ret.append(p)
        if (person is None or person == Person.Second) and (
            number is None or number == Number.Singular
        ):
            pronouns = [Pronouns.es.tú, Pronouns.es.vos]
            ret.extend(pronouns)
        if (person is None or person == Person.Third) and (
            number is None or number == Number.Singular
        ):
            pronouns = [Pronouns.es.él, Pronouns.es.ella, Pronouns.es.usted]
            if gender is not None:
                if gender == Gender.m:
                    pronouns = [Pronouns.es.él]
                else:
                    pronouns = [Pronouns.es.ella]
            ret.extend(pronouns)
        if (person is None or person == Person.First) and (
            number is None or number == Number.Plural
        ):
            p = Pronouns.es.nosotros
            ret.append(p)
        if (person is None or person == Person.Second) and (
            number is None or number == Number.Plural
        ):
            p = Pronouns.es.vosotros
            ret.append(p)
        if (person is None or person == Person.Third) and (
            number is None or number == Number.Plural
        ):
            pronouns = [Pronouns.es.ellos, Pronouns.es.ellas, Pronouns.es.ustedes]
            if gender is not None:
                if gender == Gender.m:
                    pronouns = [Pronouns.es.ellos]
                else:
                    pronouns = [Pronouns.es.ellas]
            ret.extend(pronouns)
        return ret

    def make_pronoun_reflexive(self, pronoun: str) -> str:
        if pronoun == Pronouns.es.yo:
            return pronoun + " me"
        elif pronoun in (Pronouns.es.tú, Pronouns.es.vos):
            return pronoun + " te"
        elif pronoun == Pronouns.es.vosotros:
            return pronoun + " os"
        elif pronoun == Pronouns.es.nosotros:
            return pronoun + " nos"
        else:
            return pronoun + " se"

    def get_tenses_conjugated_without_pronouns(self) -> list[Tense]:
        return [
            Tenses.es.Participo,
            Tenses.es.Gerundio,
            Tenses.es.Infinitivo,
            Tenses.es.Afirmativo,
            Tenses.es.Negativo,
        ]

    def get_auxiliary_verb(
        self,
        co: ConjugationObjects,
        mood: Mood,
        tense: Tense,
    ) -> str:
        return "haber"

    def get_infinitive_mood(self) -> Mood:
        return Moods.es.Infinitivo

    def get_imperative_mood(self) -> Mood:
        return Moods.es.Imperativo

    def get_indicative_mood(self) -> Mood:
        return Moods.es.Indicativo

    def get_subjunctive_mood(self) -> Mood:
        return Moods.es.Subjuntivo

    def get_conditional_mood(self) -> Mood:
        return Moods.es.Condicional

    def get_participle_mood(self) -> Mood:
        return Moods.es.Participo

    def get_participle_tense(self) -> Tense:
        return Tenses.es.Participo

    def get_alternate_hv_inflection(self, s: str) -> str:
        if s.endswith("hay"):
            return s[:-1]
        return s

    def get_compound_conjugations_aux_verb_map(
        self,
    ) -> dict[Mood, dict[Tense, Tuple[Mood, Tense]]]:
        return {
            Moods.es.Indicativo: {
                Tenses.es.PretéritoPerfectoCompuesto: (
                    Moods.es.Indicativo,
                    Tenses.es.Presente,
                ),
                Tenses.es.PretéritoPluscuamperfecto: (
                    Moods.es.Indicativo,
                    Tenses.es.PretéritoImperfecto,
                ),
                Tenses.es.PretéritoAnterior: (
                    Moods.es.Indicativo,
                    Tenses.es.PretéritoPerfectoSimple,
                ),
                Tenses.es.FuturoPerfecto: (Moods.es.Indicativo, Tenses.es.Futuro),
            },
            Moods.es.Condicional: {
                Tenses.es.Perfecto: (Moods.es.Condicional, Tenses.es.Presente)
            },
            Moods.es.Subjuntivo: {
                Tenses.es.PretéritoPerfecto: (Moods.es.Subjuntivo, Tenses.es.Presente),
                Tenses.es.PretéritoPluscuamperfecto1: (
                    Moods.es.Subjuntivo,
                    Tenses.es.PretéritoImperfecto1,
                ),
                Tenses.es.PretéritoPluscuamperfecto2: (
                    Moods.es.Subjuntivo,
                    Tenses.es.PretéritoImperfecto2,
                ),
                Tenses.es.FuturoPerfecto: (Moods.es.Subjuntivo, Tenses.es.Futuro),
            },
        }

    def modify_person_ending_if_applicable(
        self,
        person_ending: PersonEnding,
        mood: Mood,
        tense: Tense,
        tense_template: TenseTemplate,
        pronoun: Optional[str],
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
        if self.lang_specific_options is not None:
            if (
                pronoun is not None
                and pronoun == "vos"
                and person_ending.person == Person.Second
                and person_ending.number == Number.Singular
            ):
                if (
                    self.lang_specific_options is not None
                    and self.lang_specific_options.get_voseo_options()
                    != VoseoOptions.VoseoTipo3
                ):
                    # only voseo tipo 3 (voseo típico aka Rioplatense) is supported at the moment
                    raise NotImplementedError()

                if (
                    (mood == Moods.es.Indicativo and tense == Tenses.es.Presente)
                    or (mood == Moods.es.Subjuntivo and tense == Tenses.es.Presente)
                    or (mood == Moods.es.Imperativo and tense == Tenses.es.Afirmativo)
                ):
                    # first replace with given p2s (tú) ending(s)
                    # with the p2p (vosotros) ending(s)
                    replacement_person_ending = copy.deepcopy(
                        tense_template.get_person_ending(Person.Second, Number.Plural)
                    )
                    # change replacement PersonEnding Person from second person plural to singular
                    replacement_person_ending.person = Person.Second
                    replacement_person_ending.number = Number.Singular

                    # modify the endings for voseo to form the vos endings
                    for i, ending in enumerate(replacement_person_ending.get_endings()):

                        if mood in (Moods.es.Indicativo, Moods.es.Subjuntivo):
                            # step one for indicativo and subjuntivo presente:
                            # remove 'i' in the second-to-last letter position
                            if ending[-2] == "i":
                                ending = ending[:-2] + ending[-1]
                        if mood == Moods.es.Imperativo:
                            # step one for imperativo: remove the trailing 'd'
                            if ending[-1] == "d":
                                ending = ending[:-1]

                        if mood == Moods.es.Subjuntivo:
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

    def split_reflexive(self, infinitive: str) -> Tuple[bool, str]:
        """
        Tests whether an infinitive is reflexive
        Returns a 2-tuple of whether it is reflexive
        and the non-reflexive form of the infinitive.

        E.g. French:
        "se raser" => (True, "raser")
        "s'habiller" => (True, "habiller")
        "parler" => (False, "parler")
        E.g. Italian:
        "alzarsi" => (True, "alzare")
        "preoccuparsi" => (True, "preoccupare")

        E.g. Spanish
        "levantarse" => (True, "levantar")

        E.g. Portuguese
        "vestir-se" => (True, "vestir")
        """
        if infinitive.endswith("se"):
            return (True, infinitive[:-2])
        else:
            return (False, infinitive)
